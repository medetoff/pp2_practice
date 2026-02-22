from datetime import datetime, timedelta
import math

def parse_datetime(line):
    parts = line.strip().split()
    date_str = parts[0]
    tz_str = parts[1]
    
    year, month, day = map(int, date_str.split('-'))
    
    tz_offset_str = tz_str[3:]
    if tz_offset_str == "" or tz_offset_str == "+00:00" or tz_offset_str == "-00:00":
        offset_minutes = 0
    else:
        sign = 1 if tz_offset_str[0] == '+' else -1
        time_part = tz_offset_str[1:]
        hours, minutes = map(int, time_part.split(':'))
        offset_minutes = sign * (hours * 60 + minutes)
    
    local_midnight = datetime(year, month, day, 0, 0, 0)
    utc_time = local_midnight - timedelta(minutes=offset_minutes)
    
    return utc_time, year, month, day, offset_minutes

def is_leap_year(year):
    return (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)

def get_birthday_in_year(birth_month, birth_day, target_year, birth_offset_minutes):
    if birth_month == 2 and birth_day == 29:
        if is_leap_year(target_year):
            day = 29
        else:
            day = 28
    else:
        day = birth_day
    
    local_midnight = datetime(target_year, birth_month, day, 0, 0, 0)
    utc_time = local_midnight - timedelta(minutes=birth_offset_minutes)
    return utc_time

line1 = input().strip()
line2 = input().strip()

birth_utc, birth_year, birth_month, birth_day, birth_offset = parse_datetime(line1)
current_utc, current_year, current_month, current_day, current_offset = parse_datetime(line2)

candidate_years = [current_year - 1, current_year, current_year + 1, current_year + 2]

best_birthday = None
for year in candidate_years:
    if year < birth_year:
        continue
    birthday_utc = get_birthday_in_year(birth_month, birth_day, year, birth_offset)
    if birthday_utc >= current_utc:
        if best_birthday is None or birthday_utc < best_birthday:
            best_birthday = birthday_utc

diff_seconds = (best_birthday - current_utc).total_seconds()

if diff_seconds == 0:
    print(0)
else:
    days_left = math.ceil(diff_seconds / 86400)
    print(days_left)