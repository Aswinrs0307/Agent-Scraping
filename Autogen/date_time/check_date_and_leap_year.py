# filename: check_date_and_leap_year.py
from datetime import datetime

# Get the current date
current_date = datetime.now()

# Print the current date
print(f"Today's date is: {current_date.strftime('%Y-%m-%d')}")

# Check if the current year is a leap year
year = current_date.year
is_leap_year = (year % 4 == 0 and (year % 100 != 0 or year % 400 == 0))

# Print if the current year is a leap year
if is_leap_year:
    print(f"{year} is a leap year.")
else:
    print(f"{year} is not a leap year.")