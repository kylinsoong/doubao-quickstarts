from datetime import datetime
import pytz

tz_utc8 = pytz.timezone('Asia/Shanghai')
x_date = datetime.now(tz_utc8).strftime('%Y%m%dT%H%M%SZ')
print(x_date)

