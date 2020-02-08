import pandas as pd
import traceback
from common.utils import transfer_sentence_dict_to_dataframe


def qr_transaction_cnt_by_scene(sentence_dict, all_raw_csv, cfg):
    """
    2.2 - 主要场景交易情况

    A -- df_scene_new: merge出来的表df_scene_new, 就是 主要场景交易情况的 基础表. 这个 DataFrame 中个字段的含义:
    <1> qr_code_cnt --> 今天的二维码交易笔数
    <2> qr_code_cnt_by_yesterday --> 昨天的二维码交易笔数
    <3> qr_code_cnt_by_last_year --> 去年今天的二维码交易笔数
    <1> cnt_today_x 和 cnt_yesterday_x 还有 ratio_x --> 带 x 的都是总体
    <2> cnt_today_y / cnt_yesterday_y / ratio_y --> 带 y 的都是top 100的
    <3> proportion_xy --> 代表了 top100 在总体中的占比

    B -- 在 data 中用到的几个变量含义:
    <1> top100_count -> 交易笔数的数量, 约等于6063584;
    <2> top100_mchnt_count -> 是商户号去重之后的商户数量, 值大概为 32091.
    <3> qr_mchnt -> 二维码的商户数量
    """
    # 1 根据需求, 构造 sentence_dict
    csv = all_raw_csv["raw_qr_transaction_cnt_by_scene"]
    df_overview = all_raw_csv["raw_overview"]

    # A - 处理 df_scene_new
    qr_code_cnt = df_overview['cnt_today'][df_overview['index'] == 'qr_code_cnt'].values[0]
    qr_code_cnt_by_yesterday = df_overview['ratio_by_yesterday'][df_overview['index'] == 'qr_code_cnt'].values[0]
    qr_code_cnt_by_last_year = df_overview['ration_by_last_year'][df_overview['index'] == 'qr_code_cnt'].values[0]

    csv['proportion'] = csv['cnt_today'] / csv['cnt_today'].sum()
    csv['proportion'] = csv['proportion'].apply(lambda x: format(float(x), '.2%'))
    csv['ratio'] = csv['ratio'].apply(lambda x: format(float(x), '.2%'))
    df_scene_new = pd.merge(csv, all_raw_csv["raw_qr_transaction_cnt_by_scene_top100_in_city"], on='scene')

    df_scene_new['proportion_xy'] = df_scene_new['cnt_today_y'] / df_scene_new['cnt_today_x']
    df_scene_new['proportion_xy'] = df_scene_new['proportion_xy'].apply(lambda x: format(float(x), '.2%'))

    df_scene_new['ratio_y'] = df_scene_new['ratio_y'].apply(lambda x: format(float(x), '.2%'))
    df_scene_new = df_scene_new.head(11).loc[:, ['scene', 'cnt_today_x', 'proportion', 'ratio_x',
                                                 'cnt_today_y', 'ratio_y', 'proportion_xy']]

    # B - 处理 data 和最终的 target_text. 其中 data 是: 最后拼接句子时, 需要的所有相关的变量值.
    top100_count = all_raw_csv["raw_qr_transaction_by_merchant"]["cnt"].sum()
    top100_mchnt_count = len(set(all_raw_csv["raw_qr_transaction_by_merchant"]["mchnt_cd"]))
    qr_mchnt = df_overview['cnt_today'][df_overview['index'] == 'qr_code_mchnt_cnt'].values[0]

    data = {
        "1": str(round(qr_code_cnt / 10000, 2)),
        "2": str(round(qr_code_cnt_by_yesterday * 100, 2)) + "%",
        "3": str(round(float(qr_code_cnt_by_last_year) * 100, 2)) + "%",

        "4": "、".join(df_scene_new.head(3)['scene'].values.tolist()),
        "5": str(df_scene_new.head(3)['proportion'].values.tolist()[0]),
        "6": str(df_scene_new.head(3)['proportion'].values.tolist()[1]),
        "7": str(df_scene_new.head(3)['proportion'].values.tolist()[2]),

        "8": str(round(top100_count / 10000, 2)),
        "9": str(round(top100_count / qr_code_cnt * 100, 2)) + "%",
        "10": str(round(top100_mchnt_count / 10000, 2)),
        "11": str(round(top100_mchnt_count / qr_mchnt * 100, 2)) + "%"
    }

    target_text_dict = {
        "1": "当日, 二维码(含乘车码)交易笔数为%s笔, 环比下降%s, 同比增长%s。" % (
            data["1"],
            data["2"],
            data["3"]
        ),

        "2": "其主要场景分布在%s场景, 占比分别达%s、%s、%s。" % (
            data["4"],
            data["5"],
            data["6"],
            data["7"]
        ),

        "3": "其中各城市TOP100商户交易笔数%s万笔, 占当日二维码总交易笔数的%s; 交易商户%s万, 占二维码交易商户数的%s。" % (
            data["8"],
            data["9"],
            data["10"],
            data["11"]
        )
    }

    # 把 target_text_dict 字典拼成一个str类型的长句子
    target_text = ""
    for k, v in target_text_dict.items():
        target_text += v

    # 2 todo sentence df -- 暂时用 tmp_sentence_dict, 以后有时间再分割 sentence_dict
    tmp_sentence_dict = {"value": target_text}
    sentence_df = transfer_sentence_dict_to_dataframe(sentence_dict=tmp_sentence_dict, pandas_col_name="sentence")

    # 3 构造 final_csv
    final_csv = df_scene_new

    # 4 结果
    res = {"sentence": sentence_df,
           "csv": final_csv}

    return res


def qr_transaction_by_area_cd(sentence_dict, all_raw_csv, cfg):
    """
    model 2.3 - 二维码TOP10分公司交易情况
    """
    # 1 todo 根据需求, 构造 sentence_dict
    csv = all_raw_csv["raw_qr_transaction_by_area_cd"]

    csv['proportion'] = csv['cnt_today'] / csv['cnt_today'].sum()
    csv['dis_proportion'] = csv['dis_cnt_today'] / csv['cnt_today']
    csv['proportion'] = csv['proportion'].apply(lambda x: format(float(x), '.2%'))
    csv['ratio'] = csv['ratio'].apply(lambda x: format(float(x), '.2%'))
    csv['dis_proportion'] = csv['dis_proportion'].apply(lambda x: format(float(x), '.2%'))
    csv['dis_ratio'] = csv['dis_ratio'].apply(lambda x: format(float(x), '.2%'))
    csv = csv.head(10).loc[:, ['branch', 'cnt_today', 'proportion', 'ratio',
                               'dis_cnt_today', 'dis_proportion', 'dis_ratio']]

    target_text = "1、当日，%s地区交易量排名前十。" % "、".join(csv['branch'].values.tolist())

    # 2 todo sentence df --> (注, 由于没有对这句话进行 k-v 分割，暂时用 tmp sentence dict 代替，以后有时间再分割这个句子.)
    tmp_sentence_dict = {"value": target_text}
    sentence_df = transfer_sentence_dict_to_dataframe(sentence_dict=tmp_sentence_dict, pandas_col_name="sentence")

    # 3 todo 构造 final_csv
    final_csv = csv

    # 4 结果
    res = {"sentence": sentence_df,
           "csv": final_csv}
    return res


def qr_transaction_by_merchant(sentence_dict, all_raw_csv, cfg):
    """
    model 2.4 - 二维码TOP10商户交易情况

    sentence:
    交易笔数TOP10 的商户以乘车码交易为主，优惠笔数占比为 82.47%。
    """
    # 1 todo 根据需求, 构造 sentence_dict
    csv = all_raw_csv["raw_qr_transaction_top10_merchant"]

    csv['dis_proportion'] = csv['discnt_today'] / csv['cnt_today']
    csv['cnt_ratio'] = csv['cnt_ratio'].apply(lambda x: format(float(x), '.2%'))
    csv['dis_proportion'] = csv['dis_proportion'].apply(lambda x: format(float(x), '.2%'))
    csv = csv.loc[:, ['mchnt_nm', 'type1', 'scene', 'cnt_today', 'cnt_ratio', 'discnt_today', 'dis_proportion']]

    data = str(round(csv['discnt_today'].sum() / csv['cnt_today'].sum() * 100, 2))
    target_text = "2、交易笔数TOP10的商户以乘车码交易为主，优惠笔数占比为%s。" % data

    # 2 todo sentence df 先用 tmp 临时顶上，以后有时间，再完善sentence dict分割
    tmp_sentence_dict = {"value": target_text}
    sentence_df = transfer_sentence_dict_to_dataframe(sentence_dict=tmp_sentence_dict, pandas_col_name="sentence")

    # 3 构造 final_csv
    final_csv = csv

    # 4 结果
    res = {"sentence": sentence_df,
           "csv": final_csv}

    return res


def qr_transaction_by_amount_of_money(sentence_dict, all_raw_csv, cfg):
    """
    model 2.5 - 二维码交易金额分布
    """
    # 1 根据需求, 构造 sentence_dict
    csv = all_raw_csv["raw_qr_transaction_by_amount_of_money"]

    csv['proportion'] = csv['cnt_today'] / csv['cnt_today'].sum()
    csv['avg_cnt'] = csv['cnt_today'] / csv['mchnt_today']
    csv['proportion'] = csv['proportion'].apply(lambda x: format(float(x), '.2%'))
    csv = csv.loc[:, ['金额', 'cnt_today', 'proportion', 'ratio', 'mchnt_today', 'avg_cnt']]

    # 把 csv 按照 10元以下 / 10-50元 / 50-100元 / 100-1000元 / 1000元以上 的顺序, 重新排序
    sort_res = True
    sorted_csv = pd.DataFrame(columns=csv.columns)
    try:
        sorted_data = []
        sort_index = ["10元以下", "10-50元", "50-100元", "100-1000元", "1000元以上"]
        for i in sort_index:
            sorted_data.append(csv[csv['金额'] == i].values[0])

        for j in range(len(sorted_data)):
            sorted_csv.loc[j] = sorted_data[j]
    except Exception as e:
        sort_res = False
        print("在qr.py文件中, 运行 qr_transaction_by_amount_of_money 函数时, 对csv根据 金额 排序时, 失败了.")
        print("失败的具体原因: %s" % traceback.format_exc())

    # data -> 即十元以下的部分, 用来生成句子 target_text 的
    data = str(csv['proportion'][csv['金额'] == '10元以下'].values[0])
    target_text = "3、交易金额整体偏低，交易金额在10元以下的占比达%s。" % data

    # 2 todo sentence df -> 暂时用 tmp_sentence_dict, 以后有时间再完善 sentence_dict
    tmp_sentence_dict = {"value": target_text}
    sentence_df = transfer_sentence_dict_to_dataframe(sentence_dict=tmp_sentence_dict, pandas_col_name="sentence")

    # 3 构造 final_csv
    final_csv = sorted_csv if sort_res is True else csv

    # 4 结果
    res = {"sentence": sentence_df,
           "csv": final_csv}

    return res
