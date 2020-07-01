import datetime

import pystan

days = []
today = datetime.date.today()
for i in range(0,366,1):
    daybeforetoday = today + datetime.timedelta(days=-i)
    days.append(daybeforetoday.strftime('%Y-%m-%d'))
days = list(reversed(days))
print(days)