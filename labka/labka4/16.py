from datetime import datetime, timedelta

def parse_datetime(line):
    parts = line.strip().split()
    date_str = parts[0]
    time_str = parts[1]
    tz_str = parts[2]
    
    year, month, day = map(int, date_str.split('-'))
    hour, minute, second = map(int, time_str.split(':'))
    
    tz_offset_str = tz_str[3:]
    if tz_offset_str == "" or tz_offset_str == "+00:00" or tz_offset_str == "-00:00":
        offset_minutes = 0
    else:
        sign = 1 if tz_offset_str[0] == '+' else -1
        time_part = tz_offset_str[1:]
        hours, minutes = map(int, time_part.split(':'))
        offset_minutes = sign * (hours * 60 + minutes)
    
    local_time = datetime(year, month, day, hour, minute, second)
    utc_time = local_time - timedelta(minutes=offset_minutes)
    
    return utc_time

line1 = input().strip()
line2 = input().strip()

start_utc = parse_datetime(line1)
end_utc = parse_datetime(line2)

diff_seconds = int((end_utc - start_utc).total_seconds())

print(diff_seconds)