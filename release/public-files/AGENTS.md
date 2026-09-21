# auto-phreeqc: public agent instructions

This repository is a user-facing PHREEQC simulation toolkit. Do not look for
or recreate private development notes, prompts, or local machine settings.

## First use

When the user asks to configure this repository, run:

```bash
python scripts/bootstrap.py
```

It creates a project-local `.auto-phreeqc-venv` environment, installs the public package,
locates PHREEQC, saves only local paths in `.phreeqc-auto.local.json`, and runs
a disposable calculation. If PHREEQC is missing, explain that the official
USGS installation is required and resume this command after it is installed.
Do not silently install an external operating-system package.

For PHREEQC modelling requests, use the repository Skill at
`.agents/skills/phreeqc-auto/`. Keep each calculation in a new results
directory and preserve its input, raw output, structured results, and charts.
Before running a calculation, summarize assumptions and ask about material
missing conditions.
