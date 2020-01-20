from core.daily_report_creator import TotalDailyReportCreator


def main():
    cfg_path = "/users/hk/dev/UP/"
    cfg_name = "daily_report_cfg.json"
    daily_report_creator = TotalDailyReportCreator(cfg_path + cfg_name, model_type="total")
    daily_report_creator.run()


if __name__ == '__main__':
    main()
