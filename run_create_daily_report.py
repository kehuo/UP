from core.daily_report_creator import TotalDailyReportCreator, BaseClass


def main():
    cfg_path = "/users/hk/dev/UP/"
    cfg_name = "cfg.json"
    daily_report_creator = BaseClass(cfg_path + cfg_name)
    daily_report_creator.load_csv_data()
    daily_report_creator.run()


if __name__ == '__main__':
    main()
