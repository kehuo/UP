from core.daily_report_creator import BaseClass


def main():
    cfg_path = {
        "macbook": "/users/hk/dev/UP/",
        "windows": "C:\\users\\kehu\\dev\\up\\"
    }
    cfg_name = "cfg.json"
    daily_report_creator = BaseClass(cfg_path["windows"] + cfg_name)
    daily_report_creator.load_csv_data(device_type="windows")
    daily_report_creator.run()

    # 生成最终 excel
    daily_report_creator.concat(device_type="windows")


if __name__ == '__main__':
    main()
