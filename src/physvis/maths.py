import numpy as np
from decimal import Decimal, ROUND_HALF_EVEN, DecimalException, InvalidOperation

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

def atomic_orientation_moved_occurance(frame: pd.DataFrame) -> None:
    # count any number of orientation changes > 0 as 1 in a trial
    return atomic_orientation_moved_summed(frame, flatten=True)

def atomic_orientation_moved_summed(frame: pd.DataFrame, flatten=False) -> None:
    """
    Args:
        frame: the data frame storing data to be rendered
    Returns:
        nothing
    """

    # method local to this method
    def _chosen_cubes_to_change(x):
        x = x.loc(axis=1)['o']  # drop other columns

        resultframe = pd.DataFrame({
            '0-1': {
                'xy->z' : 1 if x.iloc[0] in ('x','y') and x.iloc[1] in ('z') else 0,
                'z->xy' : 1 if x.iloc[0] in ('z') and x.iloc[1] in ('x','y') else 0,
                'x<->y' : 1 if (x.iloc[0] in ('x') and x.iloc[1] in ('y')) or (x.iloc[0] in ('y') and x.iloc[1] in ('x')) else 0,
            },
            '1-2': {
                'xy->z' : 1 if x.iloc[1] in ('x','y') and x.iloc[2] in ('z') else 0,
                'z->xy' : 1 if x.iloc[1] in ('z') and x.iloc[2] in ('x','y') else 0,
                'x<->y' : 1 if (x.iloc[1] in ('x') and x.iloc[2] in ('y')) or (x.iloc[1] in ('y') and x.iloc[2] in ('x')) else 0,
            },
            '0-2': {
                'xy->z' : 1 if x.iloc[0] in ('x','y') and x.iloc[2] in ('z') else 0,
                'z->xy' : 1 if x.iloc[0] in ('z') and x.iloc[2] in ('x','y') else 0,
                'x<->y' : 1 if (x.iloc[0] in ('x') and x.iloc[2] in ('y')) or (x.iloc[0] in ('y') and x.iloc[2] in ('x')) else 0,
            }

        })
        # give the subaxis a name
        resultframe.rename_axis(index="type", columns="phase", inplace=True)
        return resultframe

    # columns look like: ['participant','physicalisation','orientation','condition','cube', 'h', 'o', 'g', 'x', 'y']

    # focus on each cube in each trial
    conditions = frame.groupby(['physicalisation', 'participant', 'orientation', 'cube'])
    # calculate if a cube was changed in the trial
    cubes_changed = conditions.progress_apply(_chosen_cubes_to_change)
    # sum orientation changes per trial (i.e. ignore cube IDs)

    cubes_changed = cubes_changed.groupby(['physicalisation', 'participant','orientation','type']).sum()
    cubes_changed = cubes_changed.stack()

    if flatten:
        cubes_changed = cubes_changed.apply(lambda x: np.min([1, x]))

    # calculate averages of # of cubes changed per trial
    per_participant = cubes_changed.groupby(['physicalisation', 'participant', 'type','phase']).sum().unstack(level=['type','phase'])
    per_phys = cubes_changed.groupby(['physicalisation','type','phase']).sum().unstack(level=['type','phase'])

    # add a total row
    per_phys.loc["total"] = per_phys.sum(axis=0)

    with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also
        print(per_participant)

    # save
    name = "_summed"
    if flatten:
        name="_occurances"

    per_participant.to_csv(path_or_buf=helpers.create_output_folder('output') / f"atomic_orientation_changed_per_participant{name}.csv", sep=';', header=True)
    per_phys.to_csv(path_or_buf=helpers.create_output_folder('output') / f"atomic_orientation_changed{name}.csv", sep=';', header=True)

    return per_phys

def total_cubes_moved_occurance(frame: pd.DataFrame) -> None:
    # count any number of orientation changes > 0 as 1 in a trial
    return total_cubes_moved(frame, flatten=True)

def total_cubes_moved(frame: pd.DataFrame, flatten=False) -> None:
    """
    Args:
        frame: the data frame storing data to be rendered
    Returns:
        nothing
    """

    # method local to this method
    def _chosen_cubes_to_change(x):
        x = x.loc(axis=1)['o','x','y']  # drop other columns
        yx = x.loc(axis=1)['x','y']  # drop other columns

        resultframe = pd.DataFrame({
            '0-1': {
                'total' :    1 if not x.iloc[0].equals(x.iloc[1]) else 0,
                'a_orient' : 1 if not x.iloc[0].o == x.iloc[1].o else 0,
                'prox' :     1 if not yx.iloc[0].equals(yx.iloc[1]) else 0,
            },
            '1-2': {
                'total' :    1 if not x.iloc[1].equals(x.iloc[2]) else 0,
                'a_orient' : 1 if not x.iloc[1].o == (x.iloc[2].o) else 0,
                'prox' :     1 if not yx.iloc[1].equals(yx.iloc[2]) else 0,
            },
            '0-2': {
                'total' :    1 if not x.iloc[0].equals(x.iloc[2]) else 0,
                'a_orient' : 1 if not x.iloc[0].o == (x.iloc[2].o) else 0,
                'prox' :    1 if not yx.iloc[0].equals(yx.iloc[2]) else 0,
            },


        })
        # give the subaxis a name
        resultframe.rename_axis(index="type", columns="phase", inplace=True)
        return resultframe

    # columns look like: ['participant','physicalisation','orientation','condition','cube', 'h', 'o', 'g', 'x', 'y']

    # focus on each cube in each trial
    conditions = frame.groupby(['physicalisation', 'participant', 'orientation', 'cube'])
    # calculate if a cube was changed in the trial
    cubes_changed = conditions.progress_apply(_chosen_cubes_to_change)

    # sum orientation changes per trial (i.e. ignore cube IDs)

    cubes_changed = cubes_changed.groupby(['physicalisation', 'participant','orientation','type']).sum()
    cubes_changed = cubes_changed.stack()

    if flatten:
        cubes_changed = cubes_changed.apply(lambda x: np.min([1, x]))

    # calculate averages of # of cubes changed per trial
    per_participant = cubes_changed.groupby(['physicalisation', 'participant', 'type','phase']).sum().unstack(level=['type','phase'])
    per_phys = cubes_changed.groupby(['physicalisation','type','phase']).sum().unstack(level=['type','phase'])


    # add a total row
    per_phys.loc["total"] = per_phys.sum(axis=0)

    with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also
        print(per_participant)

    # save
    name = "_summed"
    if flatten:
        name="_occurances"

    # save
    per_participant.to_csv(path_or_buf=helpers.create_output_folder('output') / f"amount_cubes_changed__with_type_per_participant{name}.csv", sep=';', header=True)
    per_phys.to_csv(path_or_buf=helpers.create_output_folder('output') / f"amount_cubes_changed_with_type{name}.csv", sep=';', header=True)

    return per_phys


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

def proximity_changes_phase1(frame: pd.DataFrame) -> None:
    return proximity_changes(frame, phase = 1, name='phase1')

def proximity_changes(frame: pd.DataFrame, phase: int = 2, name: str = 'phase2') -> None:
    """
    Internal proximity = the average distance of all cluster's cubes to its centroid
    Internal proximity = the average distance of all cluster's centroids to it's closest neighbouring cluster
    This is the Davies-Bouldin index https://en.wikipedia.org/wiki/Davies%E2%80%93Bouldin_index
    how about silhouette? https://en.wikipedia.org/wiki/Silhouette_(clustering)
    how
    Args:
        frame: the data frame storing data to be rendered
        phase: choose 1 or 2
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
                mean_distance = np.nanmean(np.hypot((cond['x'] - centroid.x),(cond['y'] - centroid.y)))

                return pd.Series([
                    centroid.values.tolist(),
                    mean_distance
                    ],index=['centroid', 'distance'])

            conditions = group.groupby(['condition']).apply(_check_per_condition)

            if len(conditions) > phase:
                # round off
                try:
                    distance_before = Decimal(conditions.iloc[0]['distance']).quantize(Decimal('.01'), rounding=ROUND_HALF_EVEN)
                    distance_after = Decimal(conditions.iloc[phase]['distance']).quantize(Decimal('.01'), rounding=ROUND_HALF_EVEN)
                except (ValueError, DecimalException, InvalidOperation) as e:
                    print(conditions)

                    print(f"error: {e}, caused in 1 {group.index}")

                centroid_before = conditions.iloc[0]['centroid']
                centroid_after = conditions.iloc[phase]['centroid']
                internal_increase = 1 if distance_before < distance_after else 0
                internal_decrease = 1 if distance_before > distance_after else 0
                cluster_removed = 0
            else:
                centroid_before = conditions.iloc[0]['centroid']
                centroid_after = [np.nan, np.nan]
                distance_before = 0
                distance_after = 0
                internal_increase = 0
                internal_decrease = 0
                cluster_removed = 1

            return pd.Series(
                [centroid_before[0],
                 centroid_before[1],
                 centroid_after[0],
                 centroid_after[1],
                 distance_before,
                 distance_after,
                 internal_increase,
                 internal_decrease,
                 cluster_removed
                 ],
                index=['c_before_x','c_before_y', 'c_after_x','c_after_y', 'd_before', 'd_after', 'coh-', 'coh+','gone'])

        def _check_seperation(group):
            # calculate whether separation was increased or decreased
            # for each centroid find closest neighbour and check if the distance was increased or decreased
            seperation_increase = []
            seperation_decrease = []
            seperation_increase_only = []
            seperation_decrease_only = []
            seperation_both = []
            # assuming no duplicates exist
            # print(f"group = {group}")

            if len(group) > 1:
                for cluster in group.index.get_level_values('g'):
                    # print(f"cluster = {cluster}")
                    # print(group.loc[cluster].c_after_x)
                    # print(np.sum(group.loc[cluster].c_after_x))
                    # print(np.isnan(np.sum(group.loc[cluster].c_after_x)))

                    # do not calculat different for a cluster that is removed - we just don't count that as a seperation+ or -
                    if not np.isnan(np.sum(group.loc[cluster].c_before_x)) and not np.isnan(np.sum(group.loc[cluster].c_after_x)):
                        before = [group.loc[cluster].c_before_x, group.loc[cluster].c_before_y]
                        after = [group.loc[cluster].c_after_x, group.loc[cluster].c_after_y]

                        # remove the cluster we are going to compare from the equation
                        compare_to = group.drop(index=cluster)

                        # remove any NaN for the comparison
                        compare_to_before = compare_to.drop(columns=['c_after_x', 'c_after_y']).dropna()
                        compare_to_after = compare_to.drop(columns=['c_before_x', 'c_before_y']).dropna()

                        # calculate the smallest distance to any of the other centroids
                        # min() on a series throws NaN if an NaN is present, but we should have removed these in the above code
                        min_distance_before = np.hypot((compare_to_before.c_before_x - before[0]),(compare_to_before.c_before_y - before[1])).min()
                        min_distance_after = np.hypot((compare_to_after.c_after_x - after[0]),(compare_to_after.c_after_y - after[1])).min()

                        min_distance_before = Decimal(min_distance_before).quantize(Decimal('.01'), rounding=ROUND_HALF_EVEN)
                        min_distance_after = Decimal(min_distance_after).quantize(Decimal('.01'), rounding=ROUND_HALF_EVEN)

                        increase = 1 if min_distance_before < min_distance_after else 0
                        decrease = 1 if min_distance_before > min_distance_after else 0
                        seperation_increase.append(increase)
                        seperation_decrease.append(decrease)
                    else:
                        seperation_increase.append(0)
                        seperation_decrease.append(0)

                return [seperation_increase, seperation_decrease]

            else:
                return [0, 0]

        def _check_combos(x):
            x['coh-only'] =  1 if x['coh-'] == 1 and x['coh+'] == 0 else 0
            x['coh+only'] =  1 if x['coh-'] == 0 and x['coh+'] == 1 else 0
            x['coh-+both'] = 1 if x['coh-'] == 1 and x['coh+'] == 1 else 0
            x['sep-only'] =  1 if x['sep-'] == 1 and x['sep+'] == 0 else 0
            x['sep+only'] =  1 if x['sep-'] == 0 and x['sep+'] == 1 else 0
            x['sep-+both'] = 1 if x['sep-'] == 1 and x['sep+'] == 1 else 0
            x['coh+&sep+'] = 1 if x['coh+'] == 1 and x['sep+'] == 1 else 0
            x['coh+&no_sep+'] = 1 if x['coh+'] == 1 and x['sep+'] == 0 else 0
            x['sep+&no_coh+'] = 1 if x['coh+'] == 0 and x['sep+'] == 1 else 0

            return x


        # per group and per condition ...

        result = x.groupby(['g'])[['x','y']].apply(_check_per_group)

        result['sep+'],result['sep-'] = _check_seperation(result)
        result.drop(['c_before_x', 'c_before_y','c_after_x','c_after_y','d_before','d_after'], axis=1, inplace=True)
        result = result.sum()

        # if it occurered more than once in any group, just pen down 1 (thus the max of all of these become 80)
        result = result.transform(lambda x: (1 if x > 0 else 0))
        # check fr combinations of coh and sep
        result = _check_combos(result)

        return result



    # columns look like: ['participant','physicalisation','orientation','condition','cube', 'h', 'o', 'g', 'x', 'y']

    # convert to numbers where possible
    print(frame.info())

    # reset index, we need a different angle, we want to check the cubes, per condition,
    frame.reset_index(inplace=True)
    frame.set_index(['physicalisation', 'participant', 'orientation', 'g', 'condition', 'cube'], inplace=True)

    # per trial...

    # if specific, change query here
    # conditions = frame.query('physicalisation == 5 and participant == 4 and orientation == "N"').groupby(['physicalisation', 'participant', 'orientation'])
    conditions = frame.groupby(['physicalisation', 'participant', 'orientation'])
    clusters_change = conditions.progress_apply(_centroids_distances)

    # with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also
         # print(clusters_change)

    per_participant = clusters_change.groupby(['physicalisation', 'participant']).sum()
    per_phys = clusters_change.groupby(['physicalisation']).sum()

    # add a total row
    per_phys.loc["total"] = per_phys.sum(axis=0)

    with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also
        print(per_participant)

    # save
    per_participant.to_csv(path_or_buf=helpers.create_output_folder('output') / f"cluster_coh&sep_per_participant_{name}.csv", sep=';', header=True)
    per_phys.to_csv(path_or_buf=helpers.create_output_folder('output') / f"cluster_coh&sep_{name}.csv", sep=';', header=True)

    return per_phys
