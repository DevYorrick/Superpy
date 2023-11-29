# Imports
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

# Do not change these lines.
__winc_id__ = "a2bc36ea784242e4989deb157d527ba0"
__human_name__ = "superpy"


# Your code below this line.
console = Console()
def display_inventory():
    try:
        # Read the CSV file into a DataFrame
        df = pd.read_csv('inventory.csv')

        # Filter out rows with quantity equal to 0
        df = df[df['quantity'] > 0]

        # Create a Rich Table
        table = Table(show_header=True, header_style="bold cyan")
        table.add_column("Product Name", style="green")
        table.add_column("Quantity")
        table.add_column("Bought Price", justify="right")
        table.add_column("Sold Price", justify="right")
        table.add_column("Expiration Date")

        # Iterate over DataFrame rows and add them to the Rich Table
        for _, row in df.iterrows():
            table.add_row(
                f"[bold cyan]{row['product_name']}[/bold cyan]",
                f"[bold]{row['quantity']}[/bold]",
                f"[bold]{row['bought_price']}[/bold]",
                f"[bold]{row['sold_price']}[/bold]",
                f"[bold cyan]{row['expiration_date']}[/bold cyan]"
            )

        # Print the Rich Table
        console.print(table)

    except FileNotFoundError:
        console.print("[red]Inventory file not found.[/red]")

def buy_item():
    # Mapping of product names to prices
    product_prices = {
        'Apples': {'bought_price': 0.5, 'sold_price': 5},
        'Oranges': {'bought_price': 1, 'sold_price': 4},
        'Mangos': {'bought_price': 1.2, 'sold_price': 6.5},
        'Grapes': {'bought_price': 0.8, 'sold_price': 2},
        'Melons': {'bought_price': 2, 'sold_price': 8},
        'Pears': {'bought_price': 0.6, 'sold_price': 1.5},
    }

    try:
        # Get user input for product and quantity
        product_name = input("What product would you like to buy? (Apples, Oranges, Mangos, Grapes, Melons or Pears): ")
        quantity = int(input(f"How many {product_name} would you like to buy? "))

        # Get prices based on the selected product
        bought_price = product_prices[product_name]['bought_price']
        sold_price = product_prices[product_name]['sold_price']

        # Calculate expiration date (current date + 10 days)
        with open('date.txt', 'r') as date_file:
            current_date = datetime.strptime(date_file.readline().strip(), '%Y-%m-%d')
        
        expiration_date = (current_date + timedelta(days=10)).strftime('%Y-%m-%d')

        # Read the inventory.csv file
        with open('inventory.csv', 'r+', newline='') as file:
            reader = csv.DictReader(file)
            rows = list(reader)

            # Check if the item with the same expiration date exists
            matching_rows = [row for row in rows if row['product_name'] == product_name and row['expiration_date'] == expiration_date]

            if matching_rows:
                # If item with the same expiration date exists, add quantity to that row
                for row in rows:
                    if row['product_name'] == product_name and row['expiration_date'] == expiration_date:
                        current_quantity = int(row['quantity'])
                        quantity = int(quantity)
                        row['quantity'] = str(current_quantity + quantity)
            else:
                # If no matching item, create a new row
                rows.append({
                    'product_name': product_name,
                    'quantity': quantity,
                    'bought_price': bought_price,
                    'sold_price': sold_price,
                    'expiration_date': expiration_date
                })

            # Set the file cursor back to the beginning before writing
            file.seek(0)

            # Write all items to inventory.csv
            writer = csv.DictWriter(file, fieldnames=['product_name', 'quantity', 'bought_price', 'sold_price', 'expiration_date'])
            writer.writeheader()
            writer.writerows(rows)

            # Truncate the file in case the new content is shorter than the old content
            file.truncate()

        print(f"Added {quantity} {product_name}(s) to the inventory with expiration date {expiration_date}.")

    except ValueError:
        console.print("[red]Invalid input. Please enter a valid quantity.[/red]")
    except KeyError:
        console.print("[red]Invalid product. Please select a valid product from the list.[/red]")

def is_expired(expiration_date):
    with open('date.txt', 'r') as date_file:
        current_date = date_file.readline().strip()
    return datetime.strptime(expiration_date, '%Y-%m-%d') > datetime.strptime(current_date, '%Y-%m-%d')

def sell_item(item, quantity):
    rows = []
    sold_rows = []

    # Read the file contents into a list
    with open('inventory.csv', 'r') as file:
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

    # Write remaining items to inventory.csv
    with open('inventory.csv', 'w', newline='') as file:
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

def plot_revenue_over_time():
    # Read the sold.csv file
    df = pd.read_csv('sold.csv')

    # Convert 'date_sold' to datetime
    df['date_sold'] = pd.to_datetime(df['date_sold'])

    # Group by date and sum the revenue
    revenue_over_time = df.groupby('date_sold')['revenue'].sum()

    # Plot the data
    plt.figure(figsize=(10, 6))
    plt.plot(revenue_over_time.index, revenue_over_time.values, marker='o')
    plt.title('Revenue Over Time')
    plt.xlabel('Date')
    plt.ylabel('Revenue')
    plt.grid(True)
    plt.show()

def main():
    parser = argparse.ArgumentParser(description="Inventory Management System")

    parser.add_argument('--display', action='store_true', help='Display current inventory')
    parser.add_argument('--buy', action='store_true', help='Add items to the inventory')
    parser.add_argument('--sell', nargs=2, metavar=('item', 'quantity'), help='Sell items from the inventory')
    parser.add_argument('--advance-time', action='store_true', help='Advance time by a specified number of days')
    parser.add_argument('--revenue', metavar='date', help='Specify the date to calculate revenue.')
    parser.add_argument('--revenue_over_time', action='store_true', help='Displays the revenue over time using matplotlib')
    parser.add_argument('--set-date', action='store_true', help='Set a specific date, no other input besides the --set_date command is needed')

    args = parser.parse_args()

    if args.display:
        display_inventory()
    elif args.buy:
        buy_item()
    elif args.sell:
        sell_item(*args.sell)
    elif args.advance_time:
        advance_time(args.advance_time)
    elif args.revenue:
        revenue(args.revenue)
    elif args.revenue_over_time:
        plot_revenue_over_time()
    elif args.set_date:
        print(set_date())
    else:
        print("No valid command provided. Use --display, --add, --advance-time or --sell.")

if __name__ == "__main__":
    main()
