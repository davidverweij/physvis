import pandas as pd
from tqdm import tqdm

# looks like: ['participant','physicalisation','orientation','condition','cube', 'h', 'o', 'g', 'x', 'y']
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
    def _chosen_cubes_to_change(x):
        x = x.loc(axis=1)['o','x','y']  # drop other columns
        diff = x.iloc[0] == x.iloc[2]   # compare elements rows 1 and 3
        return pd.Series(
            [1 if not x.iloc[0].equals(x.iloc[1]) else 0,
             1 if not x.iloc[0].equals(x.iloc[2]) else 0,
             1 if not x.iloc[1].equals(x.iloc[2]) else 0,
             1 if not x.iloc[0].equals(x.iloc[1]) and     x.iloc[1].equals(x.iloc[2]) else 0,
             1 if     x.iloc[0].equals(x.iloc[1]) and not x.iloc[1].equals(x.iloc[2]) else 0,
             1 if not x.iloc[0].equals(x.iloc[1]) and not x.iloc[1].equals(x.iloc[2]) else 0,

             # 1 if diff.all() else 0,
             # 1 if diff['o'] and not diff['x','y'].all() else 0,
             # 1 if diff['x','y'].all() and not diff['o'] else 0,
             ],
            index=[
                 'sum_changes_0_1',
                 'sum_change_0_2',
                 'sum_changes_1_2',
                 'only_changes_0_1',
                 'only_changes_1_2',
                 'both_changes_0_1_2',

                 # 'changes_0_2_all_o_x_y',
                 # 'changes_0_2_only_o_no_x_y',
                 # 'changes_0_2_only_x_y_no_o'

                 ])

    conditions = frame.groupby(['physicalisation', 'participant', 'orientation', 'cube'])
    cubes_changed = conditions.progress_apply(_chosen_cubes_to_change)
    summed = cubes_changed.groupby([nc[1], nc[4]]).sum()

    for column in summed:
        subresult = summed[column].unstack()
        print(subresult)
        subresult.to_csv(path_or_buf=helpers.create_output_folder('output') / f"conditions_ID_{column}.csv", sep=';', header=True)



'''
def move_consistency() -> None:
    pass

def cluster_change_type() -> None:
    pass
'''
