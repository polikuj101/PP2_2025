from datetime import datetime, timedelta

# 1. Subtract five days from the current date
current_date = datetime.now()
five_days_ago = current_date - timedelta(days=5)
print("Five days ago:", five_days_ago.strftime("%Y-%m-%d"))

# 2. Print yesterday, today, and tomorrow
yesterday = current_date - timedelta(days=1)
tomorrow = current_date + timedelta(days=1)

print("Yesterday:", yesterday.strftime("%Y-%m-%d"))
print("Today:", current_date.strftime("%Y-%m-%d"))
print("Tomorrow:", tomorrow.strftime("%Y-%m-%d"))

# 3. Drop microseconds from datetime
current_time = datetime.now().replace(microsecond=0)
print("Current datetime without microseconds:", current_time)

# 4. Calculate the difference between two dates in seconds
date1 = datetime(2024, 2, 10, 12, 0, 0)  # Example date 1
date2 = datetime(2024, 2, 15, 14, 30, 0)  # Example date 2

difference = abs((date2 - date1).total_seconds())
print("Difference between dates in seconds:", difference)
