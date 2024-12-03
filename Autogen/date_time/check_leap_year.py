# filename: check_leap_year.py

from datetime import datetime

# Get today's date
today = datetime.today()

# Print today's date
print("Today's date is:", today.strftime("%Y-%m-%d"))

# Check if the current year is a leap year
year = today.year

def is_leap_year(year):
    if (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0):
        return True
    else:
        return False

if is_leap_year(year):
    print(f"{year} is a leap year.")
else:
    print(f"{year} is not a leap year.")