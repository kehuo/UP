from common.utils import transfer_sentence_dict_to_dataframe


def transaction_cnt_by_day(sentence_dict, all_raw_csv, cfg):
    """
    1.2 -- 支付类交易情况

    如何读取需要的csv:
    比如你想读取 raw_control_by_merchant_details_2020_01_20 09_00_00 PM.csv, 那么
    the_csv = all_raw_csv["raw_control_by_merchant_details"]
    the_csv 是 pandas.DataFrame 数据结构

    sentence_dict: 是一个结构化好的字典格式的一段文字.
    举例 - model 1 的 总体交易情况的结构化的文字长这样:
    sentence_dict = {
        "very_beginning": "",
        "trans_type": "",
        "proportion": ""
    }
    你需要做的, 就是根据csv, 把这几个 "" 空字符串填满.
    """
    # 1 todo 根据需求, 构造 sentence_dict
    csv = all_raw_csv["raw_transaction_cnt_by_day"]

    data = {
        "1": str(round(csv["cnt_today"].sum() / 10000, 2)),
        "2": "、".join(list(csv["index"])[:10]),
        "3": str(round(csv["cnt_today"][:10].sum() / csv["cnt_today"].sum() * 100, 2)) + "%"
    }
    # 1.1
    sentence_dict["very_beginning"] = "当日, 云闪付APP发生支付类交易%s万笔" % data["1"]
    # 1.2
    sentence_dict["trans_type"] = "其中%s交易笔数排名前十，" % data["2"]
    # 1.3
    sentence_dict["proportion"] = "占到交易总量的%s。" % data["3"]

    # 2 sentence df
    sentence_df = transfer_sentence_dict_to_dataframe(sentence_dict=sentence_dict, pandas_col_name="sentence")

    # 3 todo 构造 final_csv - 新写一列 proportion (ratio是环比)
    csv["proportion"] = csv["cnt_today"] / csv["cnt_today"].sum()
    final_csv = csv.loc[:, ['index', 'cnt_today', 'proportion', 'ratio']]

    # 4 结果
    res = {"sentence": sentence_df,
           "csv": final_csv}
    return res
