import traceback
from common.utils import build_date_str, find_df_value, transfer_sentence_dict_to_dataframe, str2number


class Overview(object):
    def __init__(self, raw_csv, cfg):
        """
        raw_csv: data/raw/raw_overview.csv
        cfg: cfg.json

        self.data: 字典类型. 因为 overview 需要提前计算一些数据, 来填满一段文字中的数据. 这个变量用来存储计算出来的各种数值.
        self.sentence_dict: 字典类型. 是一段文字的结构化形式. 初始是一个空字典, 之后在 _init_sentence_dict 方法中进一步处理.
        """
        self.raw_csv = raw_csv["raw_overview"]
        self.cfg = cfg

        self.data = {}
        self.sentence_dict = {}

    def _init_sentence_dict(self, model_type):
        """
        model_type: total / qr / control 一共3种.

        total - 总体交易情况
        qr - 二维码交易情况
        control - 手机支付控件交易情况
        """

        model_sentence_map = {
            "total": {
                # 第一段
                "yesterday_date": "",
                "all_merchant_cnt": "",
                "new_merchant_cnt": "",
                "new_merchant_cluster_area": "",

                # 第二段
                "qr_code_merchant_cnt": "",
                "control_merchant": "",
                "control_out_merchant": ""
            },

            "qr": {
                "value": ""
            },

            "control": {
                "value": ""
            }
        }

        self.sentence_dict = model_sentence_map[model_type]

    def begin_time(self):
        # model 1.1 -- 日报最开头的时间 (昨天的日期)
        self.sentence_dict["yesterday_date"] = build_date_str(minus_day_count=self.cfg["minus_day_count"],
                                                              str_type="cn")

    def all_merchant_cnt(self):
        # model 1.2 -- 总体交易商户
        data = {
            "1": find_df_value(self.raw_csv, col="cnt_today", row="all_mchnt_cnt"),
            "2": find_df_value(self.raw_csv, col="ratio_by_yesterday", row="all_mchnt_cnt"),
            "3": find_df_value(self.raw_csv, col="ration_by_last_year", row="all_mchnt_cnt")
        }

        # 把 表格里的str 全部转成 int 或者 float 数字类型, 否则下面对str进行 round 操作时, 会报错说字符串不支持加减乘除的数字运算.
        if self.cfg["csv_encode_type"] in ["utf-16", "utf-8"]:
            data = str2number(data)

        self.data["all_merchant_cnt"] = data
        self.sentence_dict["all_merchant_cnt"] = "云闪付APP总体交易商户%s万, 环比下降%s, 同比增长%s。" % (
            str(round(data["1"] / 10000, 2)),
            str(round(data["2"] * 100, 2)) + "%",
            str(round(data["3"] * 100, 2)) + "%",
        )

    def new_merchant_cnt(self):
        # model 1.3 新增交易商户
        data = {
            "1": find_df_value(self.raw_csv, col="cnt_today", row="new_mchnt_cnt"),
            "2": find_df_value(self.raw_csv, col="ratio_by_yesterday", row="new_mchnt_cnt"),
            "3": find_df_value(self.raw_csv, col="ration_by_last_year", row="new_mchnt_cnt")
        }

        if self.cfg["csv_encode_type"] in ["utf-16", "utf-8"]:
            data = str2number(data)

        self.data["new_merchant_cnt"] = data
        self.sentence_dict["new_merchant_cnt"] = "当日新增交易商户%s家, 环比下降%s, 同比增长%s。" % (
            str(round(data["1"] / 10000, 2)),
            str(round(data["2"] * 100, 2)) + "%",
            str(round(data["3"] * 100, 2)) + "%",
        )

    def new_merchant_cluster_area(self):
        # model 1.4 新增商户集中地区 (从 cfg.json 中读取)
        data = self.cfg["model_1"]["overview"]["新增商户集中地区"]

        self.data["new_merchant_cluster_area"] = data
        self.sentence_dict["new_merchant_cluster_area"] = "新增商户主要集中在%s、%s、%s等地区。" % (
            data[0],
            data[1],
            data[2]
        )

    # 以下是第二段
    def qr_code_merchant_cnt(self):
        # model 1.5 二维码交易商户
        data = {
            "1": find_df_value(self.raw_csv, col="cnt_today", row="qr_code_mchnt_cnt"),
            "2": find_df_value(self.raw_csv, col="cnt_today", row="qr_code_mchnt_cnt") / self.data["all_merchant_cnt"][
                "1"],
            "3": find_df_value(self.raw_csv, col="ratio_by_yesterday", row="qr_code_mchnt_cnt")
        }

        if self.cfg["csv_encode_type"] in ["utf-16", "utf-8"]:
            data = str2number(data)

        self.data["qr_code_merchant_cnt"] = data
        self.sentence_dict["qr_code_merchant_cnt"] = "二维码交易商户%s万, 占总交易商户的%s, 环比下降%s;" % (
            str(round(data["1"] / 10000, 2)),
            str(round(data["2"] * 100, 2)) + "%",
            str(round(data["3"] * 100, 2)) + "%",
        )

    def control_merchant(self):
        # model 1.6 手机支付控件交易商户
        data = {
            "1": find_df_value(self.raw_csv, col="cnt_today", row="control_mchnt"),
            "2": find_df_value(self.raw_csv, col="cnt_today", row="control_mchnt") / self.data["all_merchant_cnt"]["1"],
            "3": find_df_value(self.raw_csv, col="ratio_by_yesterday", row="control_mchnt")
        }

        if self.cfg["csv_encode_type"] in ["utf-16", "utf-8"]:
            data = str2number(data)

        self.data["control_merchant"] = data
        self.sentence_dict["control_merchant"] = "手机支付控件交易商户%s家, 占总交易商户的%s, 环比下降%s;" % (
            str(data["1"]),
            str(round(data["2"] * 100, 2)) + "%",
            str(round(data["3"] * 100, 2)) + "%",
        )

    def control_out_merchant(self):
        # model 1.7 手机外部支付控件交易商户
        data = {
            "1": find_df_value(self.raw_csv, col="cnt_today", row="control_out_mchnt"),
            "2": find_df_value(self.raw_csv, col="ratio_by_yesterday", row="control_out_mchnt")
        }

        if self.cfg["csv_encode_type"] in ["utf-16", "utf-8"]:
            data = str2number(data)

        self.data["control_out_merchant"] = data
        self.sentence_dict["control_out_merchant"] = "手机外部支付交易商户%s家, 环比下降%s;" % (
            str(data["1"]),
            str(round(data["2"] * 100, 2)) + "%"
        )

    # todo -- model 2 qr / model 3 control 的相关函数的编写
    # 2020-02-08 注释 - model 2的 qr 暂时不需要 overview 字段, 只写control的 overview 函数即可.
    def model_3(self):
        """
        手机控件交易情况
        """

        # model 3.1 手机控件交易描述
        df_overview = self.raw_csv

        control_cnt = df_overview['cnt_today'][df_overview['index'] == 'control_cnt'].values[0]
        control_cnt_by_yesterday = df_overview['ratio_by_yesterday'][df_overview['index'] == 'control_cnt'].values[0]
        control_cnt_by_last_year = df_overview['ration_by_last_year'][df_overview['index'] == 'control_cnt'].values[0]

        control_out_cnt = df_overview['cnt_today'][df_overview['index'] == 'control_out_cnt'].values[0]
        control_out_cnt_by_yesterday = df_overview['ratio_by_yesterday'][df_overview['index'] == 'control_out_cnt'].values[0]
        control_out_cnt_by_last_year = df_overview['ration_by_last_year'][df_overview['index'] == 'control_out_cnt'].values[0]

        target_text = "当日，手机支付控件交易{}万笔，环比下降{}%，同比下降{}%。其中手机外部支付控件交易{}万笔，环比增长{}%，同比下降{}%，占总控件交易笔数的{}%。".format(
            round(control_cnt / 10000, 2),
            round(control_cnt_by_yesterday * 100, 2),
            round(float(control_cnt_by_last_year) * 100, 2),
            round(control_out_cnt / 10000, 2),
            round(control_out_cnt_by_yesterday * 100, 2),
            round(float(control_out_cnt_by_last_year) * 100, 2),
            round(control_out_cnt / control_cnt * 100, 2)
        )

        self.sentence_dict["model_3"] = target_text

    def run(self, model_type):
        run_func_map = {
            "total": [
                # 第一段
                self.begin_time,
                self.all_merchant_cnt,
                self.new_merchant_cnt,
                self.new_merchant_cluster_area,

                # 第二段
                self.qr_code_merchant_cnt,
                self.control_merchant,
                self.control_out_merchant
            ],

            "qr": [],

            # 懒得处理 sentence_dict了, 直接在一个 model_3 函数中处理完成
            "control": [self.model_3]
        }

        # 根据 model type 初始化 sentence_dict
        self._init_sentence_dict(model_type)

        # 根据 model 类型 运行对应的函数
        res = None
        if len(run_func_map[model_type]) > 0:
            for func in run_func_map[model_type]:
                func()

            # 将这段文字构造成 DataFrame, 返回.
            res = transfer_sentence_dict_to_dataframe(self.sentence_dict, pandas_col_name="overview")
        return res
