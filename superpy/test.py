import pandas as pd
from date import *

df = pd.read_csv('test_inventory.csv')
sold = df[(df['sold'] == 'yes')]
sold.to_csv('sold.csv', mode='a', index=False, header=False)

df = df.drop(df[df.sold == 'yes'].index)
df.to_csv('test_inventory.csv', index=False)

inventory = df[['product_name', 'expiration_date']]
expiration = ""
def specific_inventory():
    selected = str(input("What product would you like to see the inventory from?[apple, pear, pineaple]"))
    if selected == "apple":
        apples = df[(df['product_name'] == 'apple')]
        print(apples) 
    elif selected == "pear":
        pears = df[(df['product_name'] == 'pear')]
        print(len(pears))
    elif selected == "pineaple":
        pineaples = df[(df['product_name'] == 'pineaple')]
        print(len(pineaples))
    else:
        print("that is not a viable option, please type in apple, pear or pineaple")


def test_inventory():
    print("Current inventory")
    data = open("inventory.txt", "r")
    items = data.readlines()
    for item in items:
        name, price, count = item.split(",")
        print("{0}\t{1}\t{2}".format(name, price, count))

def test_add_item(item, quantity, bought_price, sold_price, expiration_date):
    with open('test_inventory.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([item, quantity, bought_price, sold_price, expiration_date])
    print(f"Added {quantity} {item}(s) to the inventory.")

def sell_item(item, quantity):
    rows = []
    with open('test_inventory.csv', 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['product_name'] == item:
                current_quantity = int(row['quantity'])
                quantity = int(quantity)
                if current_quantity >= quantity:
                    row['quantity'] = str(current_quantity - quantity)
                    total_price = quantity * float(row['sold_price'])
                    print(f"Sold {quantity} {item}(s) for a total of ${total_price}.")
            rows.append(row)

    with open('test_inventory.csv', 'w', newline='') as file:
        fieldnames = ['product_name', 'quantity', 'sold_price', 'bought_price', 'expiration_date']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)