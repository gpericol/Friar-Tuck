from os.path import join

CONFIG = {
    "path_pid": join("./data", "system", "pid"),
    "path_status": join("./data", "system", "status.json"),
    "path_curves": join("./data", "curves"),
    "path_curves_list": join("./data", "system", "curves_list.json"),
    "telegram_users": [],
    "telegram_token": "",
    "in_heater": 16,
    "in_cooler": 18
}