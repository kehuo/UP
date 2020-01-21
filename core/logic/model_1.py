import pandas as pd
import core.logic.handle_func.model_1 as Model_1_Handler


# service: model 中的具体业务, 如 "支付类交易情况", 即
service_sentence_map = {
    "transaction_cnt_by_day": {},

}


class TransactionCntByDay(object):
    def __init__(self, raw_csv, cfg):
        """
        raw_csv: raw_transaction_cnt_by_day
        cfg: cfg.json
        service_type: 每个model中的具体业务, 比如 model 1 中的 "支付类交易情况", model 2 中的 "主要场景交易情况".

        self.sentence_dict: 字典类型. 结构化的一段文字.
        self.csv: 最后要生成的表格
        """
        self.raw_csv = raw_csv
        self.cfg = cfg

        # todo 将文字拆成结构化的key-value对以后，为每一对写一个函数
        self.sentence_dict = {}
        self.csv = raw_csv

    def init_sentence_dict(self, service_type):
        self.sentence_dict = service_sentence_map[service_type]["sentence_dict"]

    def run(self, service_type):
        """
        1 文字 / 2 csv
        """
        res = Model_1_Handler.__dict__[service_type]
        print(res)
        return res
