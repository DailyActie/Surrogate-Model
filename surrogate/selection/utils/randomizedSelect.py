from ._randomizedPartition import _randomizedPartition


def randomizedSelect(array, begin, end, i):
    """Allows to select the ith smallest element from array without sorting it.
    Runtime is expected to be O(n).
    """
    if begin == end:
        return array[begin]
    q = _randomizedPartition(array, begin, end)
    k = q - begin + 1
    if i < k:
        return randomizedSelect(array, begin, q, i)
    else:
        return randomizedSelect(array, q + 1, end, i - k)
