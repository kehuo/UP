import pandas as pd


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
