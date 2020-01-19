import json
from datetime import datetime, timedelta
import pandas as pd
from common.utils import build_date_str
import os


class BaseClass(object):
    """
    该类 用来生成 云闪付APP交易情况日报
    """

    def __init__(self, cfg_path, model_type=None):
        with open(cfg_path, "r", encoding="utf-8") as f:
            self.cfg = json.load(f)
        self.model_type = model_type if model_type else None
        self.csv_data = {}
        return

    def _load_csv_data(self):
        """根据 model_type, 从cfg.json 中找到自己需要的csv的文件名, 并加载csv数据"""
        path = self.cfg["raw_csv_path"]
        today_time_str = build_date_str(minus_day_count=0, str_type="bottom_line")

        for k, v in self.cfg["csv_data"].items():
            if k == self.model_type:

                for target_csv, raw_csv_list in v.items():
                    # 有一个的读今天的, 有两个的读今天 和 昨天的
                    if len(raw_csv_list) == 1:
                        # todo 读的时候，用 raw_csv_list[0] 和 datetime.now() - timedelta(days=1) 2个条件过滤

                        for root_path, dir_list, os_file_name_list in os.walk(path):
                            for file_one in os_file_name_list:
                                if (raw_csv_list[0] in file_one) and (today_time_str in file_one):
                                    self.csv_data[k] = pd.read_csv(path + raw_csv_list[0])
        return

    def run(self):
        return


class TotalDailyReportCreator(BaseClass):
    """处理 总体交易情况"""
    def __init__(self, cfg_path, model_type):
        BaseClass.__init__(self, cfg_path, model_type)

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


def main():
    cfg_path = "/users/hk/dev/UP/"
    cfg_name = "daily_report_cfg.json"
    daily_report_creator = TotalDailyReportCreator(cfg_path + cfg_name, model_type="total")
    daily_report_creator.run()


if __name__ == '__main__':
    main()
