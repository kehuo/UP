import json

path = "C:\\users\\kehu\\dev\\up\\demo\\"
name = "dev.json"
formatted_name = "format.json"

with open(path + name, "r", encoding="utf-8-sig") as f:
    data = json.load(f)

with open(path + formatted_name, "w", encoding="utf-8") as ff:
    formatted_data = json.dumps(data, ensure_ascii=False, indent=4)
    ff.write(formatted_data)

