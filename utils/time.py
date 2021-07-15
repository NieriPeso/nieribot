from datetime import datetime, timedelta
import pytz

tz = pytz.timezone('America/Argentina/Buenos_Aires')

def get_date_to_close():
    now = get_date()
    day_added = timedelta(minutes=1)
    date = now + day_added
    return date.strftime('%d/%m/%Y %H:%M')

def get_date():
    now = datetime.now(tz=tz)
    now = datetime(day=now.day,month=now.month,year=now.year,hour=now.hour,minute=now.minute)
    return now

def get_date_future():
    now = get_date()
    day_added = timedelta(days=1)
    date = now + day_added
    return date.strftime('%d/%m/%Y %H:%M')

def end(date):
    now = get_date()
    if (date-now).days < 0 or (date-now).days == 0 and not (date-now).seconds > 0:
        return True
    return False

def past_date(date):
    now = get_date()
    date = convert_to_datetime(date)
    if (date-now).days < 0 or (date-now).days == 0 and (date-now).seconds <= 599:
        return True
    return False

def last_five_minutes(offerTime, closeAt):
    print('checking')
    if timedelta(minutes=5) > closeAt - offerTime:
        return True
    return False

def get_new_close(offerTime, closeAt):
    return closeAt + (timedelta(minutes=5) - (closeAt - offerTime))

def convert_to_datetime(date):
    date = datetime(
        day=int(date.split(' ')[0].split('/')[0]),
        month=int(date.split(' ')[0].split('/')[1]),
        year=int(date.split(' ')[0].split('/')[2]),
        hour=int(date.split(' ')[1].split(':')[0]),
        minute=int(date.split(' ')[1].split(':')[1])
    )
    return date
