from core.daily_report_creator import DailyReportProcessor


def main():
    # 配置
    cfg_path = {
        "linux": "/users/hk/dev/UP/",
        "windows": "C:\\users\\kehu\\dev\\up\\"
    }
    cfg_name = "cfg.json"

    # 实例化 + run
    drp = DailyReportProcessor(cfg_path["windows"] + cfg_name)
    drp.load_csv_data(device_type="windows")
    drp.run()

    # 生成最终 excel
    drp.concat(device_type="windows")


if __name__ == '__main__':
    main()
