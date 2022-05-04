import datetime
import time


class Util:
    def get_date(_, timestamp):
        get_Date = datetime.utcfromtimestamp(timestamp / 1000)
        return get_Date

    def get_unix(_, date: datetime.datetime):
        get_Unix = time.mktime(datetime.timetuple(date))
        return get_Unix

    def get_datetime(_, time: int):
        get_datetime = datetime.strptime(time, "%Y-%m-%d %H:%M:%S")
        return get_datetime

    def get_CSV(_, dataFrame, fileName: str):
        dataFrame.to_csv(fileName, index=False, encoding="utf-8")

    def get_Percent(_, currentValue: float, totalValue: float):
        return (currentValue / totalValue) * 100

    def show_Percent(_, percent: float):
        return "{:.0f}%".format(percent)
