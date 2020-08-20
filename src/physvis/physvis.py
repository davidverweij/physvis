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


def collect(input: str = "input", output: str = "output", delimiter: str = ";", save: bool = False, verbose: bool = False) -> None:
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
