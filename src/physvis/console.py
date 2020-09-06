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
@click.option("--input", "-i", default="output/combined.csv", help="The location of the large .csv file compiled by collect(). Default is 'output/combined.csv'")
def vis(input: str, delimiter: str) -> None:
    click.echo(f"----- Visualising a specific physicialisation", nl = True)
    frame = physvis.get_large_csv(input, delimiter)
    print(frame.info())

    repeat = True

    while repeat:
        # get user input
        participant = click.prompt("Participant", type=click.Choice([str(x) for x in range(1,21)]))
        condition = click.prompt("Condition", type=click.Choice([str(x) for x in range(3)]))
        orientation = click.prompt("Orientation", type=click.Choice(['N','E','S','W']))
        physicalisation = click.prompt("Physicalisation", type=click.Choice([str(x) for x in range(1,7)]))

        # display result, or err
        try:
            physvis.display(frame, participant, condition, orientation, physicalisation)
        except Exception as e:
            print(f"An error occured in visualising Phys {physicalisation}, for P{participant}_{condition}_{orientation}: {e}")

        # possibly visualise another one
        repeat = False
        if click.confirm('Would you like to visualise another one?'):
            repeat = True

    click.echo(f"Till next time!")


@click.command()
@click.option("--delimiter", "-d", default=";", help="Delimiter used in your csv files. Default is ';'")
@click.option("--input", "-i", default="input", help="The input location of the .csv files. Default is 'input'")
def collect(input: str, delimiter: str) -> None:
    click.echo(f"Collecting Data from {input}")
    frame = physvis.generate_large_csv(input = input, output = 'output', delimiter = delimiter, save = True)
    click.echo(f"See the output/combined.csv for the combined result")
