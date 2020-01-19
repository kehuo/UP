from datetime import datetime, timedelta


def process_float(raw_float, baoliu_num=2):
    """
    :param raw_float: 原始的数据如 12.335435
    :param baoliu_num: 保留小数点后几位
    :return:
    """
    return round(raw_float, baoliu_num)


def build_date_str(minus_day_count, str_type):
    res = datetime.now().date() - timedelta(days=minus_day_count)
    if str_type == "cn":
        res = "%s年%s月%s日" % (res.year, res.month, res.day)
    elif str_type == "bottom_line":
        res = "%s_%s_%s" % (res.year, res.month, res.day)
    return res