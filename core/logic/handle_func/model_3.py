from common.utils import transfer_sentence_dict_to_dataframe


def control_transaction_top10_merchant(sentence_dict, all_raw_csv, cfg):
    """
    model 3.2 - 手机支付控件TOP10商户交易情况
    """
    # 1 todo 构造 sentence_dict
    csv = all_raw_csv["raw_control_by_merchant_details"]

    # 2 sentence df
    sentence_df = transfer_sentence_dict_to_dataframe(sentence_dict=sentence_dict, pandas_col_name="sentence")

    # 3 todo 构造 final_csv
    final_csv = csv

    # 4 构造结果
    res = {"sentence": sentence_df,
           "csv": final_csv}
    return res


def control_out_transaction_top10_merchant(sentence_dict, all_raw_csv, cfg):
    """
    model 3.3 - 手机外部支付控件TOP10商户交易情况
    """
    # 1 todo 构造 sentence_dict
    csv = all_raw_csv["raw_control_out_by_merchant_details"]

    # 2 sentence df
    sentence_df = transfer_sentence_dict_to_dataframe(sentence_dict=sentence_dict, pandas_col_name="sentence")

    # 3 todo 构造 final_csv
    final_csv = csv

    # 4 构造结果
    res = {"sentence": sentence_df,
           "csv": final_csv}
    return res


def control_out_by_area_cd(sentence_dict, all_raw_csv, cfg):
    """
    model 3.4 - 手机外部支付控件TOP10商户侧分公司交易情况
    """
    # 1 todo 构造 sentence_dict
    csv = all_raw_csv["raw_control_out_by_area_cd"]

    # 2 sentence df
    sentence_df = transfer_sentence_dict_to_dataframe(sentence_dict=sentence_dict, pandas_col_name="sentence")

    # 3 todo 构造 final_csv
    final_csv = csv

    # 4 构造结果
    res = {"sentence": sentence_df,
           "csv": final_csv}
    return res


def control_out_by_user_gps(sentence_dict, all_raw_csv, cfg):
    """
    model 3.5 - 手机外部支付控件TOP10用户侧分公司交易情况
    """
    # 1 todo 构造 sentence_dict
    csv = all_raw_csv["control_out_by_user_gps"]

    # 2 sentence df
    sentence_df = transfer_sentence_dict_to_dataframe(sentence_dict=sentence_dict, pandas_col_name="sentence")

    # 3 todo 构造 final_csv
    final_csv = csv

    # 4 构造结果
    res = {"sentence": sentence_df,
           "csv": final_csv}
    return res


def control_out_transaction_by_amount_of_money(sentence_dict, all_raw_csv, cfg):
    """
    model 3.6 - 手机外部支付控件交易金额分布
    """
    # 1 todo 构造 sentence_dict
    csv = all_raw_csv["raw_control_out_transaction_by_amount_of_money"]

    # 2 sentence df
    sentence_df = transfer_sentence_dict_to_dataframe(sentence_dict=sentence_dict, pandas_col_name="sentence")

    # 3 todo 构造 final_csv
    final_csv = csv

    # 4 构造结果
    res = {"sentence": sentence_df,
           "csv": final_csv}
    return res