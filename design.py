import pandas as pd


def main():
    """
    云闪付APP交易情况日报 的设计思路

    一共3个大模块, 分别是
    1 总体交易情况
        1.1 概述 --> 这一般是2-3段文字
            a. 涉及的原始csv数据 - raw_overview.csv
        1.2 支付类交易情况 --> 一段文字 + 一个表格, 表名暂定 transaction_cnt_by_day.csv
            a. 原始csv - raw_transaction_cnt_by_day.csv


    2 二维码交易情况
        2.1 概述 --> 一般是一句文字.
            a. 原始csv数据 - raw_overview.csv

        2.2 主要场景交易情况 --> 一段文字 + 一个表 qr_transaction_cnt_by_scene.csv
            a. 原始csv数据 1 - raw_qr_transaction_cnt_by_scene.csv
            b. 原始csv数据 2 - raw_qr_transaction_by_merchant_2020_01_19 02_32_57 PM.csv

        2.3 二维码TOP10分公司交易情况 --> 一段文字 + 一个表 qr_transaction_by_area_cd.csv
            a. 原始csv数据 - raw_qr_transaction_by_area_cd.csv

        2.4 二维码TOP10商户交易情况 --> 一段文字 + 一张表 qr_transaction_by_merchant.csv
            a. 原始csv数据 1 - raw_qr_transaction_by_merchant_2020_01_19 02_32_57 PM.csv
            b. 原始csv数据 2 - raw_qr_transaction_by_merchant_日期-1.csv (注意，是昨天的相同的表)

        2.5 二维码交易金额分布 --> 一段文字 + 一个表格 qr_transaction_by_amount_of_money.csv
            a. 原始csv数据 1 - raw_qr_transaction_by_amount_of_money.csv


    3 手机支付控件交易情况
        3.1 概述 --> 一段文字
            a. 原始csv数据 - raw_overview.csv

        3.2 手机支付控件TOP10商户交易情况 --> 一段文字 + 2张表 control_transaction_top_10_merchant.csv / control_out_transaction_top_10_merchant.csv
            a. 原始csv数据 1 - raw_control_transaction_top10_merchant_2020-01-20 09_49_49 AM.csv
            b. 原始csv数据 2 - raw_control_out_transaction_top10_merchant_2020-01-20 09_20_47 AM.csv

        3.3 手机外部支付控件TOP10商户侧分公司交易情况 --> 一段文字 + 一张表 control_out_by_area_cd.csv
            a. 原始csv数据 1 - raw_control_out_by_area_cd.csv

        3.4 手机外部支付控件TOP10用户侧分公司交易情况 --> 一段文字 + 一张表 control_out_by_user_gps.csv
            a. 原始csv数据 1 - raw_control_out_by_user_gps.csv

        3.5 手机外部支付控件交易金额分布 --> 一段文字 + 一张表 control_out_transaction_by_amount_of_money.csv
            a. 原始csv数据 1 - raw_control_out_transaction_by_amount_of_money.csv

    最终返回
    res = {

    }
    """
    res = {
        "total_transaction_condition": {
            "model_id": 1,
            "model_cn_name": "总体交易情况",

            "overview": dict(),
            "tables": {
                "transaction_cnt_by_day": {
                    "id": 1,
                    "cn_name": "支付类交易情况",
                    "sentence": str(),
                    "excel": [pd.DataFrame()]
                }
            }
        },

        "qr_transaction_condition": {
            "model_id": 2,
            "model_cn_name": "二维码交易情况",

            "overview": dict(),
            "tables": {
                "qr_transaction_cnt_by_scene": {
                    "id": 1,
                    "cn_name": "主要场景交易情况",
                    "sentence": str(),
                    "excel": [pd.DataFrame()]
                },
                "qr_transaction_by_area_cd": {
                    "id": 2,
                    "cn_name": "二维码TOP10分公司交易情况",
                    "sentence": str(),
                    "excel": [pd.DataFrame()]
                },
                "qr_transaction_by_merchant": {
                    "id": 3,
                    "cn_name": "二维码TOP10商户交易情况",
                    "sentence": str(),
                    "excel": [pd.DataFrame()]
                },
                "qr_transaction_by_amount_of_money": {
                    "id": 4,
                    "cn_name": "二维码交易金额分布",
                    "sentence": str(),
                    "excel": [pd.DataFrame()]
                }
            }
        },

        "control_transaction_condition": {
            "model_id": 3,
            "model_cn_name": "手机支付控件交易情况",

            "overview": dict(),
            "tables": {
                # 这里需要返回2张表，通过2个sheet的方式，写到同一个excel中.
                "control_transaction_top_10_merchant": {
                    "id": 1,
                    "cn_name": "手机支付控件TOP10商户交易情况",
                    "sentence": str(),
                    "excel": [pd.DataFrame()]
                },
                "control_out_transaction_by_area_cd": {
                    "id": 2,
                    "cn_name": "手机外部支付控件TOP10商户侧分公司交易情况",
                    "sentence": str(),
                    "excel": [pd.DataFrame()]
                },
                "control_out_transaction_by_user_gps": {
                    "id": 3,
                    "cn_name": "手机外部支付控件TOP10用户侧分公司交易情况",
                    "sentence": str(),
                    "excel": [pd.DataFrame()]
                },
                "control_out_transaction_by_amount_of_money": {
                    "id": 4,
                    "cn_name": "手机外部支付控件交易金额分布",
                    "sentence": str(),
                    "excel": [pd.DataFrame()]
                }
            }
        }
    }
