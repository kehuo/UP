import core.logic.handle_func.model_1 as Model_1_Handler
import core.logic.handle_func.model_2 as Model_2_Handler
import core.logic.handle_func.model_3 as Model_3_Handler


class General(object):
    """
    该类用来处理每个模块中 除了Overview之外的 通用部分.
    """
    def __init__(self, all_raw_csv, cfg):
        """
        raw_csv: 字典类型. data/raw/ 下所有 13 csv
        cfg: cfg.json

        self.sentence_dict: 字典类型. 结构化的一段文字.
        self.csv: 最后要生成的表格
        """
        self.all_raw_csv = all_raw_csv
        self.cfg = cfg

        self.sentence_dict = {}

    def _init_sentence_dict(self, service_type):
        """
        该字典用来构造每个表前面的 那一段文字, 按照以下的结构, 对文字进行结构化
        service: 不同 model 中的具体业务, 如 "支付类交易情况", 即
        """

        service_sentence_map = {
            # model 1 - 总体交易情况
            "transaction_cnt_by_day": {},

            # model 2 - 二维码交易情况
            "qr_transaction_cnt_by_scene": {},
            "qr_transaction_by_area_cd": {},
            "qr_transaction_by_merchant": {},
            "qr_transaction_by_amount_of_money": {},

            # model 3 - 手机支付控件交易情况
            "control_transaction_top_10_merchant": {},
            "control_out_by_area_cd": {},
            "control_out_by_user_gps": {},
            "control_out_transaction_by_amount_of_money": {}
        }

        self.sentence_dict = service_sentence_map[service_type]["sentence_dict"]

    def run(self, model_type, service_type):
        """
        service_type: 每个model中的具体业务, 比如 model 1 中的 "支付类交易情况", model 2 中的 "主要场景交易情况".

        service_type = "transaction_cnt_by_day"
        1 文字
        2 csv
        """
        # 1 初始化 sentence_dict
        self._init_sentence_dict(service_type)

        # 2 定义不同 model 需要的 handler
        handler_module_map = {
            "total": Model_1_Handler,
            "qr": Model_2_Handler,
            "control": Model_3_Handler
        }

        # 3 这里为了函数的统一性, csv 数据统一传入所有的 self.all_raw_csv
        # 这里用 __getattribute__() 可以替换 __dict__[] 完全等效. 但是注意一个是方括号, 一个是圆括号
        res = handler_module_map[model_type].__dict__[service_type](sentence_dict=self.sentence_dict,
                                                                    all_raw_csv=self.all_raw_csv,
                                                                    cfg=self.cfg
                                                                    )

        return res
