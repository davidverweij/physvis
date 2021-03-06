import click
import inspect

from . import __version__
from . import interactions
from . import helpers
from . import maths

@click.command()
@click.version_option(version=__version__)
@click.option("--input", "-i", default="output/combined.csv", help="The location of the large .csv file compiled by collect(). Default is 'output/combined.csv'")
def main(input: str, output: str, delimiter: str, save: bool) -> None:

    click.echo(f"Press 'control+c' to abort this program at any point.\n")

    click.echo(f"Collecting .csv files from {input}")
    interactions.collect(input, output, delimiter, save = True)
    click.echo("Done.")


@click.command()
@click.option("--delimiter", "-d", default=";", help="Delimiter used in your csv files. Default is ';'")
@click.option("--input", "-i", default="output/combined.csv", help="The location of the large .csv file compiled by collect(). Default is 'output/combined.csv'")
def vis(input: str, delimiter: str) -> None:
    click.echo(f"Press 'control+c' to abort this program at any point.\n")

    click.echo(f"\nWhich situation do you want to visualise?")
    frame = helpers.get_large_csv(input, delimiter)
    # print(frame.info())

    repeat = True

    while repeat:
        repeat = False

        # get user input
        participant = click.prompt("  Participant", type=click.Choice([str(x) for x in range(1,21)]), show_choices=False)
        condition = click.prompt("  Condition", type=click.Choice([str(x) for x in range(3)]),show_choices=False)
        orientation = click.prompt("  Orientation", type=click.Choice(['N','E','S','W'], case_sensitive=False), show_choices=False)
        physicalisation = click.prompt("  Physicalisation", type=click.Choice([str(x) for x in range(1,7)]), show_choices=False)

        # display result, or err
        try:
            click.echo(f"\nI found this situation:\n")
            interactions.display(frame, participant, condition, orientation, physicalisation)
            click.echo(f"\nThe visualisation should now open in the browser\n")
        except Exception as e:
            print(f"An error occured in visualising Phys {physicalisation}, for P{participant}_{condition}_{orientation}: {e}")

        # possibly visualise another one
        if click.confirm('Would you like to visualise another one?'):
            repeat = True

    click.echo(f"\nTill next time!\n")


@click.command()
@click.option("--delimiter", "-d", default=";", help="Delimiter used in your csv files. Default is ';'")
@click.option("--input", "-i", default="output/combined.csv", help="The location of the large .csv file compiled by collect(). Default is 'output/combined.csv'")
def printheat(input: str, delimiter: str) -> None:
    click.echo(f"Press 'control+c' to abort this program at any point.\n")

    frame = helpers.get_large_csv(input, delimiter)
    data = [
        helpers.get_heatmap_csv("output/IDs_changed_0-1.csv", delimiter = delimiter),
        helpers.get_heatmap_csv("output/IDs_changed_0-2.csv", delimiter = delimiter),
        ]

    # TODO: store this variable in a .csv file 
    to_print = [
        {'phys': 1, 'part': 1, 'view': 'N', 'cond': [0], 'data': 1 },
        {'phys': 2, 'part': 1, 'view': 'N', 'cond': [0], 'data': 1 },
        {'phys': 3, 'part': 1, 'view': 'N', 'cond': [0], 'data': 1 },
        {'phys': 4, 'part': 1, 'view': 'N', 'cond': [0], 'data': 1 },
        {'phys': 5, 'part': 1, 'view': 'N', 'cond': [0], 'data': 1 },
        {'phys': 6, 'part': 1, 'view': 'N', 'cond': [0], 'data': 1 },

        {'phys': 1, 'part': 1, 'view': 'N', 'cond': [0], 'data': 2 },
        {'phys': 2, 'part': 1, 'view': 'N', 'cond': [0], 'data': 2 },
        {'phys': 3, 'part': 1, 'view': 'N', 'cond': [0], 'data': 2 },
        {'phys': 4, 'part': 1, 'view': 'N', 'cond': [0], 'data': 2 },
        {'phys': 5, 'part': 1, 'view': 'N', 'cond': [0], 'data': 2 },
        {'phys': 6, 'part': 1, 'view': 'N', 'cond': [0], 'data': 2 },
    ]


    interactions.printvis(frame=frame, tasks=to_print, data=data)

    click.echo(f"\nTill next time!\n")


@click.command()
@click.option("--delimiter", "-d", default=";", help="Delimiter used in your csv files. Default is ';'")
@click.option("--input", "-i", default="output/combined.csv", help="The location of the large .csv file compiled by collect(). Default is 'output/combined.csv'")
def print(input: str, delimiter: str) -> None:
    click.echo(f"Press 'control+c' to abort this program at any point.\n")

    frame = helpers.get_large_csv(input, delimiter)

    # TODO: store this variable in a .csv file
    to_print = [
        {'phys': 1, 'part': 1, 'view': 'N', 'cond': [0], 'baseline': True },
        {'phys': 2, 'part': 1, 'view': 'N', 'cond': [0], 'baseline': True },
        {'phys': 3, 'part': 1, 'view': 'N', 'cond': [0], 'baseline': True },
        {'phys': 4, 'part': 1, 'view': 'N', 'cond': [0], 'baseline': True },
        {'phys': 5, 'part': 1, 'view': 'N', 'cond': [0], 'baseline': True },
        {'phys': 6, 'part': 1, 'view': 'N', 'cond': [0], 'baseline': True },

        {'phys': 1, 'part': 1, 'view': 'N', 'cond': [0] },
        {'phys': 1, 'part': 8, 'view': 'N', 'cond': [0] },
        {'phys': 1, 'part': 16, 'view': 'N', 'cond': [0] },
        {'phys': 1, 'part': 8, 'view': 'N', 'cond': [0,2] },
        {'phys': 1, 'part': 8, 'view': 'E', 'cond': [0,2] },
        {'phys': 1, 'part': 8, 'view': 'S', 'cond': [0,2] },
        {'phys': 1, 'part': 8, 'view': 'W', 'cond': [0,2] },
        {'phys': 1, 'part': 11, 'view': 'N', 'cond': [0,2] },
        {'phys': 1, 'part': 16, 'view': 'N', 'cond': [0,2] },
        {'phys': 1, 'part': 4, 'view': 'E', 'cond': [0,2] },
        {'phys': 1, 'part': 19, 'view': 'N', 'cond': [0,1] },
        {'phys': 1, 'part': 19, 'view': 'N', 'cond': [0,2] },

        {'phys': 2, 'part': 1, 'view': 'N', 'cond': [0] },
        {'phys': 2, 'part': 2, 'view': 'N', 'cond': [0] },
        {'phys': 2, 'part': 11, 'view': 'E', 'cond': [0,2] },
        {'phys': 2, 'part': 9, 'view': 'E', 'cond': [0,2] },
        {'phys': 2, 'part': 2, 'view': 'N', 'cond': [0,2] },
        {'phys': 2, 'part': 13, 'view': 'S', 'cond': [0,1] },
        {'phys': 2, 'part': 7, 'view': 'N', 'cond': [0,2] },
        {'phys': 2, 'part': 15, 'view': 'S', 'cond': [0,2] },
        {'phys': 2, 'part': 4, 'view': 'E', 'cond': [0,2] },

        {'phys': 3, 'part': 4, 'view': 'N', 'cond': [0] },
        {'phys': 3, 'part': 14, 'view': 'N', 'cond': [0] },
        {'phys': 3, 'part': 1, 'view': 'N', 'cond': [0] },
        {'phys': 3, 'part': 1, 'view': 'N', 'cond': [0] },
        {'phys': 3, 'part': 14, 'view': 'E', 'cond': [0,1] },
        {'phys': 3, 'part': 14, 'view': 'E', 'cond': [0,2] },
        {'phys': 3, 'part': 1, 'view': 'N', 'cond': [0,2] },
        {'phys': 3, 'part': 7, 'view': 'E', 'cond': [0,2] },
        {'phys': 3, 'part': 8, 'view': 'E', 'cond': [0,2] },
        {'phys': 3, 'part': 12, 'view': 'N', 'cond': [0,1] },
        {'phys': 3, 'part': 12, 'view': 'N', 'cond': [0,2] },
        {'phys': 3, 'part': 7, 'view': 'E', 'cond': [0] },
        {'phys': 3, 'part': 10, 'view': 'E', 'cond': [0] },

        {'phys': 4, 'part': 4, 'view': 'N', 'cond': [0] },
        {'phys': 4, 'part': 1, 'view': 'N', 'cond': [0] },
        {'phys': 4, 'part': 3, 'view': 'N', 'cond': [0] },
        {'phys': 4, 'part': 2, 'view': 'N', 'cond': [0] },
        {'phys': 4, 'part': 5, 'view': 'N', 'cond': [0,1] },
        {'phys': 4, 'part': 16, 'view': 'S', 'cond': [0,1] },
        {'phys': 4, 'part': 3, 'view': 'N', 'cond': [0,1] },
        {'phys': 4, 'part': 6, 'view': 'N', 'cond': [0,1] },
        {'phys': 4, 'part': 10, 'view': 'N', 'cond': [0,1] },
        {'phys': 4, 'part': 17, 'view': 'N', 'cond': [0,2] },

        {'phys': 5, 'part': 1, 'view': 'N', 'cond': [0] },
        {'phys': 5, 'part': 8, 'view': 'N', 'cond': [0,1] },
        {'phys': 5, 'part': 8, 'view': 'N', 'cond': [0,2] },
        {'phys': 5, 'part': 14, 'view': 'N', 'cond': [0,2] },
        {'phys': 5, 'part': 6, 'view': 'E', 'cond': [0,2] },
        {'phys': 5, 'part': 6, 'view': 'E', 'cond': [0] },

        {'phys': 6, 'part': 1, 'view': 'N', 'cond': [0] },
        {'phys': 6, 'part': 7, 'view': 'N', 'cond': [0] },
        {'phys': 6, 'part': 3, 'view': 'N', 'cond': [0,2] },
        {'phys': 6, 'part': 4, 'view': 'S', 'cond': [0,2] },
        {'phys': 6, 'part': 8, 'view': 'W', 'cond': [0,2] },
        {'phys': 6, 'part': 14, 'view': 'S', 'cond': [0,1] },
        {'phys': 6, 'part': 9, 'view': 'N', 'cond': [0,1] },
        {'phys': 6, 'part': 15, 'view': 'N', 'cond': [0,2] },
        {'phys': 6, 'part': 7, 'view': 'E', 'cond': [0,2] },
        {'phys': 6, 'part': 2, 'view': 'S', 'cond': [0,2] },
        {'phys': 6, 'part': 7, 'view': 'S', 'cond': [0,2] },
        {'phys': 6, 'part': 15, 'view': 'S', 'cond': [0,2] },
        {'phys': 6, 'part': 5, 'view': 'N', 'cond': [0,1] },
        {'phys': 6, 'part': 15, 'view': 'N', 'cond': [0,1] },
        {'phys': 6, 'part': 15, 'view': 'N', 'cond': [0,2] },
        {'phys': 6, 'part': 11, 'view': 'N', 'cond': [0,1] },
        {'phys': 6, 'part': 16, 'view': 'W', 'cond': [0,1] },
        {'phys': 6, 'part': 16, 'view': 'W', 'cond': [0,2] },
    ]

    interactions.printvis(frame=frame, tasks=to_print)

    click.echo(f"\nTill next time!\n")


@click.command()
@click.option("--delimiter", "-d", default=";", help="Delimiter used in your csv files. Default is ';'")
@click.option("--input", "-i", default="input", help="The input location of the .csv files. Default is 'input'")
def collect(input: str, delimiter: str) -> None:
    click.echo(f"Press 'control+c' to abort this program at any point.\n")

    click.echo(f"Collecting Data from {input}")
    frame = interactions.generate_large_csv(input = input, output = 'output', delimiter = delimiter, save = True)
    click.echo(f"See the output/combined.csv for the combined result")


@click.command()
@click.option("--delimiter", "-d", default=";", help="Delimiter used in your csv files. Default is ';'")
@click.option("--input", "-i", default="output/combined.csv", help="The location of the large .csv file compiled by collect(). Default is 'output/combined.csv'")
def calc(input: str, delimiter: str) -> None:
    click.echo(f"Press 'control+c' to abort this program at any point.")

    click.echo(f"\nWhich calculation do you want to perform?\n")
    frame = helpers.get_large_csv(input, delimiter)
    # print(frame.info())

    repeat = True

    while repeat:
        repeat = False

        # get user input
        possible_functions = [x[0] for x in inspect.getmembers(maths, inspect.isfunction)]
        possible_functions.reverse()
        show_options = [str(i) + '. ' + x for i, x in enumerate(possible_functions, 1)]
        click.echo("\n".join(show_options) + "\n")

        chosen_function_nr = click.prompt("  Calulation", type=click.Choice([str(x) for x in range(1,len(possible_functions)+1)]))
        chosen_function = possible_functions[int(chosen_function_nr)-1]

        # display result, or err
        try:
            click.echo(f"\nRunning '{chosen_function}':\n")

            # run the chosen method, with options: getattr(maths, chosen_function)(**options)
            result = getattr(maths, chosen_function)(frame)
            click.echo(result)

            click.echo(f"\nFinished calculation.\n")
        except Exception as e:
            print(f"An error occured in the {chosen_function} calculation: {e}")

        # possibly visualise another one
        repeat = False
        if click.confirm('Would you like to conduct another calculation?'):
            repeat = True


    click.echo(f"\nTill next time!\n")
