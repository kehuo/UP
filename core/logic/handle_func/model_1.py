from common.utils import transfer_sentence_dict_to_dataframe


def transaction_cnt_by_day(sentence_dict, all_raw_csv, cfg):
    """
    model 1 -- 支付类交易情况 - 一段文字 + 1个 csv
    1 - sentence_df
    2 - csv
    """
    # 1 sentence df
    sentence_df = transfer_sentence_dict_to_dataframe(sentence_dict=sentence_dict, pandas_col_name="sentence")

    # 2 csv
    csv = all_raw_csv["raw_transaction_cnt_by_day"]

    # 构造结果
    res = {"sentence": sentence_df,
           "csv": csv}
    return res


