from pathlib import Path
import re

import pandas as pd
import plotly.graph_objects as go


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


def collect(input: str = "input", output: str = "output", delimiter: str = ";", save: bool = False, verbose: bool = False) -> pd.DataFrame:
    """Concatenates all .csv files into a pandas DataFrame (i.e. Table).
    Args:
        input: folder containing all .csv files
        output: output folder to store any results in
        delimiter: input files delimiter, defaults to ';'
        save: if true, saves all concatenated .csv as a .csv in the output folder
    Returns:
        A dataframe with all concatenated input .csv data
    """

    all_files = list(Path(input).glob('*.csv'));

    li = []
    naming_columns = ['particip','phys','partic_orien','cond']

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

        # split the coordinates in two columns, and remove original
        df1[['cube_x','cube_y']] = df1['coordinates'].str.split(pat=',',expand=True)
        df1 = df1.drop(columns=['coordinates'])

        # multiply the filname data to match the amount of rows
        df2 = pd.DataFrame( [filename.stem.split(sep='_')]*len(df1.index) ,columns=naming_columns)

        # remove the 'P' before participant
        df2['particip']= df2['particip'].str.lstrip('P')

        # prepend the data from the file name to each row of the data
        li.append(pd.concat([df2,df1],axis=1))

    # combine all arrays into a DataFrame, and convert to numbers where possible
    frame = pd.concat(li, axis=0, ignore_index=True)
    frame = frame.apply(pd.to_numeric, errors='ignore')

    if verbose:
        print(frame.info());
    if save:
        frame.to_csv(path_or_buf=create_output_folder(output) / 'combined.csv', sep=';', header=True)

    # return the object for further handeling
    return frame


def display(frame: pd.DataFrame, rows: [int] = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]) -> None:
    """Create 3D renderings of Data series
    Args:
        frame: the data frame storing data to be rendered
    Returns:
        nothing
    """
    if not isinstance(frame, pd.DataFrame):
        raise TypeError(f"Argument dataframe must be of type pandas DataFrame, not {type(save)}")
    else:
        # eight x, y, and z coordinates form a cube
        # reference: https://plotly.com/python/reference/isosurface/
        fig= go.Figure(
            layout_title_text="Graph Title Here",
        )

        count = 0;

        # for each row we want to display (defaults to the first)
        for row in rows:
            count+=1
            panda_row = frame.iloc[row]
            c = {
                # coordinates
                'x' : panda_row.loc['cube_x']-1.5,
                'y' : panda_row.loc['cube_y']-1.5,
                'z' : 1,
                # half widths
                'wy' : .5,
                'wx' : .5,
                # heigth
                'wz' : 1,
            }
            orientation = panda_row.loc['atom_orien']

            # overrule widths based on orientation
            c['w' + orientation] = panda_row.loc['cube_height'] / (1 if orientation == 'z' else 2)

            fig.add_trace(
                go.Isosurface(
                    x=[c['x']-c['wx'], c['x']-c['wx'], c['x']-c['wx'], c['x']-c['wx'], c['x']+c['wx'], c['x']+c['wx'], c['x']+c['wx'], c['x']+c['wx']],
                    y=[c['y']+c['wy'], c['y']-c['wy'], c['y']+c['wy'], c['y']-c['wy'], c['y']+c['wy'], c['y']-c['wy'], c['y']+c['wy'], c['y']-c['wy']],
                    z=[c['wz'],     c['wz'],     0,        0,        c['wz'],     c['wz'],     0,        0],
                    value=[1,1,1,1,1,1,1,1],
                    text="cube",
                    hoverinfo="skip",
                    showscale=False,
                    ),
            )

        # update layout of the graphs
        fig.update_layout(
            scene = dict(
                xaxis = dict(nticks=40, range=[0,20],showbackground=False),
                yaxis = dict(nticks=40, range=[0,20],showbackground=False),
                zaxis = dict(nticks=4, range=[0,20],),
                xaxis_title='X AXIS TITLE',
                yaxis_title='Y AXIS TITLE',
                zaxis_title='Z AXIS TITLE',
            ),
            scene_camera = dict(
                eye=dict(x=0., y=2.5, z=0.)
            ),

        )

        print(f"I counted {count} cubes")

        fig.show()
