from pathlib import Path
import re

import pandas as pd


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


def convert(
    input: str = "input", output: str = "output", delimiter: str = ";"
) -> None:
    print("Getting .csv data files ...")

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

        # prepend the filname data to all rows
        df2 = pd.DataFrame( [filename.stem.split(sep='_')]*len(df1.index) ,columns=naming_columns)

        # remove the 'P' before participant
        df2['particip']= df2['particip'].str.lstrip('P')


        li.append(pd.concat([df2,df1],axis=1))

    frame = pd.concat(li, axis=0, ignore_index=True)
    print(frame.info());
    frame.to_csv(path_or_buf=create_output_folder(output) / 'combined.csv', sep=';', header=True)
