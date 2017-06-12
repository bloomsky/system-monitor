from pytz import timezone, utc
import datetime

def readable_time_without_hms(ts):
    "return readable time from timestamp for specified timezone"
    pacific_zone = timezone('US/Pacific')
    utc_time = datetime.datetime.fromtimestamp(float(ts))
    now_utc = utc.localize(utc_time)
    local_time = now_utc.astimezone(pacific_zone)
    return local_time.strftime('%Y-%m-%d')
