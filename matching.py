"""
The workflow imagined here is:

* You have two pandas dataframes
    * Each of them has a column that is a geohash
    * You want to merge them on their geohash
* You will need to decide how much precision to keep
    * First, you check how many matches you would have given each possible level of precision
* Then you want to merge them on the reduced precision that you choose

TODOs:
* support args and kwargs passed
* add support for "contains" merges and explanation of difference
"""

MAX_PRECISION = 12

# assess_precision
def assess_precision(left, right, left_on, right_on):
    """
    left and right are dataframes
    left_on and right_on are the names of the columns with the geohash
    returns
        (
            (number_digits_dropped, number_matches),
        )
    """

    left_geohash = left[left_on]
    right_geohash = right[right_on]

    # TODO: Better error handling if bad input
    # TODO: be more generous about input
    assert (left_geohash.str.len() == MAX_PRECISION).all()
    assert (right_geohash.str.len() == MAX_PRECISION).all()

    results = []

    for i in range(MAX_PRECISION):
        number_matches = (left_geohash
            .str[:MAX_PRECISION - i]
            .isin(right_geohash.str[:MAX_PRECISION - i])
            .sum()
        results.append(i, number_matches)

    return tuple(results)


def merge(left, right, left_on, right_on, desired_precision):
    """
    left and right are dataframes
    left_on and right_on are the names of the columns with the geohash
    desired_precision is the number of digits of precision you want to keep

    args and kwargs will be passed to the left dataframe's `merge` method

    TODO: find a way to do this without making copies of both dataframes
    """
    new_left = left.copy()
    new_right = right.copy()

    new_left['reduced_geohash'] = new_left[left_on].str[:desired_precision]
    new_right['reduced_geohash'] = new_right[right_on].str[:desired_precision]
    return new_left.merge(new_right, on='reduced_geohash')


def generous_merge(left, right, left_on, right_on):
    """
    for each point in left, merges to the best match in right (or matches, if there is a tie)
    """
    dfs = []
    for i in range(MAX_PRECISION):
        idxs_matched = sum([df.index for df in dfs])
        left_tmp = left.loc[set(left.index).difference(set(idxs_matched))]
        merged = merge(left_tmp, right, left_on, right_on, MAX_PRECISION - i)
        dfs.append(merged)

    return pd.concat(dfs).loc[left.index]
