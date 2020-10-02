from pathlib import Path
import re

import pandas as pd
from tqdm import tqdm
import plotly.graph_objects as plot

from . import helpers



def printvis(frame: pd.DataFrame, tasks: list, data:list = None) -> None:
    """save 3D renderings of Data series
    Args:
        frame: the data frame storing data to be rendered
    Returns:
        nothing
    """

    print("Generating visuals for")

    # colors = ['Greys','YlGnBu','Greens','YlOrRd','Bluered','RdBu','Reds','Blues','Picnic','Rainbow','Portland','Jet','Hot','Blackbody','Earth','Electric','Viridis','Cividis']
    # angles = [[17,15],[15,-17],[-17,-15],[-15,17]]
    # angles = [[17,15]]

    phys_angles = {
        1: [15,  -17],
        2: [15, -17],
        3: [17,   15],
        4: [17,   15],
        5: [-15, 17],
        6: [-15, 17]
    }

    colorscale = [
        [0, 'rgb(29,123,180)'],
        [.25, 'rgb(57,177,135)'],
        [.5, 'rgb(241,206,28)'],
        [.75, 'rgb(238,116,73)'],
        [1, 'rgb(37,55,123)']
    ]

    datacolorscale = [
        [0, 'rgb(255,255,255)'],
        [1, 'rgb(255,0,0)']
    ]

    for task in tasks:

        # get the specific index from the dataframe
        query = f"physicalisation == {task['phys']} and participant == {task['part']} and orientation == '{task['view']}'"
        print(' - '+ query)

        # conditions
        remove_cond = [x for x in [0,1,2] if x not in task['cond']]

        target = frame.query(query).drop(remove_cond, level='condition')

        max_group = int(target['g'].max())
        camera = phys_angles[task['phys']]

        # eight x, y, and z coordinates form a cube
        # reference: https://plotly.com/python/reference/isosurface/



        fig= plot.Figure(
            layout_title_text=""
        )

        # numbers hovering over cubes
        total_cond = len(task['cond'])
        count = 0

        for condition, all_cubes in target.groupby('condition'):
            count += 1
            annotations = []

            if 'data' in task:
                #  max_value = data[task['data']-1].loc[task['phys']].max();
                max_value = data[task['data']-1].max().max();
                print(f"max = {max_value}")

            for row in all_cubes.itertuples():
                cubeID = row.Index[-1]
                if 'data' in task:
                    cubevalue = data[task['data']-1].loc[task['phys']][int(cubeID)-1]
                c = {
                    # coordinates
                    'x' : row.x,
                    'y' : row.y,
                    'z' : 1,
                    # half widths
                    'wx' : .45,
                    'wy' : .45,
                    # heigth
                    'wz' : .9,
                }
                # overrule widths based on orientation
                # note that a orientation in y, adds width to the 'x' direction - and vise versa
                c['w' + row.o] = row.h / (1 if row.o == 'z' else 2)

                fig.add_trace(
                    plot.Isosurface(
                        x=[c['x']-c['wy'], c['x']-c['wy'], c['x']-c['wy'], c['x']-c['wy'], c['x']+c['wy'], c['x']+c['wy'], c['x']+c['wy'], c['x']+c['wy']],
                        y=[c['y']+c['wx'], c['y']-c['wx'], c['y']+c['wx'], c['y']-c['wx'], c['y']+c['wx'], c['y']-c['wx'], c['y']+c['wx'], c['y']-c['wx']],
                        z=[c['wz'],        c['wz'],        0,              0,              c['wz'],        c['wz'],        0,               0],
                        value=[0 if 'baseline' in task
                               else ((-4 if cubevalue == 0 else cubevalue) if 'data' in task else row.g-1)
                               ]*8,
                        hoverinfo="none",
                        showscale=False,
                        opacity=(.2 if count < total_cond else 1),
                        contour=dict(
                            show=True
                            ),
                        isomin=0 if not 'data' in task else -4,       # remove the 'dark blue' harder to see
                        isomax=4 if not 'data' in task else max_value,
                        colorscale=datacolorscale if 'data' in task else colorscale,
                        lighting = dict(
                            diffuse=.9,
                            ambient=.5,
                        ),
                        surface=dict(count=3, fill=0.7, pattern='odd'),
                        ),
                )

                if 'data' in task:
                    if cubevalue > 0:
                        annotations.append(dict(
                            x=c['x'],
                            y=c['y'],
                            z=c['wz'] + 1,
                            text=' ' + str(cubevalue) + ' ',
                            showarrow=False,
                            # bgcolor="rgba(255,255,255,.7)",
                            font=dict(
                                color="black",
                                size=20
                            ),
                            )
                        )

        fig.update_layout(
            margin=dict(l=0, r=0, t=0, b=0),

            scene = dict(
                aspectratio=dict(
                 x=20,
                 y=20,
                 z=5,
                ),
                xaxis = dict(
                    showticklabels=False,
                    # showaxeslabels=False,
                    nticks=40,
                    range=[0,20],
                    showbackground=False,
                    visible=True,
                    title = dict(text=""),
                    ),
                yaxis = dict(
                    showticklabels=False,
                    # showaxeslabels=False,
                    nticks=40,
                    range=[0,20],
                    showbackground=False,
                    visible=True,
                    title = dict(text=""),
                    ),
                zaxis = dict(
                    showticklabels=False,
                    showaxeslabels=False,
                    nticks=5,
                    range=[0,5],
                    backgroundcolor="rgb(245,245,245)",
                    title = dict(text=""),
                    ),
                annotations = annotations,
                camera = dict(
                    up=dict(x=0, y=0, z=1),
                    # center=dict(x=-.4, y=-.4, z=-.7),
                    # eye=dict(x=.7, y=.6, z=-.1),

                    # This one worked well for non orthographic!
                    # center=dict(x=3, y=2, z=0),
                    # eye=dict(x=13, y=10, z=10),

                    #  with perspective
                    center=dict(x=0, y=0, z=-5),
                    eye=dict(x=camera[0], y=camera[1], z=16),

                    # orthographic
                    # projection = dict(
                    #     type="orthographic"
                    # ),
                    # center=dict(x=3, y=2, z=0),
                    # eye=dict(x=35, y=30, z=30),
                )
            ),
        )


        # fig.show()
        if 'baseline' in task:
            fig.write_image(f"images/BASELINE physicalisation == {task['phys']}.jpg", width=600, height=400, scale=5)
        elif 'data' in task:
            fig.write_image(f"images/HEATMAP physicalisation == {task['phys']} and conditiond == 0-{task['data']}.jpg", width=600, height=400, scale=5)
        else:
            fig.write_image(f"images/{query} and conditions == {task['cond']}.jpg", width=600, height=400, scale=5)



def display(frame: pd.DataFrame, participant: str, condition: str, orientation: str, physicalisation: str) -> None:
    """Create 3D renderings of Data series
    Args:
        frame: the data frame storing data to be rendered
    Returns:
        nothing
    """
    situation = f"Phys{physicalisation}_P{participant}_Condition{condition}_{orientation}"

    if not isinstance(frame, pd.DataFrame):
        raise TypeError(f"Argument dataframe must be of type pandas DataFrame, not {type(save)}")
    else:
        # get the specific index from the dataframe
        vis = frame.loc[(int(participant), int(physicalisation), orientation, int(condition))]
        print(vis)

        # eight x, y, and z coordinates form a cube
        # reference: https://plotly.com/python/reference/isosurface/

        fig= plot.Figure(
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
                plot.Isosurface(
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

        # fig.write_html(f"output/{situation}.html")
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

    for i, filename in enumerate(tqdm(all_files)):
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
            df2 = pd.DataFrame([filename.stem.split(sep='_')]*len(df1.index) ,columns=helpers.naming_columns[:4])

            # remove the 'P' before participant
            df2['participant']= df2['participant'].str.lstrip('P')

            # prepend the data from the file name to each row of the data
            df_joined = pd.concat([df2,df1],axis=1)

            # adjust header names for easy reading
            df_joined.columns = helpers.naming_columns
            # add to bigger dataframe
            li.append(df_joined)

        except Exception as e:
            print(f"An '{e}' error occured in one of the files: {filename}")


    if len(li) > 0:
        # combine all arrays into a DataFrame, and convert to numbers where possible
        frame = pd.concat(li, axis=0, ignore_index=True).set_index(helpers.naming_columns[:5]).sort_index()
        frame = frame.apply(pd.to_numeric, errors='ignore')

        # correct the .5 x .5 offset in the data
        frame.x = frame.x - .5
        frame.y = frame.y - .5

        frame.sort_index()

        # fill in the missing values, following https://stackoverflow.com/a/41274715/7053198
        # creates floats, but ensures presence of all rows/columns
        new_index = pd.MultiIndex.from_product(frame.index.levels)
        frame = frame.reindex(new_index)

        print(frame.info())

        if save:
            frame.to_csv(path_or_buf=helpers.create_output_folder(output) / 'combined.csv', sep=';', header=True)
