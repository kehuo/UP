from common.utils import build_date_str, find_df_value
import pandas as pd


def overview(raw_csv_data, cfg):
    # 1 时间
    raw_csv = raw_csv_data["raw_overview"]
    yesterday_date_str = build_date_str(minus_day_count=1, str_type="cn")

    # 2 总体交易商户
    all_merchant_cnt_data = {
        "1": find_df_value(raw_csv, col="cnt_today", row="all_mchnt_cnt"),
        "2": find_df_value(raw_csv, col="ratio_by_yesterday", row="all_mchnt_cnt"),
        "3": find_df_value(raw_csv, col="ration_by_last_year", row="all_mchnt_cnt")
    }
    all_merchant_cnt_str = "云闪付APP总体交易商户%s万, 环比下降%s, 同比增长%s。" % (
        str(round(all_merchant_cnt_data["1"] / 10000, 2)),
        str(round(all_merchant_cnt_data["2"] * 100, 2)) + "%",
        str(round(all_merchant_cnt_data["3"] * 100, 2)) + "%",
    )

    # 3 新增交易商户
    new_merchant_cnt_data = {
        "1": find_df_value(raw_csv, col="cnt_today", row="new_mchnt_cnt"),
        "2": find_df_value(raw_csv, col="ratio_by_yesterday", row="new_mchnt_cnt"),
        "3": find_df_value(raw_csv, col="ration_by_last_year", row="new_mchnt_cnt")
    }
    new_merchant_cnt_str = "当日新增交易商户%s+, 环比下降%s, 同比增长%s。" % (
        str(round(new_merchant_cnt_data["1"] / 10000, 2)),
        str(round(new_merchant_cnt_data["2"] * 100, 2)) + "%",
        str(round(new_merchant_cnt_data["3"] * 100, 2)) + "%",
    )

    # 4 新增商户集中地区 (从 cfg.json 中读取)
    new_merchant_cluster_area_data = cfg["model_1"]["overview"]["新增商户集中地区"]
    new_merchant_cluster_area_str = "新增商户主要集中在%s、%s、%s等地区。" % (
        new_merchant_cluster_area_data[0],
        new_merchant_cluster_area_data[1],
        new_merchant_cluster_area_data[2]
    )

    # 以下是第二段
    # 5 二维码交易商户
    qr_code_merchant_cnt_data = {
        "1": find_df_value(raw_csv, col="cnt_today", row="qr_code_mchnt_cnt"),
        "2": find_df_value(raw_csv, col="cnt_today", row="qr_code_mchnt_cnt") / all_merchant_cnt_data["1"],
        "3": find_df_value(raw_csv, col="ratio_by_yesterday", row="qr_code_mchnt_cnt")
    }
    qr_code_merchant_cnt_str = "二维码交易商户%s万, 占总交易商户的%s, 环比下降%s;" % (
        str(round(qr_code_merchant_cnt_data["1"] / 10000, 2)),
        str(round(qr_code_merchant_cnt_data["2"] * 100, 2)) + "%",
        str(round(qr_code_merchant_cnt_data["3"] * 100, 2)) + "%",
    )

    # 6 手机支付控件交易商户
    control_merchant_data = {
        "1": find_df_value(raw_csv, col="cnt_today", row="control_mchnt"),
        "2": find_df_value(raw_csv, col="cnt_today", row="control_mchnt") / all_merchant_cnt_data["1"],
        "3": find_df_value(raw_csv, col="ratio_by_yesterday", row="control_mchnt")
    }
    control_merchant_str = "手机支付控件交易商户%s家, 占总交易商户的%s, 环比下降%s;" % (
        str(control_merchant_data["1"]),
        str(round(control_merchant_data["2"] * 100, 2)) + "%",
        str(round(control_merchant_data["3"] * 100, 2)) + "%",
    )

    # 7 手机外部支付控件交易商户
    control_out_merchant_data = {
        "1": find_df_value(raw_csv, col="cnt_today", row="control_out_mchnt"),
        "2": find_df_value(raw_csv, col="ratio_by_yesterday", row="control_out_mchnt")
    }
    control_out_merchant_str = "手机外部支付交易商户%s家, 环比下降%s;" % (
        str(control_out_merchant_data["1"]),
        str(round(control_out_merchant_data["2"] * 100, 2)) + "%"
    )
    res = {
        # 第一段
        "yesterday_date": yesterday_date_str,
        "all_merchant_cnt": all_merchant_cnt_str,
        "new_merchant_cnt": new_merchant_cnt_str,
        "new_merchant_cluster_area": new_merchant_cluster_area_str,

        # 第二段
        "qr_code_merchant_cnt": qr_code_merchant_cnt_str,
        "control_merchant": control_merchant_str,
        "control_out_merchant": control_out_merchant_str
    }
    all_str = ""
    for k, v in res.items():
        all_str += v
    print(all_str)

    df_data = {"str": all_str}
    # 放到 dataframe 中
    df = pd.DataFrame(data=df_data)

    print("model_1_overview")
    print(df)
    return df


def transaction_cnt_by_day(raw_csv_data):
    res = {}
    """
    当日，云闪付APP发生支付类交易1133.76万笔，其中被扫、乘车码、远程转账、信用卡还款、一般主扫、快速收款码、小微主扫、手机外部支付控件、
    无感支付、人到人转账交易笔数排名前十，占到交易总量的98.94%。
    """
    raw_df = raw_csv_data["raw_transaction_cnt_by_day"]
    raw_df["ratio"] = raw_df["ratio"].apply(lambda x: format(float(x), ".2%"))
    raw_df["proportion"] = raw_df["cnt_today"] / raw_df["cnt_today"].sum()
    raw_df["proportion"] = raw_df["proportion"].apply(
        lambda x: format(float(x), ".2%")
    )
    raw_df = raw_df.loc[:, ["index", "cnt_today", "proportion", "ratio"]]

    return res
