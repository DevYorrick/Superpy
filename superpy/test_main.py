# Imports
import argparse
import csv
import datetime
from date import *
import pandas as pd
from test import *

# Do not change these lines.
__winc_id__ = "a2bc36ea784242e4989deb157d527ba0"
__human_name__ = "superpy"


# Your code below this line.
def main():
    pass


if __name__ == "__main__":
    main()



def display_menu():
    print("SuperPy inventory system:")
    print("1. Products for sale")
    print("2. Current inventory and expiry dates")
    print("3. Bought product price")
    print("4. Sold products or expired")
    print("5. Revenue")
    print("6. Current day")
    print("7. Advance time")
    print("8. Exit")

while (True):
    print('''SuperPy inventory system:
        1. Products for sale
        2. Current inventory and expiry dates
        3. sell a product
        4. Sold products or expired
        5. Revenue
        6. Current day
        7. Advance time
        8. Import new product
        8. Exit
        ''')
        

    choice = int(input("Enter your option =  "))
    if choice == 1:
        print("Under construction")
    elif choice == 2:
        df = pd.read_csv('test_inventory.csv')
        inventory = df[['product_name', 'expiration_date']]
        print(inventory)
    elif choice == 3:
        print("Under construction")
    elif choice == 4:
        print("Under construction")
    elif choice == 5:
        print("Under construction")
    elif choice == 6:
        print('The current date is:', saved_date)
    elif choice == 7:
        print('Current Date:', current_date)
        skip_days = int(input("How many days would you like to skip?"))
        new_date = advance_time_now(current_date, skip_days)
        print('New Date :', new_date)
        # Save the new date to the file
        save_date_to_file(file_path, new_date)
    elif choice == 8:
        break
    else:
        print("That is not a viable option, please pick an option from the menu.")

def get_current_date():
    try:
        with open('date.txt', 'r') as file:
            return file.readline().strip()
    except FileNotFoundError:
        return datetime.now().strftime('%Y-%m-%d')

def sell_item(item, quantity):
    rows = []
    sold_rows = []

    with open('test_inventory.csv', 'r') as file:
        reader = csv.DictReader(file)
        sorted_rows = sorted(reader, key=lambda x: datetime.strptime(x['expiration_date'], '%Y-%m-%d'))

        for row in sorted_rows:
            if row['product_name'] == item:
                current_quantity = int(row['quantity'])
                quantity = int(quantity)

                if current_quantity >= quantity:
                    row['quantity'] = str(current_quantity - quantity)
                    total_price = quantity * float(row['sold_price'])
                    revenue = (quantity * float(row['sold_price'])) - (quantity * float(row['bought_price']))
                    print(f"Sold {quantity} {item}(s) for a total of ${total_price}.")
                    sold_row = row.copy()
                    sold_row['quantity'] = str(quantity)
                    sold_row['date_sold'] = get_current_date()
                    sold_row['revenue'] = revenue
                    sold_rows.append(sold_row)
                else:
                    print(f"Not enough {item}(s) in the inventory to sell.")
                
            rows.append(row)

    # Write remaining items to test_inventory.csv
    with open('test_inventory.csv', 'w', newline='') as file:
        fieldnames = ['product_name', 'quantity', 'bought_price', 'sold_price', 'expiration_date']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    # Write sold items to sold.csv
    with open('sold.csv', 'a', newline='') as sold_file:
        fieldnames = ['product_name', 'quantity', 'bought_price', 'sold_price', 'expiration_date', 'date_sold', 'revenue']
        writer = csv.DictWriter(sold_file, fieldnames=fieldnames)
        if not sold_file.tell():
            writer.writeheader()
        writer.writerows(sold_rows)

def revenue():
    # Read the sold.csv file
    with open('sold.csv', 'r') as file:
        reader = csv.DictReader(file)

        # Create a dictionary to store revenue for each date
        revenue_by_date = {}

        # Iterate through each row in the sold.csv file
        for row in reader:
            date_sold = row['date_sold']
            revenue = float(row['revenue'])

            # Check if the date is already in the dictionary, if not, add it
            if date_sold in revenue_by_date:
                revenue_by_date[date_sold] += revenue
            else:
                revenue_by_date[date_sold] = revenue

        # Print the revenue for each date
        for date, total_revenue in revenue_by_date.items():
            print(f"Revenue on {date}: ${total_revenue:.2f}")