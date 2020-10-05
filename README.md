[![Project Status: WIP – Initial development is in progress, but there has not yet been a stable, usable release suitable for the public.](https://www.repostatus.org/badges/latest/wip.svg)](https://www.repostatus.org/#wip)

# physvis
A command line interface (CLI) to reconstruct, visualise and analyse data from physicalisations (physical visualisations) from `.csv` files, using [plotly](https://plotly.com/) and [pandas](https://pandas.pydata.org/).

> This is a tool originally written for a single use case - so bear with me on the sloppiness. I intend to transfer this tool to colleagues in a modular fashion - this process is a work-in-progress.

![Example reconstruction of a physicalisation](/assets/example.jpg)

_Example reconstruction of a physicalisation_

## Installing

[Poetry](https://python-poetry.org/) is used for dependency management and
[pyenv](https://github.com/pyenv/pyenv) to manage python installations.

With Poetry and pyenv installed, clone this repository and install dependencies via:

```shell
poetry install --no-dev
```

To setup a virtual environment with your local pyenv version run:

```shell
poetry shell
```

### CLI usage
The tool is split in 5 methods:
```shell
poetry run vis      # provides a CLI to select one trial, and 3D visualises this in an HTML page
poetry run collect  # gathers separate .csv files from trials and collates them in one
poetry run calc     # analyses the collected .csv - various calculations are provided
poetry run print    # takes a list of trials and reconstructs a 3D visual (.jpg) for each
poetry run heatmap  # a special case for the 'print' command, incorporates heatmap data
```

## Prepare your `.csv` data files
...
