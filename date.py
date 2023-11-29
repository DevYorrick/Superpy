import argparse
import csv
import datetime
from datetime import datetime, timedelta
import pandas as pd
from date import *
from datetime import datetime
from rich import print
from rich.console import Console
from rich.table import Table
import matplotlib.pyplot as plt
from datetime import timedelta

def read_date_from_file(file_path):
            try:
                with open(file_path, 'r') as file:
                    date_str = file.readline()
                    return datetime.strptime(date_str.strip(), '%Y-%m-%d')
            except FileNotFoundError:
                return None
            
def save_date_to_file(file_path, date):
    with open(file_path, 'w') as file:
        file.write(date.strftime('%Y-%m-%d'))

# Advance the time forward by a specified number of days
def advance_time_now(current_date, days):
    new_date = current_date + datetime.timedelta(days=days)
    return new_date

file_path = 'date.txt'
saved_date = read_date_from_file(file_path)

def print_date():
    if saved_date:
        print('Saved Date:', saved_date)
    else:
        print('No saved date found.')

# Get current date and time
current_date = saved_date

def advance_time(days):
    # Read the current date from date.txt
    with open('date.txt', 'r') as date_file:
        current_date = date_file.readline().strip()

    print('Current Date:', current_date)
    skip_days = int(input("How many days would you like to skip?"))

    # Calculate the new date
    new_date = advance_time_now(current_date, skip_days)
    print('New Date:', new_date)

    # Save the new date to the file
    save_date_to_file('date.txt', new_date)

    # Check for expired items and move them to expired.csv
    move_expired_items()

def advance_time_now(current_date, days_to_skip):
    # Convert current_date to a datetime object
    current_date = datetime.strptime(current_date, '%Y-%m-%d')

    # Calculate the new date by adding days_to_skip
    new_date = current_date + timedelta(days=days_to_skip)

    # Format the new date as a string in the required format
    return new_date.strftime('%Y-%m-%d')

def move_expired_items():
    try:
        # Read the current date from date.txt
        with open('date.txt', 'r') as date_file:
            current_date = date_file.readline().strip()

        rows = []

        # Read the inventory.csv file
        with open('inventory.csv', 'r') as file:
            reader = csv.DictReader(file)

            # Check expiration_date and move items to expired.csv if expired
            for row in reader:
                expiration_date = row['expiration_date']
                if datetime.strptime(current_date, '%Y-%m-%d') > datetime.strptime(expiration_date, '%Y-%m-%d'):
                    move_to_expired(row)
                else:
                    rows.append(row)

        # Write the remaining items to inventory.csv
        with open('inventory.csv', 'w', newline='') as file:
            fieldnames = ['product_name', 'quantity', 'bought_price', 'sold_price', 'expiration_date']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)
    except Exception as e:
        print(f"An error occurred: {e}")

def move_to_expired(item):
    # Move the expired item to expired.csv
    with open('expired.csv', 'a', newline='') as expired_file:
        fieldnames = ['product_name', 'quantity', 'bought_price', 'sold_price', 'expiration_date']
        writer = csv.DictWriter(expired_file, fieldnames=fieldnames)
        if not expired_file.tell():
            writer.writeheader()
        writer.writerow(item)
    print(f"{item['product_name']} expired and moved to expired.csv")

def save_date_to_file(file_path, new_date):
    # Save the new date to the file
    with open(file_path, 'w') as date_file:
        date_file.write(new_date)

def set_date():
    # Ask the user for a new date
    new_date = input("Enter the new date (YYYY-MM-DD): ")

    try:
        # Convert the input date string to a datetime object
        parsed_date = datetime.strptime(new_date, '%Y-%m-%d')
    except ValueError:
        return "Invalid date format. Please use YYYY-MM-DD."

    # Format the datetime object back to a string
    formatted_date = parsed_date.strftime('%Y-%m-%d')

    # Write the formatted date to the date.txt file
    with open('date.txt', 'w') as file:
        file.write(formatted_date)

    return f"Date updated to: {formatted_date}"
