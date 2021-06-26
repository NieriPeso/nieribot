from datetime import datetime
import pytz

tz = pytz.timezone('America/Argentina/Buenos_Aires')

def get_date():
    now = datetime.now(tz=tz)
    now = datetime(day=now.day,month=now.month,year=now.year,hour=now.hour,minute=now.minute)
    return now

def end(date):
    now = get_date()
    date = datetime(
        day=int(date.split(' ')[0].split('/')[0]),
        month=int(date.split(' ')[0].split('/')[1]),
        year=int(date.split(' ')[0].split('/')[2]),
        hour=int(date.split(' ')[1].split(':')[0]),
        minute=int(date.split(' ')[1].split(':')[1])
    )
    if (date-now).days < 0 or (date-now).days == 0 and not (date-now).seconds > 0:
        return True
    return False

def past_date(date):
    now = get_date()
    date = datetime(
        day=int(date.split(' ')[0].split('/')[0]),
        month=int(date.split(' ')[0].split('/')[1]),
        year=int(date.split(' ')[0].split('/')[2]),
        hour=int(date.split(' ')[1].split(':')[0]),
        minute=int(date.split(' ')[1].split(':')[1])
    )
    if (date-now).days < 0 or (date-now).days == 0 and (date-now).seconds <= 599:
        return True
    return False
