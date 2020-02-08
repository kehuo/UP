import pandas as pd
import traceback
from common.utils import transfer_sentence_dict_to_dataframe


def control_transaction_top10_merchant(sentence_dict, all_raw_csv, cfg):
    """
    model 3.2 - 手机支付控件TOP10商户交易情况
    """
    # 1 todo 构造 sentence_dict
    csv = all_raw_csv["raw_control_transaction_top10_merchant"]

    csv['dis_proportion'] = csv['dis_cnt_today'] / csv['cnt_today']
    csv['ratio_by_yesterday'] = csv['ratio_by_yesterday'].apply(lambda x: format(float(x), '.2%'))
    csv['dis_proportion'] = csv['dis_proportion'].apply(lambda x: format(float(x), '.2%'))

    # 删除一行
    csv = csv.drop(1)

    target_text = "1、手机支付控件TOP10商户主要是信用卡还款业务、以内部商户为主，商户优惠交易占比仅为{}%。".format(
        round(csv['dis_cnt_today'].sum() / csv['cnt_today'].sum() * 100, 2)
    )

    # 2 todo sentence df - 暂时用tmp dict, 以后再完善
    tmp_sentence_dict = {"value": target_text}
    sentence_df = transfer_sentence_dict_to_dataframe(sentence_dict=tmp_sentence_dict, pandas_col_name="sentence")

    # 3 构造 final_csv
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
    csv = all_raw_csv["raw_control_out_transaction_top10_merchant"]

    csv['dis_proportion'] = csv['dis_cnt_today'] / csv['cnt_today']
    csv['ratio_by_yesterday'] = csv['ratio_by_yesterday'].apply(lambda x: format(float(x), '.2%'))
    csv['dis_proportion'] = csv['dis_proportion'].apply(lambda x: format(float(x), '.2%'))

    # 2 sentence df **注意** 这里没有任何句子，这里返回一个空df即可.
    tmp_sentence_dict = {"value": ""}
    sentence_df = transfer_sentence_dict_to_dataframe(sentence_dict=tmp_sentence_dict, pandas_col_name="sentence")

    # 3 构造 final_csv
    # 不需要 mchnt_type 列, 从csv中删掉
    del csv["mchnt_type"]
    final_csv = csv

    # 4 构造结果
    res = {"sentence": sentence_df,
           "csv": final_csv}

    return res


def control_out_by_area_cd(sentence_dict, all_raw_csv, cfg):
    """
    model 3.4 - 手机外部支付控件TOP10商户侧分公司交易情况
    """
    # 1 构造 sentence_dict
    csv = all_raw_csv["raw_control_out_by_area_cd"]

    csv['交易笔数占比'] = csv['交易笔数'] / csv['交易笔数'].sum()
    csv['交易笔数环比'] = csv['交易笔数环比'].apply(lambda x: format(float(x), '.2%'))
    csv['优惠笔数环比'] = csv['优惠笔数环比'].apply(lambda x: format(float(x), '.2%'))
    csv['交易笔数占比'] = csv['交易笔数占比'].apply(lambda x: format(float(x), '.2%'))
    csv['优惠笔数占比'] = csv['优惠交易笔数'] / csv['交易笔数']
    csv['优惠笔数占比'] = csv['优惠笔数占比'].apply(lambda x: format(float(x), '.2%'))
    csv = csv.head(10).loc[:, ['pro', '交易笔数', '交易笔数占比', '交易笔数环比', '优惠交易笔数', '优惠笔数占比', '优惠笔数环比']]

    # 删掉 "其他" 这一列
    for idx in csv.index:
        if csv.iloc[idx]["pro"] == '其他':
            csv = csv.drop([idx])
            break

    list_area = csv['pro'].values.tolist()
    b = '、'
    area = b.join(list_area)

    target_text = "2、当日，从商户入网分公司来看，" + area + "地区交易量排名手机外部支付控件前十。"

    # 2 todo sentence df - 暂时用 tmp dict, 以后再完善
    tmp_sentence_dict = {"value": target_text}
    sentence_df = transfer_sentence_dict_to_dataframe(sentence_dict=tmp_sentence_dict, pandas_col_name="sentence")

    # 3 构造 final_csv
    final_csv = csv

    # 4 构造结果
    res = {"sentence": sentence_df,
           "csv": final_csv}
    return res


def control_out_by_user_gps(sentence_dict, all_raw_csv, cfg):
    """
    model 3.5 - 手机外部支付控件TOP10用户侧分公司交易情况
    """
    # 1 构造 sentence_dict
    csv = all_raw_csv["raw_control_out_by_user_gps"].sort_values(by="交易笔数", ascending=False)

    # 只删除 branch 列中，值为null的项
    csv.dropna(axis=0, subset=["branch"], inplace=True)
    csv['交易笔数占比'] = csv['交易笔数'] / csv['交易笔数'].sum()
    csv['交易笔数环比'] = csv['交易笔数环比'].apply(lambda x: format(float(x), '.2%'))
    csv['优惠笔数环比'] = csv['优惠笔数环比'].apply(lambda x: format(float(x), '.2%'))
    csv['交易笔数占比'] = csv['交易笔数占比'].apply(lambda x: format(float(x), '.2%'))
    csv['优惠笔数占比'] = csv['优惠交易笔数'] / csv['交易笔数']
    csv['优惠笔数占比'] = csv['优惠笔数占比'].apply(lambda x: format(float(x), '.2%'))
    csv = csv.head(10).loc[:, ['branch', '交易笔数', '交易笔数占比', '交易笔数环比', '优惠交易笔数', '优惠笔数占比', '优惠笔数环比']]

    area = "、".join(csv['branch'].values.tolist())
    target_text = "3、当日，从交易用户归属地来看，" + area + "地区交易量排名手机外部支付控件前十。"

    # 2 todo sentence df - 暂时用 tmp dict, 以后有时间再完善
    tmp_sentence_dict = {"value": target_text}
    sentence_df = transfer_sentence_dict_to_dataframe(sentence_dict=tmp_sentence_dict, pandas_col_name="sentence")

    # 3 构造 final_csv
    final_csv = csv

    # 4 构造结果
    res = {"sentence": sentence_df,
           "csv": final_csv}
    return res


def control_out_transaction_by_amount_of_money(sentence_dict, all_raw_csv, cfg):
    """
    model 3.6 - 手机外部支付控件交易金额分布
    """
    # 1 todo 构造 sentence_dict - 会用到2个csv, 分别是 raw_overview 和  control_out_transaction_by_amount_of_money.
    csv = all_raw_csv["raw_control_out_transaction_by_amount_of_money"]
    df_overview = all_raw_csv["raw_overview"]

    control_out_mchnt = df_overview['cnt_today'][df_overview['index'] == 'control_out_mchnt'].values[0]

    csv['交易笔数占比'] = csv['交易笔数'] / csv['交易笔数'].sum()
    csv['商户数占比'] = csv['商户数'] / control_out_mchnt
    csv['商户日均交易笔数'] = csv['交易笔数'] / csv['商户数']
    csv['交易笔数占比'] = csv['交易笔数占比'].apply(lambda x: format(float(x), '.2%'))
    csv['商户数占比'] = csv['商户数占比'].apply(lambda x: format(float(x), '.2%'))
    csv = csv.loc[:, ['金额区间', '交易笔数', '交易笔数占比', '商户数', '商户数占比', '商户日均交易笔数']]

    # 把 csv 按照 10元以下 / 10-50元 / 50-100元 / 100-1000元 / 1000元以上 的顺序, 重新排序
    sort_res = True
    sorted_csv = pd.DataFrame(columns=csv.columns)
    try:
        sorted_data = []
        sort_index = ["0-10元", "10-50元", "50-100元", "100-1000元", "1000元以上"]
        for i in sort_index:
            sorted_data.append(csv[csv['金额区间'] == i].values[0])

        for j in range(len(sorted_data)):
            sorted_csv.loc[j] = sorted_data[j]
    except Exception as e:
        sort_res = False
        print("在control.py文件中, 运行control_out_transaction_by_amount_of_money函数时, 对csv根据金额区间排序时失败了.")
        print("失败的具体原因: %s" % traceback.format_exc())

    # 手机控件交易情况
    target_text = "4、交易金额整体偏低。交易金额在10元以下的交易笔数占比达{}。".format(
        csv['交易笔数占比'][csv['金额区间'] == '0-10元'].values[0]
    )

    # 2 todo sentence df - 暂时用tmp dict, 以后有时间再完善
    tmp_sentence_dict = {"value": target_text}
    sentence_df = transfer_sentence_dict_to_dataframe(sentence_dict=tmp_sentence_dict, pandas_col_name="sentence")

    # 3 构造 final_csv - 若排序成功, 则用排序后的结果，若失败则使用未排序的原始 csv
    final_csv = sorted_csv if sort_res is True else csv

    # 4 构造结果
    res = {"sentence": sentence_df,
           "csv": final_csv}
    return res
