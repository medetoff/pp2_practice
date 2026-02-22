from datetime import datetime, timedelta

def parse_datetime(line):
    parts = line.strip().split()
    date_str = parts[0]
    tz_str = parts[1]
    
    year, month, day = map(int, date_str.split('-'))
    
    if tz_str.startswith("UTC"):
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
    
    return utc_time

line1 = input().strip()
line2 = input().strip()

dt1 = parse_datetime(line1)
dt2 = parse_datetime(line2)

diff = abs((dt2 - dt1).total_seconds())
full_days = int(diff // 86400)

print(full_days)