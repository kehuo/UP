import pandas as pd
import core.logic.handle_func.model_1 as Model_1_Handler
import core.logic.handle_func.model_2 as Model_2_Handler
import core.logic.handle_func.model_3 as Model_3_Handler


# service: 不同 model 中的具体业务, 如 "支付类交易情况", 即
service_sentence_map = {
    # model 1
    "transaction_cnt_by_day": {}

    # model 2

}


class General(object):
    def __init__(self, all_raw_csv, cfg):
        """
        raw_csv: 字典类型. data/raw/ 下所有 13 csv
        cfg: cfg.json

        self.sentence_dict: 字典类型. 结构化的一段文字.
        self.csv: 最后要生成的表格
        """
        self.all_raw_csv = all_raw_csv
        self.cfg = cfg

        # todo 将文字拆成结构化的key-value对以后，为每一对写一个函数
        self.sentence_dict = {}

    def init_sentence_dict(self, service_type):
        self.sentence_dict = service_sentence_map[service_type]["sentence_dict"]

    def run(self, model_type, service_type):
        """
        service_type: 每个model中的具体业务, 比如 model 1 中的 "支付类交易情况", model 2 中的 "主要场景交易情况".

        service_type = "transaction_cnt_by_day"
        1 文字
        2 csv
        """
        handler_module_map = {
            "total": Model_1_Handler,
            "qr": Model_2_Handler,
            "control": Model_3_Handler
        }

        # 因为有些函数需要 2-3个 csv 文件, 所以这里统一传入所有的 self.all_raw_csv
        res = handler_module_map[model_type].__dict__[service_type](
            sentence_dict=self.sentence_dict,
            all_raw_csv=self.all_raw_csv,
            cfg=self.cfg
        )

        return res
