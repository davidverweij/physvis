import click

from . import __version__
from . import physvis

@click.command()
@click.version_option(version=__version__)
@click.option(
    "--delimiter", "-d", default=";", help="Delimiter used in your csv files. Default is ';'"
)
@click.option("--output", "-o", default="output", help="The output location to store the result. Default is 'output'")
@click.option("--input", "-i", default="input", help="The input location of the .csv files. Default is 'input'")
def main(input: str, output: str, delimiter: str) -> None:
    physvis.convert(input, output, delimiter)
