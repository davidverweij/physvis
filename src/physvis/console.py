import click

from . import __version__
from . import physvis

@click.command()
@click.version_option(version=__version__)
@click.option("--input", "-i", default="output/combined.csv", help="The location of the large .csv file compiled by collect(). Default is 'output/combined.csv'")
def main(input: str, output: str, delimiter: str, save: bool) -> None:
    click.echo(f"Collecting .csv files from {input}")
    physvis.collect(input, output, delimiter, save = True)
    click.echo("Done.")


@click.command()
@click.option("--delimiter", "-d", default=";", help="Delimiter used in your csv files. Default is ';'")
@click.option("--output", "-o", default="output", help="The output location to store the result. Default is 'output'")
@click.option("--input", "-i", default="input", help="The input location of the .csv files. Default is 'input'")
def vis(input: str, output: str, delimiter: str) -> None:
    click.echo(f"Collecting Data")
    frame = physvis.collect(input, output, delimiter)
    click.echo(f"Generating Visualisation")
    physvis.display(frame)
    click.echo(f"Done Visualising")


@click.command()
@click.option("--delimiter", "-d", default=";", help="Delimiter used in your csv files. Default is ';'")
@click.option("--input", "-i", default="input", help="The input location of the .csv files. Default is 'input'")
def collect(input: str, delimiter: str) -> None:
    click.echo(f"Collecting Data from {input}")
    frame = physvis.generate_large_csv(input = input, output = 'output', delimiter = delimiter, save = True)
    click.echo(f"See the output/combined.csv for the combined result")
