from common.utils import build_date_str, find_df_value, transfer_sentence_dict_to_dataframe


class Overview(object):
    def __init__(self, raw_csv, cfg, model_type):
        """
        raw_csv: data/raw/raw_overview.csv
        cfg: cfg.json
        model_type: total / qr / control 一共3种.

        self.data: 字典类型. 因为 overview 需要提前计算一些数据, 来填满一段文字中的数据. 这个变量用来存储计算出来的各种数值.
        self.sentence_dict: 字典类型. 是一段文字的结构化形式. 初始是一个空字典, 之后在 _init_sentence_dict 方法中进一步处理.
        """
        self.raw_csv = raw_csv
        self.cfg = cfg
        self.model_type = model_type

        self.data = {}
        self.sentence_dict = {}

    def _init_sentence_dict(self):
        """
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
                "1": ""
            },

            "control": {
                "1": ""
            }
        }

        self.sentence_dict = model_sentence_map[self.model_type]

    def begin_time(self):
        # model 1.1 -- 日报最开头的时间 (昨天的日期)
        self.sentence_dict["yesterday_date"] = build_date_str(minus_day_count=1, str_type="cn")

    def all_merchant_cnt(self):
        # model 1.2 -- 总体交易商户
        data = {
            "1": find_df_value(self.raw_csv, col="cnt_today", row="all_mchnt_cnt"),
            "2": find_df_value(self.raw_csv, col="ratio_by_yesterday", row="all_mchnt_cnt"),
            "3": find_df_value(self.raw_csv, col="ration_by_last_year", row="all_mchnt_cnt")
        }

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

        self.data["new_merchant_cnt"] = data
        self.sentence_dict["new_merchant_cnt"] = "当日新增交易商户%s+, 环比下降%s, 同比增长%s。" % (
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

        self.data["control_out_merchant"] = data
        self.sentence_dict["control_out_merchant"] = "手机外部支付交易商户%s家, 环比下降%s;" % (
            str(data["1"]),
            str(round(data["2"] * 100, 2)) + "%"
        )

    # todo -- model 2 qr / model 3 control 的相关函数的编写

    def run(self):
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

            "control": []
        }

        # 根据 model 类型 运行对应的函数
        for func in run_func_map[self.model_type]:
            func()

        # 将这段文字构造成 dataframe, 返回.
        res = transfer_sentence_dict_to_dataframe(self.sentence_dict, pandas_col_name="overview")
        return res
