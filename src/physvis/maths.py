import numpy as np

import pandas as pd
from tqdm import tqdm
import plotly.express as px

from .helpers import naming_columns as nc
from . import helpers


# initiate tqdm pandas methods
tqdm.pandas()

def changes_total_cubes(frame: pd.DataFrame) -> None:
    """Calculates various stats about the different moves participants made
    For 'standard' stats, see https://pandas.pydata.org/pandas-docs/stable/user_guide/groupby.html#aggregation
    Here, we use our own aggregation method, see https://pandas.pydata.org/pandas-docs/stable/user_guide/groupby.html#flexible-apply
    Args:
        frame: the data frame storing data to be rendered
    Returns:
        nothing
    """

    # method local to this method
    def _count_occurance_total_cube_changes(x):

        def _check_per_cube(sub_x):
            # return 1 if a change between row 2 and 0 occured, else 0
            sub_x = sub_x.loc(axis=1)['o','x','y']  # drop other columns

            return pd.Series(
                [1 if not sub_x.iloc[0].equals(sub_x.iloc[2]) else 0,],
                index=['changed'])

        x_checked = x.groupby(['cube']).apply(_check_per_cube)  # per cube (3 rows of condition 0,1,2) check if there are changed
        x_summed = x_checked.sum() # sum all the 1's over the cubed (i.e. how many were changed)
        return x_summed


    # columns look like: ['participant','physicalisation','orientation','condition','cube', 'h', 'o', 'g', 'x', 'y']

    # focus on each trial
    conditions = frame.groupby(['physicalisation', 'participant', 'orientation'])
    # calculate if changes occured and sum to how many, per trial
    cubes_changed = conditions.progress_apply(_count_occurance_total_cube_changes)
    # count occurance of summed moves (e.g. 2x 16 cubes, 1x 3 cubes, etc)
    change_occurance = cubes_changed.groupby('physicalisation')['changed'].value_counts(sort=False)
    # make counted changes the header, and fill in the gaps with 0
    change_occurance_table = change_occurance.unstack(level='changed', fill_value=0)
    # save to file
    change_occurance_table.to_csv(path_or_buf=helpers.create_output_folder('output') / f"count_if_change.csv", sep=';', header=True)

    return change_occurance_table


def IDs_cubes_moved(frame: pd.DataFrame) -> None:
    """
    Args:
        frame: the data frame storing data to be rendered
    Returns:
        nothing
    """

    # method local to this method
    def _chosen_cubes_to_change(x):
        x = x.loc(axis=1)['o','x','y']  # drop other columns

        return pd.Series(
            [1 if not x.iloc[0].equals(x.iloc[1]) else 0,
             1 if not x.iloc[0].equals(x.iloc[2]) else 0,
             ],
            index=[
                '0-1',
                '0-2',
                ])


    # columns look like: ['participant','physicalisation','orientation','condition','cube', 'h', 'o', 'g', 'x', 'y']

    # focus on each cube in each trial
    conditions = frame.groupby(['physicalisation', 'participant', 'orientation', 'cube'])
    # calculate if a cube was changed in the trial
    cubes_changed = conditions.progress_apply(_chosen_cubes_to_change)
    # give the new values a name
    # cubes_changed.columns.name = 'any_change_at'
    # stack the horizontal 'headers' of 'any_change_at' back into a column, to perform the sum()
    # cubes_changed = cubes_changed.stack()
    # name the newly calculated values
    # cubes_changed.name = '#_it_was_moved'
    # sum the changes per cube, per phys
    summed_per_cube = cubes_changed.groupby(['physicalisation', 'cube']).sum()
    print(summed_per_cube)

    for columnname in summed_per_cube:
        # put back the cube ID as headers
        tabular=summed_per_cube[columnname].unstack()
        # save to csv
        tabular.to_csv(path_or_buf=helpers.create_output_folder('output') / f"IDs_changed_{columnname}.csv", sep=';', header=True)

    return summed_per_cube.unstack()

    # plotting a grouped AND stacked bar chart: https://stackoverflow.com/questions/45055661/combine-grouped-and-stacked-bar-graph-in-r

def proximity_changes(frame: pd.DataFrame) -> None:
    """
    Internal proximity = the average distance of all cluster's cubes to its centroid
    Internal proximity = the average distance of all cluster's centroids to it's closest neighbouring cluster
    Args:
        frame: the data frame storing data to be rendered
    Returns:
        nothing
    """

    # method local to this method
    def _centroids_distances(x):

        def _check_per_group(group):

            def _check_per_condition(cond):
                # calculate the centroid
                centroid = cond.mean()
                # calculate mean distance to the centroid
                mean_distance = np.hypot((cond['x'] - centroid.x),(cond['y'] - centroid.y)).mean()

                return pd.Series([
                    centroid.values.tolist(),
                    mean_distance
                    ],index=['centroid', 'distance'])

            conditions = group.groupby(['condition']).apply(_check_per_condition)

            try:
                internal_incease = 1 if conditions.iloc[0]['distance'] < conditions.iloc[2]['distance'] else 0
                internal_decrease = 1 if conditions.iloc[0]['distance'] > conditions.iloc[2]['distance'] else 0

                return pd.Series(
                    [internal_incease,
                     internal_decrease
                     ],
                    index=['internal_increase', 'internal_decrease'])
            except Exception as e:
                print(f"error at {group.index}: {e}")

        # per group and per condition ...
        groups = x.groupby(['g'])[['x','y']].apply(_check_per_group)
        return groups



        # x_checked = x.groupby(['cube']).apply(_check_per_cube)  # per cube (3 rows of condition 0,1,2) check if there are changed
        # x_summed = x_checked.sum() # sum all the 1's over the cubed (i.e. how many were changed)
        # return x_summed
        return 1


    # columns look like: ['participant','physicalisation','orientation','condition','cube', 'h', 'o', 'g', 'x', 'y']

    # convert to numbers where possible
    frame = frame.apply(pd.to_numeric, errors='ignore')
    print(frame.info())

    # reset index, we need a different angle, we want to check the cubes, per condition,
    frame.reset_index(inplace=True)
    frame.set_index(['physicalisation', 'participant', 'orientation', 'g', 'condition', 'cube'], inplace=True)

    # per trial...
    conditions = frame.groupby(['physicalisation', 'participant', 'orientation'])
    clusters_change = conditions.progress_apply(_centroids_distances)
    print(clusters_change)


    # calculate changes then:

    # count occurance of summed moves (e.g. 2x 16 cubes, 1x 3 cubes, etc)
    change_occurance = clusters_change.groupby('physicalisation')['changed'].value_counts(sort=False)
    # make counted changes the header, and fill in the gaps with 0
    change_occurance_table = change_occurance.unstack(level='changed', fill_value=0)
    # save to file
    change_occurance_table.to_csv(path_or_buf=helpers.create_output_folder('output') / f"count_if_change.csv", sep=';', header=True)

    return change_occurance_table
