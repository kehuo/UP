from common.utils import transfer_sentence_dict_to_dataframe


def qr_transaction_cnt_by_scene(sentence_dict, all_raw_csv, cfg):
    """
    model 2.2 --  - 一段文字 + 1个 csv
    1 - sentence_df
    2 - csv
    """
    # 1 sentence df
    sentence_df = transfer_sentence_dict_to_dataframe(sentence_dict=sentence_dict, pandas_col_name="sentence")

    # 2 csv
    csv = all_raw_csv["raw_qr_transaction_cnt_by_scene"]

    # 构造结果
    res = {"sentence": sentence_df,
           "csv": csv}
    return res


def qr_transaction_by_area_cd(sentence_dict, all_raw_csv, cfg):
    """
    model 2.3 --  - 一段文字 + 1个 csv
    1 - sentence_df
    2 - csv
    """
    # 1 sentence df
    sentence_df = transfer_sentence_dict_to_dataframe(sentence_dict=sentence_dict, pandas_col_name="sentence")

    # 2 csv
    csv = all_raw_csv["raw_qr_transaction_by_area_cd"]

    # 构造结果
    res = {"sentence": sentence_df,
           "csv": csv}
    return res


def qr_transaction_by_merchant(sentence_dict, all_raw_csv, cfg):
    """
    model 2.4 --  - 一段文字 + 1个 csv
    1 - sentence_df
    2 - csv

    """
    # 1 sentence df
    sentence_df = transfer_sentence_dict_to_dataframe(sentence_dict=sentence_dict, pandas_col_name="sentence")

    # 2 csv
    csv = all_raw_csv["raw_qr_transaction_by_merchant"]

    # 构造结果
    res = {"sentence": sentence_df,
           "csv": csv}
    return res


def qr_transaction_by_amount_of_money(sentence_dict, all_raw_csv, cfg):
    """
    model 2.5 --  - 一段文字 + 1个 csv
    1 - sentence_df
    2 - csv
    """
    # 1 sentence df
    sentence_df = transfer_sentence_dict_to_dataframe(sentence_dict=sentence_dict, pandas_col_name="sentence")

    # 2 csv
    csv = all_raw_csv["raw_qr_transaction_by_amount_of_money"]

    # 构造结果
    res = {"sentence": sentence_df,
           "csv": csv}
    return res