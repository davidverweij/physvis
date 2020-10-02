# physvis
A command line interface (CLI) to visualise and analyse physicalisations (physical visualisations) from `.csv` files

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

```shell
poetry run convert --data "path/to/data.csv" --template "path/to/template.docx" --name csv_column_name
```

Where the arguments are your Microsoft Word template (`.docx`), your data to apply to the template (`.csv`) and the column name (case sensitive) to generate filenames for the output `.docx` files. Optional arguments allow you to indicate a delimiter other than `;` in your `csv` data file, and an ouput folder other than the default `output` in the current directory:

```shell
poetry run vis
```

For help, run

```shell
poetry run vis --help
```

For a demo, run

```shell
poetry run vis -t tests/data/example.docx -c tests/data/example.csv -n NAME
```

## Prepare your `.csv` data files
...
