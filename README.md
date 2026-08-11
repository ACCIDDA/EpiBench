# EpiBenchmark

EpiBench is a work-in-progress benchmarking tool for evaluating performance of infectious disease forecasting models. The package is still in development.

## Choose the installation guide that matches your environment:
- **Personal computer or standard Linux workstation (Windows/macOS/Linux):** Continue with the instructions below.
- **High-performance computing (HPC) cluster:** See [`installation_longleaf`](https://accidda.github.io/EpiBenchmark/getting-started/installation_longleaf/).

## Requirements
- Python 3.10 or later
- Git
- R and the `scoringutils` and `purrr` packages for the `epibench score` command

## Quick Start
```bash
git clone https://github.com/ACCIDDA/EpiBenchmark.git
cd EpiBenchmark
uv sync
uv run epibench --help
```

## Installation

Clone the repository:

```bash
git clone https://github.com/ACCIDDA/EpiBenchmark.git

cd EpiBenchmark
```

EpiBenchmark supports installation using either **uv** (recommended) or **pip**.

## Option 1: Install with uv

This is the fastet installation method.

```bash
uv sync
```

### Activate the virtual environment

### Windows

```bash
.venv\Scripts\activate
```

### macOS/Linux

```bash
source .venv/bin/activate
```

Alternatively, users can run commands without activating the virtual environment when using `uv`:

```bash
uv run epibench --help
```

## Option 2: Install with pip

Create a virtual environment.

### Windows

```bash
python -m venv .venv
.venv\Scripts\activate
```

### macOS/Linux

```bash
python -m venv .venv
source .venv/bin/activate
```

Upgrade pip:

```bash
python -m pip install --upgrade pip
```

Install EpiBenchmark in editable mode:

```bash
python -m pip install -e .
```

## Verify the Installation

After installation, verify that the command-line interface is available:

```bash
epibench
epibench --help
```
Users can also verify the available subcommands:

```bash
epibench create --help
epibench score --help
epibench plot --help
```

## R Requirements for Scoring

The Python virtual environment only manages EpiBenchmark's Python dependencies.
The `epibench score` command also calls `Rscript`, so scoring has two external
requirements:

- `Rscript` must be available on users' `PATH`
- the CRAN packages `scoringutils` and `purrr` must be installed in the R
  library used by that `Rscript`

Check that `R` is available with:

```bash
Rscript --version
```

Install the required R packages with:

```bash
Rscript -e 'install.packages(c("scoringutils", "purrr"))'
```

Verify that the packages are available with:

```bash
Rscript -e 'library(scoringutils); library(purrr)'
```

If `epibench score` reports that `Rscript`, `scoringutils`, or `purrr` is
missing, make sure they are installed in the same R environment used by
`Rscript` command.


## Remove the virtual environment
Deletes the local `.venv` directory, allowing users to create a fresh virtual environment.

### Windows
If Command Prompt:
```bash
rmdir /s /q .venv 
```

If PowerShell:
```bash
Remove-Item -Recurse -Force .venv (PowerShell)
```

### macOS/Linux
```bash
rm -rf .venv
```
