import json
import os

import pandas as pd

from common.utils import build_date_str, can_load
from core.logic.overview import Overview
from core.logic.general import General


class DailyReportProcessor(object):
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

            "raw_control_transaction_top10_merchant",
            "raw_control_out_transaction_top10_merchant",
            "raw_control_out_by_area_cd",
            "raw_control_out_by_user_gps",
            "raw_control_out_transaction_by_amount_of_money"
        ]

        self.res_model = {
            "total": dict(),
            "qr": dict(),
            "control": dict()
        }

        self.overview_handler = None
        self.general_handler = None

        return

    def load_csv_data(self, device_type):
        """
        读取 self.required_csv_name_list 列出的所有csv
        device_type = "windows" or "linux"

        minus_day_count = 今天 - 几天前的csv数据, 在 cfg.json 中配置。 举例:
        如果今天 = 1月20日, minux_day_count = 2, 那么取的就是 1月18日的csv文件.
        """
        path = self.cfg["raw_csv_path"][device_type]
        today_time_str = build_date_str(minus_day_count=self.cfg["minus_day_count"],
                                        str_type="middle_line")
        all_raw_csv_files = os.listdir(path)

        for required_one in self.required_csv_name_list:
            the_bingo_one = can_load(all_raw_csv_files, required_one, today_time_str)
            if the_bingo_one is not None:
                self.csv_data[required_one] = pd.read_csv(path + the_bingo_one)

        print("数据读取完成, 一共从%s读取%d个csv文件" % (path, len(self.csv_data)))
        return

    def _init_handler(self):
        self.overview_handler = Overview(self.csv_data, self.cfg)
        self.general_handler = General(self.csv_data, self.cfg)

    def run(self):
        """
        日报共 3 个model --> 总体交易情况(total) / 二维码交易情况(qr) / 手机支付控件交易情况(control)

        1 总体交易情况 - total
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


        2 二维码交易情况 - qr
        2.1 概述 --> 一般是一句文字.
            a. 原始csv数据 - raw_overview.csv

        2.2 主要场景交易情况 --> 一段文字 + 一个表 qr_transaction_cnt_by_scene.csv
            a. 原始csv数据 1 - raw_qr_transaction_cnt_by_scene.csv
            b. 原始csv数据 2 - raw_qr_transaction_by_merchant.csv

        2.3 二维码TOP10分公司交易情况 --> 一段文字 + 一个表 qr_transaction_by_area_cd.csv
            a. 原始csv数据 - raw_qr_transaction_by_area_cd.csv

        2.4 二维码TOP10商户交易情况 --> 一段文字 + 一张表 qr_transaction_by_merchant.csv
            a. 原始csv数据 1 - raw_qr_transaction_by_merchant_2020_01_19 02_32_57 PM.csv
            b. 原始csv数据 2 - raw_qr_transaction_by_merchant_日期-1.csv (注意，是昨天的相同的表)

        2.5 二维码交易金额分布 --> 一段文字 + 一个表格 qr_transaction_by_amount_of_money.csv
            a. 原始csv数据 1 - raw_qr_transaction_by_amount_of_money.csv

        res = {
            "overview": pd.DataFrame(),

            "qr_transaction_cnt_by_scene": {
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

        3 手机支付控件交易情况
        3.1 概述 --> 一段文字
            a. 原始csv数据 - raw_overview.csv

        3.2 手机支付控件TOP10商户交易情况 --> 一段文字 + 1张表 control_transaction_top_10_merchant.csv
            a. 原始csv数据 1 - raw_control_transaction_top10_merchant_2020-01-20 09_49_49 AM.csv

        3.3 手机外部支付控件TOP10商户交易情况 --> 一段文字 + 1张表 control_out_transaction_top_10_merchant.csv
            a. 原始csv数据 1 - raw_control_transaction_top10_merchant_2020-01-20 09_49_49 AM.csv

        3.4 手机外部支付控件TOP10商户侧分公司交易情况 --> 一段文字 + 一张表 control_out_by_area_cd.csv
            a. 原始csv数据 1 - raw_control_out_by_area_cd.csv

        3.5 手机外部支付控件TOP10用户侧分公司交易情况 --> 一段文字 + 一张表 control_out_by_user_gps.csv
            a. 原始csv数据 1 - raw_control_out_by_user_gps.csv

        3.6 手机外部支付控件交易金额分布 --> 一段文字 + 一张表 control_out_transaction_by_amount_of_money.csv
            a. 原始csv数据 1 - raw_control_out_transaction_by_amount_of_money.csv
        """

        self._init_handler()

        # 1 定义3个模块要构造的 services
        general_service_map = {
            "total": ["transaction_cnt_by_day"],

            "qr": ["qr_transaction_cnt_by_scene",
                   "qr_transaction_by_area_cd",
                   "qr_transaction_by_merchant",
                   "qr_transaction_by_amount_of_money"],

            "control": ["control_transaction_top10_merchant",
                        "control_out_transaction_top10_merchant",
                        "control_out_by_area_cd",
                        "control_out_by_user_gps",
                        "control_out_transaction_by_amount_of_money"]
        }

        # 2 要构造的所有 model 类型
        model_types = ["total", "qr", "control"]
        for model_type in model_types:
            res = dict()
            # overview
            res["overview"] = self.overview_handler.run(model_type=model_type)

            # general
            for service in general_service_map[model_type]:
                res[service] = self.general_handler.run(model_type=model_type, service_type=service)
            # 写入
            self.res_model[model_type] = res

    def concat(self, device_type):
        """
        将 res_model 1/2/3 的所有结果, 写入同一个excel 的多个 sheet 中
        device_type = linux / windows
        """
        finale_excel_path = self.cfg["final_excel_path"][device_type]
        final_excel_name = self.cfg["final_excel_name"]
        writer = pd.ExcelWriter(finale_excel_path + final_excel_name)

        # 遍历 self.res_model_1/2/3 中的所有 key-value 对, 将每一个csv 作为一个 sheet, 写入 writer
        for model_k, model_v in self.res_model.items():
            # model_k = "1", model_v = 一个字典
            for k, v in model_v.items():
                # k = "overview", v可能是dataframe, 也可能是一个字典, 里面包括多个dataframe
                if isinstance(v, dict):
                    # v 是字典, 包括多个dataframe
                    for each_k, each_v in v.items():
                        if isinstance(each_v, pd.DataFrame):
                            total_sheet_name = "model" + model_k + "_" + k + "_" + each_k
                            each_v.to_excel(excel_writer=writer, sheet_name=total_sheet_name)

                elif isinstance(v, pd.DataFrame):
                    v.to_excel(excel_writer=writer, sheet_name="model" + model_k + "_" + k)
        writer.save()
        writer.close()
