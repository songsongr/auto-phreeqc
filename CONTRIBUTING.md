# Contributing to phreeqc-auto

Thank you for your interest in contributing! This project aims to make geochemical modeling
more accessible through automated workflows, and your help is greatly appreciated.

## How to Contribute

### Reporting Issues

- Check existing issues before creating a new one
- Include PHREEQC version, Python version, and OS
- Provide a minimal reproducible example if possible
- Include error messages and log output

### Suggesting Enhancements

- Describe the geochemical scenario you want to model
- Provide references to relevant literature if applicable
- Explain why existing tools don't cover your use case

### Pull Requests

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run the existing tests
5. Add tests for new functionality
6. Commit with clear messages
7. Open a PR describing the changes and their motivation

### Code Style

- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/)
- Use type hints where practical
- Write docstrings for public functions
- Keep functions focused and testable

### Adding a new geochemical workflow

1. Create a reference document in `.claude/skills/phreeqc-auto/references/`
2. Add coordinator script or extend `generate_input.py` if new PHREEQC keywords are needed
3. Add a test case
4. Verify it runs end-to-end with a real PHREEQC installation

## Development Setup

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/auto-phreeqc.git
cd auto-phreeqc

# Install dependencies
pip install -r requirements.txt
pip install -e .[dev]

# Set up PHREEQC
export PHREEQC_EXE="/path/to/phreeqc.exe"
export PHREEQC_DATABASE="/path/to/phreeqc.dat"
```

## Questions?

Open a [discussion](https://github.com/songsongr/auto-phreeqc/discussions) or issue.
