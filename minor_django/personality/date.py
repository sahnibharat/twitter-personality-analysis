import datetime
now = datetime.date.today()
week=now-datetime.timedelta(days=15)
#week=week.strftime('%d-%m-%Y')
print(week.strftime('%d'))
