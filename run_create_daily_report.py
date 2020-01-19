import json


class DailyReportCreator(object):
    """
    该类 用来生成 云闪付APP交易情况日报
    """
    def __init__(self, cfg_path):
        with open(cfg_path, "r", encoding="utf-8") as f:
            self.cfg = json.load(f)
        return



def main():
    cfg_path = "/users/hk/dev/UP/"
    cfg_name = "daily_report_cfg.json"
    daily_report_creator = DailyReportCreator(cfg_path + cfg_name)


if __name__ == '__main__':
    main()