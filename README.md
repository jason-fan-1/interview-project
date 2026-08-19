 # Interview Project

Python environment for data-science interview exercises, managed with [uv](https://docs.astral.sh/uv/).

## Setup

Install [uv](https://docs.astral.sh/uv/getting-started/installation/), then run:

```powershell
uv sync
```

This creates `.venv` from `uv.lock` and installs the runtime and development dependencies.

## Common Commands

```powershell
# Run Python in the project environment
uv run python

# Start JupyterLab
uv run jupyter lab

# Run tests and linting
uv run pytest
uv run ruff check .

# Add a dependency
uv add package-name
```

The environment includes NumPy, pandas, SciPy, scikit-learn, Matplotlib, Seaborn, statsmodels, JupyterLab, and the IPython kernel. Pytest and Ruff are available in the development dependency group.

## Project Layout

```text
src/interview_project/
	preprocessing.py  # data splitting and feature transformations
	modeling.py       # model pipeline construction and training
	evaluation.py     # evaluation metrics
notebooks/
	experiment.ipynb  # VS Code experiment workflow
```

Open `notebooks/experiment.ipynb` in VS Code and select the `.venv` Python interpreter as its kernel. The notebook imports the reusable functions from `interview_project` rather than defining the workflow inline.
