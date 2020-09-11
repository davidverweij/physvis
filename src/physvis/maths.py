import pandas as pd
from tqdm import tqdm
import plotly.express as px

from .helpers import naming_columns as nc
from . import helpers


# initiate tqdm pandas methods
tqdm.pandas()

def move_types_overall(frame: pd.DataFrame) -> None:
    """Calculates various stats about the different moves participants made
    For 'standard' stats, see https://pandas.pydata.org/pandas-docs/stable/user_guide/groupby.html#aggregation
    Here, we use our own aggregation method, see https://pandas.pydata.org/pandas-docs/stable/user_guide/groupby.html#flexible-apply
    Args:
        frame: the data frame storing data to be rendered
    Returns:
        nothing
    """

    # method local to this method
    def _check_changes(x):


        def _check_per_cube(sub_x):
            # return 1 if a change between row 2 and 0 occured, else 0
            sub_x = sub_x.loc(axis=1)['o','x','y']  # drop other columns

            return pd.Series(
                [1 if not sub_x.iloc[0].equals(sub_x.iloc[2]) else 0,],
                index=['changed'])

        x_checked = x.groupby(['cube']).apply(_check_per_cube)  # per cube (3 rows of condition 0,1,2) check if there are changed
        x_summed = x_checked.sum() # sum all the 1's over the cubed (i.e. how many were changed)
        return x_summed


        '''
        return pd.Series(
            [ 1 if not x.iloc[0].equals(x.iloc[2]) else 0,
             # 1 if not x.iloc[0].equals(x.iloc[1]) else 0,
             # 1 if not x.iloc[1].equals(x.iloc[2]) else 0,
             1 if not x.iloc[0].equals(x.iloc[1]) and     x.iloc[1].equals(x.iloc[2]) else 0,
             1 if     x.iloc[0].equals(x.iloc[1]) and not x.iloc[1].equals(x.iloc[2]) else 0,
             1 if not x.iloc[0].equals(x.iloc[1]) and not x.iloc[1].equals(x.iloc[2]) else 0,

             # 1 if diff.all() else 0,
             # 1 if diff['o'] and not diff['x','y'].all() else 0,
             # 1 if diff['x','y'].all() and not diff['o'] else 0,
             ],
            index=[
                 'total',
                 # 'sum_changes_0_1',
                 # 'sum_changes_1_2',
                 'only_0-1',
                 'only_1-2',
                 'both',

                 # 'changes_0_2_all_o_x_y',
                 # 'changes_0_2_only_o_no_x_y',
                 # 'changes_0_2_only_x_y_no_o'

                 ])
        '''

    # columns look like: ['participant','physicalisation','orientation','condition','cube', 'h', 'o', 'g', 'x', 'y']

    # focus on each trial
    conditions = frame.groupby(['physicalisation', 'participant', 'orientation'])
    # calculate if changes occured and sum to how many, per trial
    cubes_changed = conditions.progress_apply(_check_changes)
    # count occurance of summed moves (e.g. 2x 16 cubes, 1x 3 cubes, etc)
    change_occurance = cubes_changed.groupby('physicalisation')['changed'].value_counts(sort=False)
    # make counted changes the header, and fill in the gaps with 0
    change_occurance_table = change_occurance.unstack(level='changed', fill_value=0)
    # save to file  
    change_occurance_table.to_csv(path_or_buf=helpers.create_output_folder('output') / f"occurance_change.csv", sep=';', header=True)

    return change_occurance_table

    # plotting a grouped AND stacked bar chart: https://stackoverflow.com/questions/45055661/combine-grouped-and-stacked-bar-graph-in-r

    '''
    for column in summed_per_cube:
        subresult = summed_per_cube[column].unstack()
        print(subresult)
        subresult.to_csv(path_or_buf=helpers.create_output_folder('output') / f"conditions_ID_{column}.csv", sep=';', header=True)
    '''


'''
def move_consistency() -> None:
    pass

def cluster_change_type() -> None:
    pass
'''
