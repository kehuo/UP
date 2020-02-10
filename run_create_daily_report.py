from core.daily_report_processor import DailyReportProcessor


def main():
    # 配置
    cfg_path = {
        "linux": "/users/apple/dev/UP/",
        "windows": "C:\\users\\kehu\\dev\\up\\"
    }
    cfg_name = "cfg.json"

    # 实例化 + run
    curr_device_type = "linux"
    drp = DailyReportProcessor(cfg_path[curr_device_type] + cfg_name)
    drp.load_csv_data(device_type=curr_device_type)
    drp.run()

    # 生成最终 excel
    drp.concat(device_type=curr_device_type)


if __name__ == '__main__':
    main()
