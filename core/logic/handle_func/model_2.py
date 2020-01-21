from common.utils import transfer_sentence_dict_to_dataframe


def qr_transaction_cnt_by_scene(sentence_dict, all_raw_csv, cfg):
    """
    2.2 - 主要场景交易情况
    """
    # 1 todo 根据需求, 构造 sentence_dict

    # 2 sentence df
    sentence_df = transfer_sentence_dict_to_dataframe(sentence_dict=sentence_dict, pandas_col_name="sentence")

    # 3 csv
    csv = all_raw_csv["raw_qr_transaction_cnt_by_scene"]

    # 4 结果
    res = {"sentence": sentence_df,
           "csv": csv}
    return res


def qr_transaction_by_area_cd(sentence_dict, all_raw_csv, cfg):
    """
    model 2.3 - 二维码TOP10分公司交易情况
    """
    # 1 todo 根据需求, 构造 sentence_dict

    # 2 sentence df
    sentence_df = transfer_sentence_dict_to_dataframe(sentence_dict=sentence_dict, pandas_col_name="sentence")

    # 3 csv
    csv = all_raw_csv["raw_qr_transaction_by_area_cd"]

    # 4 结果
    res = {"sentence": sentence_df,
           "csv": csv}
    return res


def qr_transaction_by_merchant(sentence_dict, all_raw_csv, cfg):
    """
    model 2.4 - 二维码TOP10商户交易情况
    """
    # 1 todo 根据需求, 构造 sentence_dict

    # 2 sentence df
    sentence_df = transfer_sentence_dict_to_dataframe(sentence_dict=sentence_dict, pandas_col_name="sentence")

    # 3 csv
    csv = all_raw_csv["raw_qr_transaction_by_merchant"]

    # 4 结果
    res = {"sentence": sentence_df,
           "csv": csv}
    return res


def qr_transaction_by_amount_of_money(sentence_dict, all_raw_csv, cfg):
    """
    model 2.5 - 二维码交易金额分布
    """
    # 1 todo 根据需求, 构造 sentence_dict

    # 2 sentence df
    sentence_df = transfer_sentence_dict_to_dataframe(sentence_dict=sentence_dict, pandas_col_name="sentence")

    # 3 csv
    csv = all_raw_csv["raw_qr_transaction_by_amount_of_money"]

    # 4 结果
    res = {"sentence": sentence_df,
           "csv": csv}
    return res