from common.utils import build_date_str, find_df_value
import pandas as pd


class Overview2(object):
    def __init__(self, raw_csv, cfg):
        self.raw_csv = raw_csv
        self.cfg = cfg
        self.yesterday_date_str = build_date_str(minus_day_count=1, str_type="cn")

        self.data = {}
        # todo 结构化
        self.all_str = {}

    def all_merchant_cnt(self):
        # 2 总体交易商户
        data = {
            "1": find_df_value(self.raw_csv, col="cnt_today", row="all_mchnt_cnt"),
            "2": find_df_value(self.raw_csv, col="ratio_by_yesterday", row="all_mchnt_cnt"),
            "3": find_df_value(self.raw_csv, col="ration_by_last_year", row="all_mchnt_cnt")
        }

        self.data["all_merchant_cnt"] = data
        self.all_str["all_merchant_cnt"] = "云闪付APP总体交易商户%s万, 环比下降%s, 同比增长%s。" % (
            str(round(data["1"] / 10000, 2)),
            str(round(data["2"] * 100, 2)) + "%",
            str(round(data["3"] * 100, 2)) + "%",
        )

    def new_merchant_cnt(self):
        # 3 新增交易商户
        data = {
            "1": find_df_value(self.raw_csv, col="cnt_today", row="new_mchnt_cnt"),
            "2": find_df_value(self.raw_csv, col="ratio_by_yesterday", row="new_mchnt_cnt"),
            "3": find_df_value(self.raw_csv, col="ration_by_last_year", row="new_mchnt_cnt")
        }

        self.data["new_merchant_cnt"] = data
        self.all_str["new_merchant_cnt"] = "当日新增交易商户%s+, 环比下降%s, 同比增长%s。" % (
            str(round(data["1"] / 10000, 2)),
            str(round(data["2"] * 100, 2)) + "%",
            str(round(data["3"] * 100, 2)) + "%",
        )

    def new_merchant_cluster_area(self):
        # 4 新增商户集中地区 (从 cfg.json 中读取)
        data = self.cfg["model_1"]["overview"]["新增商户集中地区"]

        self.data["new_merchant_cluster_area"] = data
        self.all_str["new_merchant_cluster_area"] = "新增商户主要集中在%s、%s、%s等地区。" % (
            data[0],
            data[1],
            data[2]
        )

    # 以下是第二段
    def qr_code_merchant_cnt(self):
        # 5 二维码交易商户
        data = {
            "1": find_df_value(self.raw_csv, col="cnt_today", row="qr_code_mchnt_cnt"),
            "2": find_df_value(self.raw_csv, col="cnt_today", row="qr_code_mchnt_cnt") / self.data["all_merchant_cnt"]["1"],
            "3": find_df_value(self.raw_csv, col="ratio_by_yesterday", row="qr_code_mchnt_cnt")
        }

        self.data["qr_code_merchant_cnt"] = data
        self.all_str["qr_code_merchant_cnt"] = "二维码交易商户%s万, 占总交易商户的%s, 环比下降%s;" % (
            str(round(data["1"] / 10000, 2)),
            str(round(data["2"] * 100, 2)) + "%",
            str(round(data["3"] * 100, 2)) + "%",
        )

    def control_merchant(self):
        # 6 手机支付控件交易商户
        data = {
            "1": find_df_value(self.raw_csv, col="cnt_today", row="control_mchnt"),
            "2": find_df_value(self.raw_csv, col="cnt_today", row="control_mchnt") / self.data["all_merchant_cnt"]["1"],
            "3": find_df_value(self.raw_csv, col="ratio_by_yesterday", row="control_mchnt")
        }

        self.data["control_merchant"] = data
        self.all_str["control_merchant"] = "手机支付控件交易商户%s家, 占总交易商户的%s, 环比下降%s;" % (
            str(data["1"]),
            str(round(data["2"] * 100, 2)) + "%",
            str(round(data["3"] * 100, 2)) + "%",
        )

    def control_out_merchant(self):
        # 7 手机外部支付控件交易商户
        data = {
            "1": find_df_value(self.raw_csv, col="cnt_today", row="control_out_mchnt"),
            "2": find_df_value(self.raw_csv, col="ratio_by_yesterday", row="control_out_mchnt")
        }

        self.data["control_out_merchant"] = data
        self.all_str["control_out_merchant"] = "手机外部支付交易商户%s家, 环比下降%s;" % (
            str(data["1"]),
            str(round(data["2"] * 100, 2)) + "%"
        )

    def run(self):
        # 第一段
        self.all_merchant_cnt()
        self.new_merchant_cnt()
        self.new_merchant_cluster_area()

        # 第二段
        self.qr_code_merchant_cnt()
        self.control_merchant()
        self.control_out_merchant()

        # 将self.all_str 从字典 转成 字符串
        all_str = ""
        for k, v in self.all_str.items():
            all_str += v
        # 转成 dataframe 后返回结果
        res = pd.DataFrame(data={"overview": [all_str]})
        return res


class QrTransactionCntByScene(object):
    def __init__(self, raw_csv, cfg):
        """
        主要场景交易情况

        raw_csv: 字典格式, 包含2个csv --  qr_transaction_cnt_by_scene / raw_qr_transaction_by_merchant

        self.all_str: 最后要生成的一段文字
        self.csv: 最后要生成的表格 - qr_transaction_cnt_by_scene
        """
        self.raw_csv = raw_csv
        self.cfg = cfg

        # todo 将文字拆成结构化的key-value对以后，为每一对写一个函数
        self.all_str = {
            "1": "",
            "2": ""
        }
        self.csv = raw_csv["raw_qr_transaction_cnt_by_scene"]

    def build_sentence(self):
        # 1 构造 self.all_str 字典
        # todo

        # 2 将字典 转为 dataframe
        sentence = ""
        for k, v in self.all_str.items():
            sentence += v
        res = pd.DataFrame(data={"sentence": [sentence]})
        return res

    def build_csv(self):
        # 构造CSV
        # todo 按照昨天的理解，csv 不需要做进一步处理，直接作为dataframe写入最终的excel即可。今晚再确认一下
        pass

    def run(self):
        """
        支付类交易情况 -- 一段文字 + 一个表格

        1 文字
        当日，云闪付APP发生支付类交易1133.76万笔，其中被扫、乘车码、远程转账、信用卡还款、一般主扫、快速收款码、小微主扫、手机外部支付控件、
        无感支付、人到人转账交易笔数排名前十，占到交易总量的98.94%。

        2 表格
        """
        # 1 文字
        sentence = self.build_sentence()

        # 2 表格
        self.build_csv()

        # 构造最终返回的结果
        res = {
            "sentence": sentence,
            "csv": self.csv
        }
        return res


class QrTransactionByAreaCd(object):
    def __init__(self, raw_csv, cfg):
        """
        二维码TOP10分公司交易情况
        
        raw_csv: 包含1个csv --  raw_qr_transaction_by_area_cd

        self.all_str: 最后要生成的一段文字
        self.csv: 最后要生成的表格 - qr_transaction_cnt_by_scene
        """
        self.raw_csv = raw_csv
        self.cfg = cfg

        # todo 将文字拆成结构化的key-value对以后，为每一对写一个函数
        self.all_str = {
            "1": "",
            "2": ""
        }
        self.csv = raw_csv["qr_transaction_cnt_by_scene"]

    def build_sentence(self):
        # 1 构造 self.all_str 字典
        # todo

        # 2 将字典 转为 dataframe
        sentence = ""
        for k, v in self.all_str.items():
            sentence += v
        res = pd.DataFrame(data={"sentence": [sentence]})
        return res

    def build_csv(self):
        # 构造CSV
        # todo 按照昨天的理解，csv 不需要做进一步处理，直接作为dataframe写入最终的excel即可。今晚再确认一下
        pass

    def run(self):
        """
        支付类交易情况 -- 一段文字 + 一个表格

        1 文字
        当日，云闪付APP发生支付类交易1133.76万笔，其中被扫、乘车码、远程转账、信用卡还款、一般主扫、快速收款码、小微主扫、手机外部支付控件、
        无感支付、人到人转账交易笔数排名前十，占到交易总量的98.94%。

        2 表格
        df_transaction_cnt_by_day=dfs['raw_transaction_cnt_by_day']
        df_transaction_cnt_by_day['ratio']=df_transaction_cnt_by_day['ratio'].apply(lambda x: format(float(x), '.2%'))
        df_transaction_cnt_by_day['proportion'] = df_transaction_cnt_by_day['cnt_today'] / df_transaction_cnt_by_day['cnt_today'].sum()
        df_transaction_cnt_by_day['proportion'] = df_transaction_cnt_by_day['proportion'].apply(lambda x: format(float(x), '.2%'))
        df_transaction_cnt_by_day=df_transaction_cnt_by_day_print=df_transaction_cnt_by_day.loc[:,['index','cnt_today','proportion','ratio'] ]
        """
        # 1 文字
        sentence = self.build_sentence()

        # 2 表格
        self.build_csv()

        # 构造最终返回的结果
        res = {
            "sentence": sentence,
            "csv": self.csv
        }
        return res


class QrTransactionByMerchant(object):
    def __init__(self, raw_csv, cfg):
        """
        二维码TOP10商户交易情况

        raw_csv: 包含1个csv --  raw_qr_transaction_by_merchant

        self.all_str: 最后要生成的一段文字
        self.csv: 最后要生成的表格 - qr_transaction_cnt_by_scene
        """
        self.raw_csv = raw_csv
        self.cfg = cfg

        # todo 将文字拆成结构化的key-value对以后，为每一对写一个函数
        self.all_str = {
            "1": "",
            "2": ""
        }
        self.csv = raw_csv

    def build_sentence(self):
        # 1 构造 self.all_str 字典
        # todo

        # 2 将字典 转为 dataframe
        sentence = ""
        for k, v in self.all_str.items():
            sentence += v
        res = pd.DataFrame(data={"sentence": [sentence]})
        return res

    def build_csv(self):
        # 构造CSV
        # todo 按照昨天的理解，csv 不需要做进一步处理，直接作为dataframe写入最终的excel即可。今晚再确认一下
        pass

    def run(self):
        """
        1 文字
        当日，云闪付APP发生支付类交易1133.76万笔，其中被扫、乘车码、远程转账、信用卡还款、一般主扫、快速收款码、小微主扫、手机外部支付控件、
        无感支付、人到人转账交易笔数排名前十，占到交易总量的98.94%。

        2 表格
        """
        # 1 文字
        sentence = self.build_sentence()

        # 2 表格
        self.build_csv()

        # 构造最终返回的结果
        res = {
            "sentence": sentence,
            "csv": self.csv
        }
        return res


class QrTransactionByAmountOfMoney(object):
    def __init__(self, raw_csv, cfg):
        """
        二维码交易金额分布

        raw_csv: 包含1个csv --  raw_qr_transaction_by_amount_of_money

        self.all_str: 最后要生成的一段文字
        self.csv: 最后要生成的表格 - qr_transaction_cnt_by_scene
        """
        self.raw_csv = raw_csv
        self.cfg = cfg

        # todo 将文字拆成结构化的key-value对以后，为每一对写一个函数
        self.all_str = {
            "1": "",
            "2": ""
        }
        self.csv = raw_csv

    def build_sentence(self):
        # 1 构造 self.all_str 字典
        # todo

        # 2 将字典 转为 dataframe
        sentence = ""
        for k, v in self.all_str.items():
            sentence += v
        res = pd.DataFrame(data={"sentence": [sentence]})
        return res

    def build_csv(self):
        # 构造CSV
        # todo 按照昨天的理解，csv 不需要做进一步处理，直接作为dataframe写入最终的excel即可。今晚再确认一下
        pass

    def run(self):
        """
        1 文字

        2 表格
        """
        # 1 文字
        sentence = self.build_sentence()

        # 2 表格
        self.build_csv()

        # 构造最终返回的结果
        res = {
            "sentence": sentence,
            "csv": self.csv
        }
        return res
