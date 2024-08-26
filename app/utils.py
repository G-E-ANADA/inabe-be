from datetime import datetime

def str_to_datetime(date_str) -> datetime:
    if isinstance(date_str, datetime):
        return date_str
    return datetime.strptime(date_str, "%Y%m%d")
