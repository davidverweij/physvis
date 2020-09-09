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
    def _chosen_cubes_to_change(x):
        x = x.loc(axis=1)['o','x','y']  # drop other columns
        diff = x.iloc[0] == x.iloc[2]   # compare elements rows 1 and 3


        # return pd.DataFrame({
        #     'Type_of_Change' : ['only_0-1','only_1-2','both'],
        #     'count': [
        #         1 if not x.iloc[0].equals(x.iloc[1]) and     x.iloc[1].equals(x.iloc[2]) else 0,
        #         1 if     x.iloc[0].equals(x.iloc[1]) and not x.iloc[1].equals(x.iloc[2]) else 0,
        #         1 if not x.iloc[0].equals(x.iloc[1]) and not x.iloc[1].equals(x.iloc[2]) else 0,
        #         ]
        # }).groupby('Type_of_Change')



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

    # ['participant','physicalisation','orientation','condition','cube', 'h', 'o', 'g', 'x', 'y']
    conditions = frame.groupby(['physicalisation', 'participant', 'orientation', 'cube'])
    cubes_changed = conditions.progress_apply(_chosen_cubes_to_change)
    cubes_changed.columns.name = 'any_change_at'
    cubes_changed = cubes_changed.stack()
    cubes_changed.name = 'moves'
    summed_per_cube = cubes_changed.groupby([nc[1], nc[4], 'any_change_at']).sum()
    tabular = summed_per_cube.reset_index().pivot(columns='cube', index=['physicalisation','any_change_at'])
    summed_per_cube.to_csv(path_or_buf=helpers.create_output_folder('output') / f"conditions_ID_change.csv", sep=';', header=True)
    tabular.to_csv(path_or_buf=helpers.create_output_folder('output') / f"conditions_ID_change_tabular.csv", sep=';', header=True)

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
