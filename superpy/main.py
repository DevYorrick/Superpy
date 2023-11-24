# Imports
import argparse
import csv
import datetime
from datetime import datetime, timedelta
import pandas as pd
from date import *
from datetime import datetime

# Do not change these lines.
__winc_id__ = "a2bc36ea784242e4989deb157d527ba0"
__human_name__ = "superpy"


# Your code below this line.
def display_inventory():
        df = pd.read_csv('test_inventory.csv')
        df = df.drop(df[df.quantity == 0].index)
        df.to_csv('test_inventory.csv', index=False)
        with open('test_inventory.csv', 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                print(f"{row['product_name']}: Quantity - {row['quantity']}, Bought Price - ${row['bought_price']}, Sold Price - ${row['sold_price']}, Expiration Date - {row['expiration_date']}")

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

def save_date_to_file(file_path, new_date):
    # Save the new date to the file
    with open(file_path, 'w') as date_file:
        date_file.write(new_date)

def move_expired_items():
    # Read the current date from date.txt
    with open('date.txt', 'r') as date_file:
        current_date = date_file.readline().strip()

    rows = []

    # Read the test_inventory.csv file
    with open('test_inventory.csv', 'r') as file:
        reader = csv.DictReader(file)

        # Check expiration_date and move items to expired.csv if expired
        for row in reader:
            expiration_date = row['expiration_date']
            if datetime.strptime(current_date, '%Y-%m-%d') > datetime.strptime(expiration_date, '%Y-%m-%d'):
                move_to_expired(row)
            else:
                rows.append(row)

    # Write the remaining items to test_inventory.csv
    with open('test_inventory.csv', 'w', newline='') as file:
        fieldnames = ['product_name', 'quantity', 'bought_price', 'sold_price', 'expiration_date']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

def move_to_expired(item):
    # Move the expired item to expired.csv
    with open('expired.csv', 'a', newline='') as expired_file:
        fieldnames = ['product_name', 'quantity', 'bought_price', 'sold_price', 'expiration_date']
        writer = csv.DictWriter(expired_file, fieldnames=fieldnames)
        if not expired_file.tell():
            writer.writeheader()
        writer.writerow(item)
    print(f"{item['product_name']} expired and moved to expired.csv")

def buy_item(item, quantity, bought_price, sold_price, expiration_date):
    rows = []

    with open('test_inventory.csv', 'r+', newline='') as file:
        reader = csv.DictReader(file)
        rows = list(reader)

        matching_rows = [row for row in rows if row['product_name'] == item and row['expiration_date'] == expiration_date]

        if matching_rows:
            # If item with the same expiration date exists, add quantity to that row
            for row in rows:
                if row['product_name'] == item and row['expiration_date'] == expiration_date:
                    current_quantity = int(row['quantity'])
                    quantity = int(quantity)
                    row['quantity'] = str(current_quantity + quantity)
        else:
            # If no matching item, create a new row
            rows.append({
                'product_name': item,
                'quantity': quantity,
                'bought_price': bought_price,
                'sold_price': sold_price,
                'expiration_date': expiration_date
            })

        # Set the file cursor back to the beginning before writing
        file.seek(0)

        # Write all items to test_inventory.csv
        writer = csv.DictWriter(file, fieldnames=['product_name', 'quantity', 'bought_price', 'sold_price', 'expiration_date'])
        writer.writeheader()
        writer.writerows(rows)

        # Truncate the file in case the new content is shorter than the old content
        file.truncate()

    print(f"Added {quantity} {item}(s) to the inventory.")

def is_expired(expiration_date):
    with open('date.txt', 'r') as date_file:
        current_date = date_file.readline().strip()
    return datetime.strptime(expiration_date, '%Y-%m-%d') > datetime.strptime(current_date, '%Y-%m-%d')

def move_to_expired(item):
    with open('expired.csv', 'a', newline='') as expired_file:
        fieldnames = ['product_name', 'quantity', 'bought_price', 'sold_price', 'expiration_date']
        writer = csv.DictWriter(expired_file, fieldnames=fieldnames)
        if not expired_file.tell():
            writer.writeheader()
        writer.writerow(item)
    print(f"{item['product_name']} expired and moved to expired.csv")

def sell_item(item, quantity):
    rows = []
    sold_rows = []

    # Read the file contents into a list
    with open('test_inventory.csv', 'r') as file:
        rows = list(csv.DictReader(file))

    matching_rows = [row for row in rows if row['product_name'] == item]

    if not matching_rows:
        print(f"No {item}(s) found in the inventory.")
        return

    # Find the closest row based on expiration_date
    closest_row = min(matching_rows, key=lambda x: datetime.strptime(x['expiration_date'], '%Y-%m-%d'))

    # Calculate the total quantity available for sale
    total_quantity_available = sum(int(row['quantity']) for row in matching_rows)

    quantity = int(quantity)

    if total_quantity_available >= quantity:
        # If the total quantity available is sufficient
        remaining_quantity = quantity
        for row in matching_rows:
            current_quantity = int(row['quantity'])
            if current_quantity >= remaining_quantity:
                # If the current row has enough quantity, update it and break
                row['quantity'] = str(current_quantity - remaining_quantity)
                remaining_quantity = 0
                break
            else:
                # If the current row does not have enough quantity, update and continue to the next row
                remaining_quantity -= current_quantity
                row['quantity'] = '0'

        total_price = quantity * float(closest_row['sold_price'])
        revenue = (quantity * float(closest_row['sold_price'])) - (quantity * float(closest_row['bought_price']))
        print(f"Sold {quantity} {item}(s) with the closest expiration date for a total of ${total_price}.")
        sold_row = closest_row.copy()
        sold_row['quantity'] = str(quantity)
        sold_row['date_sold'] = get_current_date()
        sold_row['revenue'] = revenue
        sold_rows.append(sold_row)

        # Check if quantity becomes zero and remove the row
        if int(closest_row['quantity']) == 0:
            rows.remove(closest_row)
    else:
        print(f"Not enough {item}(s) with the closest expiration date in the inventory to sell.")

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

def get_current_date():
    try:
        with open('date.txt', 'r') as file:
            return file.readline().strip()
    except FileNotFoundError:
        return datetime.now().strftime('%Y-%m-%d')

def revenue(date):
    # Read the sold.csv file
    with open('sold.csv', 'r') as file:
        reader = csv.DictReader(file)

        # Create a variable to store total revenue for the specified date
        total_revenue = 0

        # Iterate through each row in the sold.csv file
        for row in reader:
            if row['date_sold'] == date:
                total_revenue += float(row['revenue'])

        # Print the total revenue for the specified date
        print(f"Total revenue on {date}: ${total_revenue:.2f}")

def main():
    parser = argparse.ArgumentParser(description="Inventory Management System")

    parser.add_argument('--display', action='store_true', help='Display current inventory')
    parser.add_argument('--buy', nargs=5, metavar=('item', 'quantity', 'bought price', 'sold price', 'expiration date'), help='Add items to the inventory')
    parser.add_argument('--sell', nargs=2, metavar=('item', 'quantity'), help='Sell items from the inventory')
    parser.add_argument('--advance-time', action='store_true', help='Advance time by a specified number of days')
    parser.add_argument('--revenue', metavar='date', help='Specify the date to calculate revenue.')

    args = parser.parse_args()

    if args.display:
        display_inventory()
    elif args.buy:
        buy_item(*args.buy)
    elif args.sell:
        sell_item(*args.sell)
    elif args.advance_time:
        advance_time(args.advance_time)
    elif args.revenue:
        revenue(args.revenue)
    else:
        print("No valid command provided. Use --display, --add, --advance-time or --sell.")

if __name__ == "__main__":
    main()
