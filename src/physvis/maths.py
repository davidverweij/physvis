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
    def _change_at_cond_1(x):
        # prep for 2. remove any duplicates based on orientation, x or y changes
        uniques = x.drop_duplicates(subset=['o','x','y'])

        yes_change = pd.Series([1], index=['change_at_cond_1'])
        no_change = pd.Series([0], index=['change_at_cond_1'])

        # 1. if there are less than 3 rows in the original, a cube was removed
        if (len(x) < 3):
            # if the condition '1' is not present, it was removed then = change
            if not any(x.index.isin([1],level=nc[3])):
                return 1

        # 2. or if, when duplicates are removed, multiple are present, a change occured
        elif (len(uniques) > 1):

            # if condition '1' is still left, the cube was changed at condition
            if any(uniques.index.isin([1],level=nc[3])):
                return 1

        # nothing happened, return not a number (will be filtered)
        return 0

    frame.to_csv(path_or_buf=helpers.create_output_folder('output') / 'test_save_changes_0_1.csv', sep=';', header=True)

    # looks like: ['participant','physicalisation','orientation','condition','cube', 'h', 'o', 'g', 'x', 'y']
    result = frame.groupby([nc[1], nc[0], nc[2], nc[4]]).progress_apply(_change_at_cond_1)
    summed = result.groupby([nc[1], nc[4]]).sum()
    unstacked = summed.unstack()
    with pd.option_context('display.max_rows', None, 'display.max_columns', None):
        print(summed)
        print(unstacked)


    unstacked.to_csv(path_or_buf=helpers.create_output_folder('output') / 'changes_0_1_unstacked.csv', sep=';', header=True)
    summed.to_csv(path_or_buf=helpers.create_output_folder('output') / 'changes_0_1.csv', sep=';', header=True)



'''
def move_consistency() -> None:
    pass

def cluster_change_type() -> None:
    pass
'''
