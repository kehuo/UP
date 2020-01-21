import json
import pandas as pd
from common.utils import build_date_str, can_load
from core.logic.model_1 import Overview1, TransactionCntByDay
from core.logic.model_2 import Overview2, QrTransactionCntByScene
import os


class BaseClass(object):
    """
    该类 是3个模块的父类, 定义通用的属性和方法
    """

    def __init__(self, cfg_path):
        with open(cfg_path, "r", encoding="utf-8") as f:
            self.cfg = json.load(f)

        self.csv_data = {}
        self.required_csv_name_list = [
            "raw_overview",
            "raw_transaction_cnt_by_day",

            "raw_qr_transaction_cnt_by_scene",
            "raw_qr_transaction_by_merchant",
            "raw_qr_transaction_by_area_cd",
            "raw_qr_transaction_by_amount_of_money",
            "raw_qr_transaction_cnt_by_scene_top100_in_city",
            "raw_qr_transaction_by_city",
            "raw_qr_transaction_top10_merchant",

            "raw_control_by_merchant_details",
            "raw_control_out_by_area_cd",
            "raw_control_out_by_user_gps",
            "raw_control_out_transaction_by_amount_of_money"
        ]
        return

    def load_csv_data(self, device_type):
        """
        读取 self.required_csv_name_list 列出的所有csv
        device_type = "windows" or "macbook"
        """
        path = self.cfg["raw_csv_path"][device_type]
        today_time_str = build_date_str(minus_day_count=1, str_type="middle_line")
        all_raw_csv_files = os.listdir(path)

        for required_one in self.required_csv_name_list:
            the_bingo_one = can_load(all_raw_csv_files, required_one, today_time_str)
            if the_bingo_one is not None:
                self.csv_data[required_one] = pd.read_csv(path + the_bingo_one)
        print("数据读取完成, 一共从%s读取%d个csv文件" % (path, len(self.csv_data)))
        return

    def _handle_model_1(self):
        """
        1 处理 总体交易情况
        1.1 概述 --> 这一般是2-3段文字
            a. 涉及的原始csv数据 - raw_overview.csv
        1.2 支付类交易情况 --> 一段文字 + 一个表格, 表名暂定 transaction_cnt_by_day.csv
            a. 原始csv - raw_transaction_cnt_by_day.csv

        res = {
            "overview": pd.DataFrame,
            "transaction_cnt_by_day": {
                    "sentence": pd.DataFrame(),
                    "csv": pd.DataFrame()
                }
        }
        """
        res = dict()
        # 1 overview
        overview_handler = Overview1(
            raw_csv=self.csv_data["raw_overview"],
            cfg=self.cfg
        )
        res["overview"] = overview_handler.run()
        print(res["overview"])

        # 2 transaction_cnt_by_day
        transaction_cnt_by_day_handler = TransactionCntByDay(
            raw_csv=self.csv_data["raw_transaction_cnt_by_day"],
            cfg=self.cfg
        )
        res["transaction_cnt_by_day"] = transaction_cnt_by_day_handler.run()
        print(res["transaction_cnt_by_day"])
        return res

    def _handle_model_2(self):
        """
        2 处理 二维码交易情况
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


        res = {
            "overview": pd.DataFrame(),

            "transaction_cnt_by_scene": {
                    "sentence": pd.DataFrame(),
                    "csv": pd.DataFrame()
                },

            "qr_transaction_by_area_cd": {
                    "sentence": pd.DataFrame(),
                    "csv": pd.DataFrame()
                },

            "qr_transaction_by_merchant": {
                    "sentence": pd.DataFrame(),
                    "csv": pd.DataFrame()
                },

            "qr_transaction_by_amount_of_money": {
                    "sentence": pd.DataFrame(),
                    "csv": pd.DataFrame()
                }
        }
        """
        res = dict()
        # 1 overview
        overview_handler = Overview2(
            raw_csv=self.csv_data["raw_overview"],
            cfg=self.cfg
        )
        res["overview"] = overview_handler.run()

        # 2 transaction_cnt_by_scene
        transaction_cnt_by_day_handler = QrTransactionCntByScene(
            raw_csv={"raw_qr_transaction_cnt_by_scene": self.csv_data["raw_qr_transaction_cnt_by_scene"],
                     "raw_qr_transaction_by_merchant": self.csv_data["raw_qr_transaction_by_merchant"]},
            cfg=self.cfg
        )
        res["transaction_cnt_by_scene"] = transaction_cnt_by_day_handler.run()

        # 3 qr_transaction_by_area_cd

        return res

    def _handle_model_3(self):
        """
        3 处理 手机支付控件交易情况
        3.1 概述 --> 一段文字
            a. 原始csv数据 - raw_overview.csv

        3.2 手机支付控件TOP10商户交易情况 --> 一段文字 + 2张表 control_transaction_top_10_merchant.csv / control_out_transaction_top_10_merchant.csv
            a. 原始csv数据 1 - raw_control_transaction_by_merchant_details.csv

        3.3 手机外部支付控件TOP10商户侧分公司交易情况 --> 一段文字 + 一张表 control_out_transaction_by_area_cd.csv
            a. 原始csv数据 1 - raw_control_out_transaction_by_area_cd.csv

        3.4 手机外部支付控件TOP10用户侧分公司交易情况 --> 一段文字 + 一张表 control_out_transaction_by_user_gps.csv
            a. 原始csv数据 1 - raw_control_out_transaction_by_user_gps.csv

        3.5 手机外部支付控件交易金额分布 --> 一段文字 + 一张表 control_out_transaction_by_amount_of_money.csv
            a. 原始csv数据 1 - raw_control_out_transaction_by_amount_of_money.csv"""
        res = {}
        return res

    def run(self):
        """
        model_1: 总体交易情况
        model_2: 二维码交易情况
        model_3: 手机支付控件交易情况
        """

        res_model_1 = self._handle_model_1()
        res_model_2 = self._handle_model_2()
        res_model_3 = self._handle_model_3()
        return
