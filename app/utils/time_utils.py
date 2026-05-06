def calc_week_diff(y1, m1, w1, y2, m2, w2):
    """
    2つの日時（year, month, week）間の週差を返す
    """

    total1 = y1 * 48 + m1 * 4 + w1
    total2 = y2 * 48 + m2 * 4 + w2

    return total2 - total1