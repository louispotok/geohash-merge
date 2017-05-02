Tools for merging pandas dataframes using geohashing.

Note: none of this is tested, that's a TODO.

Geohashing ([python implementation](https://github.com/vinsci/geohash/)) is a way to encode latitude and longitude into a single string. The length of the string encodes the amount of precision, and nearby places will *usually* have similar prefixes.

The problem this is meant to solve is as follows:
* suppose you have two lists of (lat, long) points with different precision
* how can you decide whether a point in list A represents the same point as a point in list B?

One possibility is to simply compute for each point in A the closest point in B (and to apply a threshold where only matches within a certain distance are considered). Geohashing provides an alternative.

This "library" provides a few convenience functions for working with geohashes. It assumes that you have two pandas DataFrames, each with a column containing geohashes, and you are trying to merge them. Right now only left outer merges are supported.

The functions provided are:
* `assess_precision`: tells you how many points in `left` have matches in `right` for a given amount of precision. The idea is that you visualize these results and see where the "elbow" is, in other words use heuristics to decide where you want to make the tradeoff between "more matches" and "less precise matches".
* `merge` runs a merge at a specified level of precision. The idea is that you first `assess_precision` and then run a merge at your desired level of precision.
* `generous_merge` matches, for each point in `left`, the best match in `right` (or matches, if there is a tie).

Read more about geohashing:
* https://en.wikipedia.org/wiki/Geohash


