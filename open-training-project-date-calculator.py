#!/usr/bin/env python3
# Calculates the open training Core & QuickStart project dates based on the class start date.
# The Core project duration is 3 weeks (bonus days before class starts + 1 week of class + 2 weeks to complete work).
# The QuickStart project duration is 2 weeks and 1 month (bonus days before class starts + 1 week of class + 1 week to complete work + 1 month).

from datetime import datetime, timedelta
import calendar
import subprocess
import platform


def leap_end_date_calculator(orig_date: datetime, num_months: int) -> datetime:
    # version 1.00  -  python version of "End Date Calculator" in Leap Admin
    # Calculates the end date based on: a given start date; and given duration (in months)
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
    print("\nOpen Training Project Date Calculator\n")
    while True:
        try:
            date_str: str = input("Enter the start date (monday) for the upcoming open training class (YYYY-MM-DD or YYYY/MM/DD):   ")
            date_str = date_str.replace("/", "-").strip()
            class_start_date: datetime = datetime.strptime(date_str, "%Y-%m-%d")
            # confirm start date is a Monday
            if class_start_date.weekday() != 0:
                print("\033[31m \tThe date entered is not a Monday, online training classes start on a Monday.\033[0m")
                continue
        except ValueError:
            print("\033[31m \tInvalid date format! Please use YYYY-MM-DD or YYYY/MM/DD\033[0m")  
        else:
            break
    
    while True:
        try:
            num_qs_users_str: str = input("How many QuickStart users are attending 0..10?   ").strip()
            if int(num_qs_users_str) < 0:
                raise ValueError()
        except ValueError:
            print("\033[31m \tInvalid format! Please enter an integer value for the number of QuickStart users.\033[0m") 
        else:
            break
    
    # Class with office hours is from Monday to Friday
    class_end_date: datetime = class_start_date + timedelta(days=4)   
    # The Core project duration is 3 weeks (bonus days before class starts + 1 week of class + 2 weeks to complete work).
    core_proj_start_date: datetime = class_start_date - timedelta(days=4)
    core_proj_end_date: datetime = class_start_date + timedelta(days=21)

    # check to see if class_start_date and class_end_date are in the same month; if so, don't repeat the month in end date
    if class_start_date.month == class_end_date.month:
        open_training_class_str: str = f"{class_start_date.strftime('%B %d')} to {class_end_date.strftime('%d, %Y')}"
        class_name_str: str = f"{class_start_date.strftime('%d')}-{class_end_date.strftime('%d %B %Y')}"
    else:
        open_training_class_str: str = f"{class_start_date.strftime('%B %d')} to {class_end_date.strftime('%B %d, %Y')}"
        class_name_str: str = f"{class_start_date.strftime('%d %B')} - {class_end_date.strftime('%d %B %Y')}"

    # Full reset (clears scrollback buffer as well)
    print("\033c", end="")    
    
    printout_message_str: str = "Hello Support,\n" \
        + "\n" \
        + f"Attached is the course roster for the upcoming Open Training class from {open_training_class_str}.\n" \
        + "  - Provision the necessary project(s) in Leap\n" \
        + "  - Invite the attendees and project admins (if any)\n" \
        + "\n" \
        + f"Class name: {class_name_str}\n" \
        + "Organization Admins: Kelly Novic, Sara Jamous\n" \
        + "Additional Project Admins: \n" \
        + f"QuickStart Users: {num_qs_users_str}\n" \
        + "\n" \
        + f"Project: Open Training {class_start_date.strftime('%Y/%m/%d')} Core\n" \
        + f"Start Date: {core_proj_start_date.strftime('%Y-%m-%d')}\n" \
        + f"End Date: {core_proj_end_date.strftime('%Y-%m-%d')}\n" \
        + "\n"

    if int(num_qs_users_str) > 0:
        # QuickStart class duration is 2-weeks (1 week of class + 1 week to complete work) and 1-month of QS project time
        qs_proj_start_date: datetime = class_start_date - timedelta(days=4)
        qs_start_of_month: datetime = class_start_date + timedelta(days=14)
        qs_proj_end_date: datetime = leap_end_date_calculator(qs_start_of_month, 1)
        printout_message_str += "" \
            + f"Project: Open Training {class_start_date.strftime('%Y/%m/%d')} QuickStart\n" \
            + f"Start Date: {qs_proj_start_date.strftime('%Y-%m-%d')}\n" \
            + f"End Date: {qs_proj_end_date.strftime('%Y-%m-%d')}\n" \
            + "\n"

    print(printout_message_str)

    # wait for user to press Enter before exiting
    print("Press Enter to copy to clipboard. Press Ctrl+C to exit\n")

    current_os: str = platform.system()
    
    while True:
        try:
            input("")
        except KeyboardInterrupt:
            # Clears the visible console screen (does not clear scrollback buffer)
            print("\033[H\033[J", end="")
            break
        else:
            #copy to clipboard based on OS
            if current_os == "Windows":
                subprocess.run("clip", input=printout_message_str, text=True, check=True)
            elif current_os == "Darwin":    # MacOS
                subprocess.run("pbcopy", input=printout_message_str, text=True, check=True)
            elif current_os == "Linux":     
                # Linux (requires 'xclip' or 'xsel' to be installed)
                try:
                    subprocess.run(["xclip", "-selection", "clipboard"], input=printout_message_str, text=True, check=True)
                except FileNotFoundError:
                    print("\033[31m'xclip' not found. Please install 'xclip' to enable clipboard copy on Linux, or copy the text manually." \
                          "\nsudo apt-get install xclip\t(Debian/Ubuntu)" \
                          "\nsudo yum install xclip\t\t(RHEL/CentOS/Fedora)\033[0m")
            else:
                print("\033[31m \tUnsupported OS for clipboard copy. Please copy the text manually.\033[0m")

            # Move the cursor up one line and clear that line
            print("\033[1A\033[K", end="")
            continue
            

if __name__ == "__main__":
    main()
