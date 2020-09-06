from pathlib import Path
import re

import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots


naming_columns = ['participant','physicalisation','orientation','condition','cube', 'h', 'o', 'g', 'x', 'y']


def create_output_folder(output_path: str) -> Path:
    """Creates a path to store output data if it does not exists.
    Args:
        path: the path from user in any format (relative, absolute, etc.)
    Returns:
        A path to store output data.
    """
    path = Path(output_path)
    if not path.exists():
        path.mkdir(parents=True, exist_ok=True)
    return path

def get_large_csv(input_path: str, delimiter: str = ";") -> pd.DataFrame:
    """Get the large .csv as a DataFrame (must have created it first using collect())
    Args:
        path: the path from user in any format (relative, absolute, etc.)
    Returns:
        A pandas dataframe
    """
    frame = pd.read_csv(input_path, index_col=naming_columns[:5], header=0, delimiter=delimiter, keep_default_na=False)
    frame.sort_index()
    return frame

def display(frame: pd.DataFrame, participant: str, condition: str, orientation: str, physicalisation: str) -> None:
    """Create 3D renderings of Data series
    Args:
        frame: the data frame storing data to be rendered
    Returns:
        nothing
    """
    situation = f"Phys {physicalisation}, Participant {participant}, Condition {condition}, Orientation {orientation}"

    if not isinstance(frame, pd.DataFrame):
        raise TypeError(f"Argument dataframe must be of type pandas DataFrame, not {type(save)}")
    else:
        # get the specific index from the datafra,e
        vis = frame.loc[(int(participant), int(physicalisation), orientation, int(condition))]
        print(vis)

        # eight x, y, and z coordinates form a cube
        # reference: https://plotly.com/python/reference/isosurface/

        fig= go.Figure(
            layout_title_text=situation
        )

        # numbers hovering over cubes
        annotations = []

        for row in vis.itertuples():
            c = {
                # coordinates
                'x' : row.x,
                'y' : row.y,
                'z' : 1,
                # half widths
                'wx' : .5,
                'wy' : .5,
                # heigth
                'wz' : 1,
            }
            # overrule widths based on orientation
            # note that a orientation in y, adds width to the 'x' direction - and vise versa
            c['w' + row.o] = row.h / (1 if row.o == 'z' else 2)

            fig.add_trace(
                go.Isosurface(
                    x=[c['x']-c['wy'], c['x']-c['wy'], c['x']-c['wy'], c['x']-c['wy'], c['x']+c['wy'], c['x']+c['wy'], c['x']+c['wy'], c['x']+c['wy']],
                    y=[c['y']+c['wx'], c['y']-c['wx'], c['y']+c['wx'], c['y']-c['wx'], c['y']+c['wx'], c['y']-c['wx'], c['y']+c['wx'], c['y']-c['wx']],
                    z=[c['wz'],     c['wz'],     0,        0,        c['wz'],     c['wz'],     0,        0],
                    value=[row.g]*8,
                    hoverinfo="none",
                    showscale=False,
                    opacity=1.0,
                    contour=dict(
                        show=True
                        ),
                    isomin=1,
                    isomax=5,
                    ),
            )

            annotations.append(dict(
                x=c['x'],
                y=c['y'],
                z=c['wz'] + .5,
                text=str(row.Index),
                showarrow=False,
                bgcolor="rgba(255,255,255,.7)",
                font=dict(
                    color="black",
                    size=12
                ),
                )
            )

        fig.update_layout(
            scene_aspectmode='cube',
            scene = dict(
                xaxis = dict(nticks=40, range=[0,20],showbackground=False),
                yaxis = dict(nticks=40, range=[0,20],showbackground=False),
                zaxis = dict(nticks=4, range=[0,20],),
                xaxis_title='X AXIS TITLE',
                yaxis_title='Y AXIS TITLE',
                zaxis_title='Z AXIS TITLE',
                annotations = annotations,
            ),
            scene_camera = dict(
                eye=dict(x=0., y=2.5, z=0.)
            ),
        )

        fig.show()


def generate_large_csv(input: str = "input", output: str = "output", delimiter: str = ";", save: bool = False ) -> None:
    """Concatenates all .csv files into a pandas MultiIndex Frame (i.e. Table).
    Performs minor tweaks to the incoming data, e.g. coordinates and naming scheme
    Args:
        input: folder containing all .csv files
        output: output folder to store any results in
        delimiter: input files delimiter, defaults to ';'
        save: if true, saves all concatenated .csv as a .csv in the output folder
    Returns:
        A dataframe with all concatenated input .csv data
    """

    # find all .csv files in the input folder recursively
    all_files = list(Path(input).rglob('*.csv'));

    li = []

    for filename in all_files:
        ''' split the filename into columns
        Expecting filesnames in the format PX_0_N_0
            Participant = [P1-P20]
            Phys = [1-6]
            Orientation = [N, E, S, W]
            Condition = [0-2]
                0 = clustering
                1 = single move
                2 = multiple moves
        '''
        df1 = pd.read_csv(filename, index_col=None, header=0, delimiter=delimiter, keep_default_na=False)

        # removed empty (or in our case unnamed) columns
        df1 = df1.loc[:, ~df1.columns.str.contains('^Unnamed')]

        try:
            # split the coordinates in two columns, and remove original
            df1[['cube_x','cube_y']] = df1['coordinates'].str.split(pat=',',expand=True)
            df1 = df1.drop(columns=['coordinates'])

            # multiply the filname data to match the amount of rows
            df2 = pd.DataFrame([filename.stem.split(sep='_')]*len(df1.index) ,columns=naming_columns[:4])

            # remove the 'P' before participant
            df2['participant']= df2['participant'].str.lstrip('P')

            # prepend the data from the file name to each row of the data
            df_joined = pd.concat([df2,df1],axis=1)

            # adjust header names for easy reading
            df_joined.columns = naming_columns
            # add to bigger dataframe
            li.append(df_joined)

        except Exception as e:
            print(f"An '{e}' error occured in one of the files: {filename}")


    if len(li) > 0:
        # combine all arrays into a DataFrame, and convert to numbers where possible
        frame = pd.concat(li, axis=0, ignore_index=True).set_index(naming_columns[:5]).sort_index()
        frame = frame.apply(pd.to_numeric, errors='ignore')

        # correct the .5 x .5 offset in the data
        frame.x = frame.x - .5
        frame.y = frame.y - .5

        frame.sort_index()

        print(frame.info())

        if save:
            frame.to_csv(path_or_buf=create_output_folder(output) / 'combined.csv', sep=';', header=True)
