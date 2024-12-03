# filename: check_date_leap_year.py

from datetime import date

# Get today's date
today = date.today()

# Print today's date
print("Today's date is:", today)

# Check if the current year is a leap year
year = today.year
is_leap = (year % 4 == 0 and (year % 100 != 0 or year % 400 == 0))

if is_leap:
    print(f"{year} is a leap year.")
else:
    print(f"{year} is not a leap year.")