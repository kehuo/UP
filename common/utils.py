def process_float(raw_float, baoliu_num=2):
    """
    :param raw_float: 原始的数据如 12.335435
    :param baoliu_num: 保留小数点后几位
    :return:
    """
    return round(raw_float, baoliu_num)