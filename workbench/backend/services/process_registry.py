"""
Process registry for the workbench.

A single instance of :class:`ProcessRegistry` lives for the lifetime
of the workbench process.  Background run threads register the
``Popen`` they launch with :meth:`register` so that the API can later:

* abort a single run (:meth:`abort`)
* abort all running runs (:meth:`abort_all`) -- called from the
  shutdown handler so the server does not leave dangling
  ``phreeqc.exe`` children behind

The registry is intentionally minimal: it tracks ``(run_id,
subprocess.Popen)`` pairs and is thread-safe.  We do *not* track
threads, because a run that hasn't reached the PHREEQC subprocess yet
can be aborted by simply flipping its status to ``"aborted"`` in
storage; the runner's own progress checks are best-effort.
"""

from __future__ import annotations

import os
import signal
import subprocess
import threading
import time
from typing import Optional


class ProcessRegistry:
    def __init__(self) -> None:
        self._lock = threading.RLock()
        self._procs: dict[str, subprocess.Popen] = {}

    # ---- registration --------------------------------------------------
    def register(self, run_id: str, proc: subprocess.Popen) -> None:
        with self._lock:
            self._procs[run_id] = proc

    def unregister(self, run_id: str) -> None:
        with self._lock:
            self._procs.pop(run_id, None)

    # ---- queries -------------------------------------------------------
    def is_running(self, run_id: str) -> bool:
        with self._lock:
            proc = self._procs.get(run_id)
            return proc is not None and proc.poll() is None

    def list_running(self) -> list[str]:
        with self._lock:
            # Drop finished children opportunistically.
            for rid in list(self._procs.keys()):
                if self._procs[rid].poll() is not None:
                    self._procs.pop(rid, None)
            return [rid for rid, p in self._procs.items() if p.poll() is None]

    # ---- termination ---------------------------------------------------
    def abort(self, run_id: str, *, grace_seconds: float = 2.0) -> bool:
        """Best-effort terminate of one run's PHREEQC subprocess.

        Returns ``True`` if a process was found and a terminate signal
        was sent.  The caller should also flip the run's stored status
        to ``"aborted"``; the registry only handles the OS-level kill.
        """
        with self._lock:
            proc: Optional[subprocess.Popen] = self._procs.get(run_id)
        if proc is None:
            return False
        return _terminate(proc, grace_seconds=grace_seconds)

    def abort_all(self, *, grace_seconds: float = 2.0) -> list[str]:
        """Terminate every registered child.  Returns the list of run_ids
        that had a live process.
        """
        with self._lock:
            snapshot = list(self._procs.items())
        aborted: list[str] = []
        for rid, proc in snapshot:
            if proc.poll() is None:
                if _terminate(proc, grace_seconds=grace_seconds):
                    aborted.append(rid)
        return aborted


def _terminate(proc: subprocess.Popen, *, grace_seconds: float) -> bool:
    """Send ``CTRL_BREAK`` on Windows, ``SIGTERM`` on POSIX; fall back to kill.

    On Windows, ``Popen.terminate()`` only calls ``TerminateProcess``,
    which is harsher than a clean CTRL_BREAK.  For PHREEQC (a console
    exe) CTRL_BREAK is enough to interrupt its current step and let
    cleanup run.
    """
    if proc.poll() is not None:
        return False
    try:
        if os.name == "nt":
            # Best-effort CTRL_BREAK (only works for processes started
            # with CREATE_NEW_PROCESS_GROUP).  Our launcher uses that,
            # so this is the preferred path; fall back to terminate on
            # failure.
            try:
                proc.send_signal(signal.CTRL_BREAK_EVENT)
            except (ValueError, OSError):
                proc.terminate()
        else:
            proc.terminate()
    except OSError:
        try:
            proc.kill()
        except OSError:
            return False
    try:
        proc.wait(timeout=grace_seconds)
    except subprocess.TimeoutExpired:
        try:
            proc.kill()
            proc.wait(timeout=grace_seconds)
        except Exception:  # noqa: BLE001
            pass
    return True


# Module-level singleton
registry = ProcessRegistry()
