import json
import pandas as pd
from common.utils import build_date_str, can_load
from core.logic.model_1 import Overview1, TransactionCntByDay
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

    def load_csv_data(self):
        """读取 self.required_csv_name_list 列出的所有csv"""
        path = self.cfg["raw_csv_path"]
        today_time_str = build_date_str(minus_day_count=0, str_type="middle_line")
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

        参数解释
        required_raw_csv: 需要的原始数据
        """
        res = dict()
        # 1 overview
        model_1_overview_handler = Overview1(self.csv_data["raw_overview"], self.cfg)
        res["overview"] = model_1_overview_handler.run()

        # 2 transaction_cnt_by_day
        transaction_cnt_by_day_handler = TransactionCntByDay(self.csv_data["raw_transaction_cnt_by_day"], self.cfg)
        res["transaction_cnt_by_day"] = transaction_cnt_by_day_handler.run()
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
        """
        res = {}
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
        print(self.cfg)
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


class TotalDailyReportCreator(BaseClass):
    """处理 总体交易情况"""
    def __init__(self, cfg_path):
        BaseClass.__init__(self, cfg_path)

    def run(self):
        def _overview():
            # 1 时间
            yesterday_date_str = build_date_str(minus_day_count=1, str_type="cn")

            # 2 总体交易商户
            all_merchant_cnt = {"yesterday": 269654,
                                "today": 410180,
                                "same_today_last_year": 411636}
            all_merchant_cnt_str = "云闪付APP总体交易商户%s万, 环比下降%s, 同比增长%s。" % (
                str(round(all_merchant_cnt["today"] / 10000, 2)),
                str(round(((all_merchant_cnt["today"] / all_merchant_cnt["yesterday"]) - 1) * 100, 2)) + "%",
                str(round(((all_merchant_cnt["today"] / all_merchant_cnt["same_today_last_year"]) - 1) * 100, 2)) + "%"
            )

            # 3 新增交易商户
            new_merchant_cnt = {"yesterday": 269654,
                                "today": 410180,
                                "same_today_last_year": 411636}
            new_merchant_cnt_str = "当日新增交易商户%s+, 环比下降%s, 同比增长%s。" % (
                str(new_merchant_cnt["today"]),
                str(round(((new_merchant_cnt["today"] / new_merchant_cnt["yesterday"]) - 1) * 100, 2)) + "%",
                str(round(((new_merchant_cnt["today"] / new_merchant_cnt["same_today_last_year"]) - 1) * 100, 2)) + "%"
            )

            # 4 新增商户集中地区
            new_merchant_cluster_area = ["辽宁", "湖北", "重庆"]
            new_merchant_cluster_area_str = "新增商户主要集中在%s、%s、%s等地区。" % (
                new_merchant_cluster_area[0],
                new_merchant_cluster_area[1],
                new_merchant_cluster_area[2]
            )

            # 以下是第二段
            # 5 二维码交易商户
            qr_code_merchant_cnt = {"yesterday": 269654,
                                    "today": 410180,
                                    "total": 456789}
            qr_code_merchant_cnt_str = "二维码交易商户%s万, 占总交易商户的%s, 环比下降%s;" % (
                str(round(qr_code_merchant_cnt["today"] / 10000, 2)),
                str(round(qr_code_merchant_cnt["today"] / qr_code_merchant_cnt["total"] * 100, 2)) + "%",
                str(round(((qr_code_merchant_cnt["today"] / qr_code_merchant_cnt["yesterday"]) - 1) * 100, 2)) + "%"
            )

            # 6 手机支付控件交易商户
            control_merchant = {"yesterday": 269654,
                                "today": 410180,
                                "total": 456789}
            control_merchant_str = "手机支付控件交易商户%s家, 占总交易商户的%s, 环比下降%s;" % (
                str(control_merchant["today"]),
                str(round(control_merchant["today"] / control_merchant["total"] * 100, 2)) + "%",
                str(round(((control_merchant["today"] / control_merchant["yesterday"]) - 1) * 100, 2)) + "%"
            )

            # 7 手机外部支付控件交易商户
            control_out_merchant = {"yesterday": 269654,
                                    "today": 410180,
                                    "total": 456789}
            control_out_merchant_str = "手机外部支付交易商户%s家, 环比下降%s;" % (
                str(control_out_merchant["today"]),
                # str(round(control_out_merchant["today"] / control_out_merchant["total"] * 100, 2)) + "%",
                str(round(((control_out_merchant["today"] / control_out_merchant["yesterday"]) - 1) * 100, 2)) + "%"
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

        _overview()
        return
