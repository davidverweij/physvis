import click

from . import __version__
from . import physvis

@click.command()
@click.version_option(version=__version__)
@click.option("--delimiter", "-d", default=";", help="Delimiter used in your csv files. Default is ';'")
@click.option("--output", "-o", default="output", help="The output location to store the result. Default is 'output'")
@click.option("--input", "-i", default="input", help="The input location of the .csv files. Default is 'input'")
@click.option('--save', '-s', is_flag=True)
def main(input: str, output: str, delimiter: str, save: bool) -> None:
    click.echo(f"Collecting .csv files from {input}")
    physvis.collect(input, output, delimiter, save, verbose = True)
    click.echo("Done.")
    if save:
        click.echo(f"See the {output}/combined.csv for the combined result")


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
