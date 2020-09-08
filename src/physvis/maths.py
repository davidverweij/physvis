import pandas as pd
from tqdm import tqdm

# looks like: ['participant','physicalisation','orientation','condition','cube', 'h', 'o', 'g', 'x', 'y']
from .helpers import naming_columns as nc


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
    def _change_at_cond_1(x):
        uniques = x.drop_duplicates(subset=x.columns.difference([nc[3]]))

        # 1. check if there are 3 rows, else - cube was removed = change!
        # 2. check if any of the columns are not the same (ignore cluster?)

        # if more than 1 rows are left, some change happend!
        if len(uniques) > 1:
            # if condition '1' is still left, the cube was changed at condition 1
            if any(uniques.index.isin([2],level=nc[3])):
                return True
        # else, nothing happened
        return False

    # new plan, check if change and add as a column to the dataframe to keep the info


    # looks like: ['participant','physicalisation','orientation','condition','cube', 'h', 'o', 'g', 'x', 'y']
    result = frame.groupby([nc[1], nc[0], nc[2], nc[4]]).progress_apply(_change_at_cond_1).value_counts(subset=[nc[1],nc[4]], sort=False)
    with pd.option_context('display.max_rows', None, 'display.max_columns', None):
        print(result)

    '''
    # arrange data for each phys, for each participant, for each orientation
    for name, group in frame.groupby([nc[1], nc[0], nc[2]):
        # we are left with groups showing cube data over the three conditions

        for subname, subgroup in group.groupby([nc[4]]):
            # ignoring the condition, remove duplicates
            subgroup = subgroup.drop_duplicates(subset=subgroup.columns.difference([nc[3]]))
            if len(subgroup) > 1:
                print(subgroup)
                print(len(subgroup))
            # print(subgroup.apply(lambda s: len(s.unique()) > 1))

    '''



'''
def move_consistency() -> None:
    pass

def cluster_change_type() -> None:
    pass
'''
