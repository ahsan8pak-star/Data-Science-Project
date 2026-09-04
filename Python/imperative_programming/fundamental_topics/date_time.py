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

