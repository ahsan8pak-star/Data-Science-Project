import datetime
from zoneinfo import ZoneInfo

date = datetime.date(2025, 1, 2)
today = datetime.date.today()

print(date)
print(today)

time = datetime.time(12, 30, 0)
now = datetime.datetime.now()

print(time)
print(now)

new_time = now.strftime("%Y-%m-%d %H:%M:%S")
print(new_time)

new_format = now.strftime("%Y-%m-%d %H:%M:%S")
print(new_format)

est_now = datetime.datetime.now(ZoneInfo("America/New_York"))
bst_now = datetime.datetime.now(ZoneInfo("Europe/London"))

print(f"EST: {est_now.strftime('%Y-%m-%d %H:%M:%S %Z')}")
print(f"BST: {bst_now.strftime('%Y-%m-%d %H:%M:%S %Z')}")

target_datetime = datetime.datetime(2030, 1, 2, 12, 30, 1)
current_datetime = datetime.datetime.now()

if target_datetime < current_datetime:
    print("DEADLINE MET!")

else:
    print(f"You have {target_datetime - current_datetime} left to meet the deadline.")

"""----------------------------------------------------------------------------------"""

# datetime functions and attributes
print(dir(datetime))
# ['MAXYEAR', 'MINYEAR', 'UTC', '__all__', '__builtins__', '__cached__', '__doc__', '__file__', '__loader__', '__name__', '__package__', '__spec__', 'date', 'datetime', 'datetime_CAPI', 'time', 'timedelta', 'timezone', 'tzinfo']

from datetime import datetime   # from datetime import datetime

# Basics of datetime

now = datetime.now()
print(now)                      # 2026-09-13 15:11:45.371491

day = now.day                   # 13
month = now.month               # 9
year = now.year                 # 2026
hour = now.hour                 # 15
minute = now.minute             # 11
second = now.second             # 45

timestamp = now.timestamp()     # 1789308705.371491
print(day, month, year, hour, minute)               # 13 9 2026 15 11
print('timestamp', timestamp)                       # timestamp 1789308705.371491
print(f'{day}/{month}/{year}, {hour}:{minute}')     # 13/9/2026, 15:11

# --------------------------------------------------------------------------------------
# Formatting using strftime
# --------------------------------------------------------------------------------------

new_year = datetime(2026, 9, 28, 8, 00, 0)      # 2026-09-28 08:00:00
print(new_year)      # 2026-09-28 08:00:00
day = new_year.day
month = new_year.month
year = new_year.year
hour = new_year.hour
minute = new_year.minute
second = new_year.second
print(day, month, year, hour, minute)           # 28 9 2026 8 0
print(f'{day}/{month}/{year}, {hour}:{minute}') # 28/9/2026, 8:0

# --------------------------------------------------------------------------------------
# Example of formatting datetime using strftime
# --------------------------------------------------------------------------------------

# current date and time
now = datetime.now()
t = now.strftime("%H:%M:%S")
print("time:", t)                               # 15:11:45

time_one = now.strftime("%m/%d/%Y, %H:%M:%S")
# mm/dd/YY H:M:S format
print("time one:", time_one)                    # 09/13/2026, 15:11:45

time_two = now.strftime("%d/%m/%Y, %H:%M:%S")
# dd/mm/YY H:M:S format
print("time two:", time_two)                    # 13/09/2026, 15:11:45

# --------------------------------------------------------------------------------------
# String to Time using strptime
# --------------------------------------------------------------------------------------

from datetime import datetime
date_string = "28th September, 2026"
print("date_string =", date_string)     # date_string = 28th September, 2026

date_object = datetime.strptime(date_string, "%dth %B, %Y")
print("date_object =", date_object)     # date_object = 2026-09-28 00:00:00

# --------------------------------------------------------------------------------------
# Using date from datetime
# --------------------------------------------------------------------------------------

from datetime import date
d = date(2026, 9, 28)
print(d)                                # 2026-09-28
print('Current date:', d.today())       # Current date: 2026-09-13

# date object of today's date
today = date.today()
print("Current year:", today.year)      # Current year: 2026
print("Current month:", today.month)    # Current month: 9
print("Current day:", today.day)        # Current day: 13

# --------------------------------------------------------------------------------------
# Time object to represent time
# --------------------------------------------------------------------------------------

from datetime import time

# time(hour = 0, minute = 0, second = 0)
a = time()
print("a =", a)     # a = 00:00:00

# time(hour, minute and second)
b = time(10, 30, 50)
print("b =", b)     # b = 10:30:50

# time(hour, minute and second)
c = time(hour=10, minute=30, second=50)
print("c =", c)     # c = 10:30:50

# time(hour, minute, second, microsecond)
d = time(10, 30, 50, 200555)
print("d =", d)     # d = 10:30:50.200555

# --------------------------------------------------------------------------------------
# Difference Between Two Points in Time
# --------------------------------------------------------------------------------------

from datetime import date, datetime
today = date(year=2026, month=12, day=5)
new_year = date(year=2027, month=1, day=1)
time_left_for_newyear = new_year - today
# Time left for new year:  27 days, 0:00:00
print('Time left for new year: ', time_left_for_newyear)  # Time left for new year:  27 days, 0:00:00

t1 = datetime(year = 2026, month = 9, day = 28, hour = 8, minute = 30, second = 15)
t2 = datetime(year = 2027, month = 1, day = 1, hour = 0, minute = 0, second = 0)
diff = t2 - t1
print('Time left for new year:', diff) # Time left for new year: 26 days, 23: 01: 00

# --------------------------------------------------------------------------------------
# Difference Between Two Points in Time Using timedelta
# --------------------------------------------------------------------------------------

from datetime import timedelta
t1 = timedelta(weeks=12, days=10, hours=4, seconds=20)
t2 = timedelta(days=7, hours=5, minutes=3, seconds=30)
t3 = t1 - t2
print("t3 =", t3)

