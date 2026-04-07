# version 1.00  -  python version of "End Date Calculator" in Leap Admin

from datetime import datetime, timedelta
import calendar

def leap_end_date_calculator(orig_date: datetime, num_months: int) -> datetime:
    # Calculates the end date based on: a given start date; and given duration (in months).
    #    python version of "End Date Calculator" in Leap Admin
    # Add the dates together and adjust the year if needed
    new_month: int = orig_date.month + num_months
    new_year: int = orig_date.year
    while new_month > 12:
        new_year += 1
        new_month -= 12
    # Use 'calendar.monthrange' to find the last day of the new month, and ensure the day is real/valid (e.g., Jan 31 -> Feb 28/29)  
    last_day_of_new_month: int = calendar.monthrange(new_year, new_month)[1]
    new_day: int = min(orig_date.day, last_day_of_new_month)
    # Creates the new real/valid end date, then subtracts 1 day (similar to how Leap does it)
    end_date: datetime = orig_date.replace(year=new_year, month=new_month, day=new_day)
    end_date -= timedelta(days=1)
    return end_date


def main():
    print()
    while True:
        try:
            # note: input() returns a string that needs to be converted to a datetime object
            date_str: str = input("Start date (YYYY-MM-DD or YYYY/MM/DD):   ").strip()
            date_str = date_str.replace("/", "-").strip()
            start_date: datetime = datetime.strptime(date_str, "%Y-%m-%d")
        except ValueError:
            print("\033[31m \tInvalid date format! Please use YYYY-MM-DD or YYYY/MM/DD\033[0m")  
        else:
            break

    while True:
        try:
            num_months: int = int(input("Duration in months 1..24?   ").strip())
            if num_months < 1:
                raise ValueError()
                #return False
        except ValueError:
            print("\033[31m \tPlease enter a positive integer.\033[0m") 
        else:
            break

    end_date: datetime = leap_end_date_calculator(start_date, num_months)
    print(f"\nThe END date is: {end_date.strftime('%Y-%m-%d')}")
    print()


if __name__ == "__main__":
    main()
