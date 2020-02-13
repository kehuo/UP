import traceback
from datetime import datetime, timedelta
import pandas as pd


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
    :param all_raw_csv_name: 一个列表, 包含在raw文件夹下的所有 csv文件名, 如 raw_overview_2020_01_20 09_00_00 PM.csv
    :param current_timestamp: 运行该程序时的时间, str类型, 如 "2020_01_20"
    :param required_csv_name_one: 比如 "raw_overview"
    :return: 2个条件都符合 > 返回对应的 完整raw_csv的文件名. 否则返回None
    """
    res = None
    filtered_raw_csv_name = []
    for i in all_raw_csv_name:
        if required_csv_name_one in i:
            # todo qr_transaction_cnt_by_scene / qr_transaction_cnt_by_scene_top100_in_city 会有问题, 用if特殊处理
            if required_csv_name_one == "raw_qr_transaction_cnt_by_scene":
                if "top100_in_city" in i:
                    continue
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

    if the_bingo_idx is not None:
        res = df.loc[the_bingo_idx][col]
    return res


def transfer_sentence_dict_to_dataframe(sentence_dict, pandas_col_name):
    """
    将一个 结构化的 文字字典 转换成 pandas.DataFrame
    """

    # 将self.all_str 从字典 转成 字符串
    sentence_str = ""
    for k, v in sentence_dict.items():
        sentence_str += v

    # 转成 dataframe 后返回结果
    df = pd.DataFrame(data={pandas_col_name: [sentence_str]})
    return df


def str2number(a_dict):
    """传入一个字典，将这个字典所有的v, 从str类型转成 float 的数字类型."""
    for k, v in a_dict.items():
        a_dict[k] = float(v)
    return a_dict
