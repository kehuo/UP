import pandas as pd


class ControlTransactionTop10Merchant(object):
    def __init__(self, raw_csv, cfg):
        """
        手机支付控件TOP10商户交易情况

        raw_csv: 字典格式, 包含2个csv --  raw_control_transaction_top10_merchant / raw_control_out_transaction_top10_merchant

        self.all_str: 最后要生成的一段文字
        self.csv: 最后要生成的2个表格 - control_transaction_top10_merchant.csv / control_out_transaction_top10_merchant.csv
        """
        self.raw_csv = raw_csv
        self.cfg = cfg

        # todo 将文字拆成结构化的key-value对以后，为每一对写一个函数
        self.all_str = {
            "1": "",
            "2": ""
        }
        # todo 因为要生成2张表, 暂时定义一个空字典, 在 build_csv 函数中构造 self.csv 的具体数据
        self.csv = {}

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
        # todo 构造2 个 CSV (control / control out)
        pass

    def run(self):
        """
        主函数 -- 一段文字 + 一个表格
        """
        # 1 文字
        sentence = self.build_sentence()

        # 2 表格
        self.build_csv()

        # 构造最终返回的结果 (注意, 这里 self.csv 是一个字典, 因为有2张表需要返回, 分别是control / control out)
        res = {
            "sentence": sentence,
            "csv": self.csv
        }
        return res


class ControlOutByAreaCd(object):
    def __init__(self, raw_csv, cfg):
        """
        手机外部支付控件TOP10商户侧分公司交易情况

        raw_csv: 1个 -- raw_control_out_by_area_cd

        self.all_str: 最后要生成的一段文字
        self.csv: 最后要生成的 1 个表格 - control_out_by_area_cd.csv
        """
        self.raw_csv = raw_csv
        self.cfg = cfg

        # todo 将文字拆成结构化的key-value对以后，为每一对写一个函数
        self.all_str = {
            "1": "",
            "2": ""
        }

        self.csv = self.raw_csv

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
        # todo 按照我的理解, 不需要做其他处理
        pass

    def run(self):
        """
        主函数 -- 一段文字 + 一个表格
        """
        # 1 文字
        sentence = self.build_sentence()

        # 2 表格
        self.build_csv()

        # 构造最终返回的结果 (注意, 这里 self.csv 是一个 dataframe)
        res = {
            "sentence": sentence,
            "csv": self.csv
        }
        return res


class ControlOutByUserGps(object):
    def __init__(self, raw_csv, cfg):
        """
        手机外部支付控件TOP10用户侧分公司交易情况

        raw_csv: 1个 -- raw_control_out_by_user_gps

        self.all_str: 最后要生成的一段文字
        self.csv: 最后要生成的 1 个表格 - control_out_by_user_gps.csv
        """
        self.raw_csv = raw_csv
        self.cfg = cfg

        # todo 将文字拆成结构化的key-value对以后，为每一对写一个函数
        self.all_str = {
            "1": "",
            "2": ""
        }

        self.csv = self.raw_csv

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
        # todo 按照我的理解, 不需要做其他处理
        pass

    def run(self):
        """
        主函数 -- 一段文字 + 一个表格
        """
        # 1 文字
        sentence = self.build_sentence()

        # 2 表格
        self.build_csv()

        # 构造最终返回的结果 (注意, 这里 self.csv 是一个 dataframe)
        res = {
            "sentence": sentence,
            "csv": self.csv
        }
        return res


class ControlOutTransactionByAmountOfMoney(object):
    def __init__(self, raw_csv, cfg):
        """
        手机外部支付控件交易金额分布

        raw_csv: 1个 dataframe -- raw_control_out_transaction_by_amount_of_money

        self.all_str: 最后要生成的一段文字
        self.csv: 最后要生成的 1 个表格 - control_out_transaction_by_amount_of_money.csv
        """
        self.raw_csv = raw_csv
        self.cfg = cfg

        # todo 将文字拆成结构化的key-value对以后，为每一对写一个函数
        self.all_str = {
            "1": "",
            "2": ""
        }

        self.csv = self.raw_csv

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
        # todo 按照我的理解, 不需要做其他处理
        pass

    def run(self):
        """
        主函数 -- 一段文字 + 一个表格
        """
        # 1 文字
        sentence = self.build_sentence()

        # 2 表格
        self.build_csv()

        # 构造最终返回的结果 (注意, 这里 self.csv 是一个 dataframe)
        res = {
            "sentence": sentence,
            "csv": self.csv
        }
        return res
