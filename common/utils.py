from datetime import datetime, timedelta


def process_float(raw_float, baoliu_num=2):
    """
    :param raw_float: 原始的数据如 12.335435
    :param baoliu_num: 保留小数点后几位
    :return:
    """
    return round(raw_float, baoliu_num)


def build_date_str(minus_day_count=0, str_type="bottom_line"):
    """type=cn > 返回 x年x月x日
    typw = bottom_line > 返回 xxxx_xx_xx"""
    res = datetime.now().date() - timedelta(days=minus_day_count)

    if str_type == "cn":
        res = "%s年%s月%s日" % (res.year, res.month, res.day)

    elif str_type == "bottom_line":
        res = "%s_%s_%s" % (res.year, res.month, res.day)

    elif str_type == "middle_line":
        res = res.strftime("%Y-%m-%d")
    return res


def can_load(all_raw_csv_name, required_csv_name_one, current_timestamp):
    """
    :param all_raw_csv_name: 在raw文件夹下的 csv文件名, 如 raw_overview_2020_01_20 09_00_00 PM.csv
    :param current_timestamp: 运行该程序时的时间, str类型, 如 "2020_01_20"
    :param required_csv_name_one: 比如 "raw_overview"
    :return: 2个条件都符合 > True; 否则返回 False
    """
    res = None
    filtered_raw_csv_name = []
    for i in all_raw_csv_name:
        if required_csv_name_one in i:
            filtered_raw_csv_name.append(i)

    for raw_one in filtered_raw_csv_name:
        if current_timestamp in raw_one:
            res = raw_one
            break

    return res


def find_df_value(df, col, row):
    """返回一个 dataframe 中 某一行 某一列的一个值
    示例:
    df = raw_overview.csv
    col = cnt_yesterday
    row = all_merchant

    那么 res = raw_overview.csv 中 "index"等于all_merchant那一行的 "cnt_yesterday"列的值
    """
    res = None
    the_bingo_idx = None
    for idx in df.index:
        if df.loc[idx]["index"] == row:
            the_bingo_idx = idx
            break

    if the_bingo_idx:
        res = df.loc[the_bingo_idx][col]
    return res
