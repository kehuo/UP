from common.utils import transfer_sentence_dict_to_dataframe


def transaction_cnt_by_day(sentence_dict, all_raw_csv, cfg):
    """
    1.2 -- 支付类交易情况
    """
    # 1 todo 根据需求, 构造 sentence_dict

    # 2 sentence df
    sentence_df = transfer_sentence_dict_to_dataframe(sentence_dict=sentence_dict, pandas_col_name="sentence")

    # 3 构造 csv
    csv = all_raw_csv["raw_transaction_cnt_by_day"]

    # 4 结果
    res = {"sentence": sentence_df,
           "csv": csv}
    return res


