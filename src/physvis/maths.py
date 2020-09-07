import pandas as pd

from .helpers import naming_columns as nc

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
    def _custom_calc(x):
        pass

    for name, group in frame.groupby(nc[0:2]):
        group.apply(_custom_calc)




'''
def move_consistency() -> None:
    pass

def cluster_change_type() -> None:
    pass
'''
