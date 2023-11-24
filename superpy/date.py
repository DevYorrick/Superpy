import argparse
import csv
import datetime

def read_date_from_file(file_path):
            try:
                with open(file_path, 'r') as file:
                    date_str = file.readline()
                    return datetime.datetime.strptime(date_str.strip(), '%Y-%m-%d')
            except FileNotFoundError:
                return None
            
# Save the current date to a text file
def save_date_to_file(file_path, date):
    with open(file_path, 'w') as file:
        file.write(date.strftime('%Y-%m-%d'))

# Advance the time forward by a specified number of days
def advance_time_now(current_date, days):
    new_date = current_date + datetime.timedelta(days=days)
    return new_date

# Example usage
file_path = 'date.txt'
saved_date = read_date_from_file(file_path)

def print_date():
    if saved_date:
        print('Saved Date:', saved_date)
    else:
        print('No saved date found.')

# Get current date and time
current_date = saved_date

# Advance time forward by 7 days
