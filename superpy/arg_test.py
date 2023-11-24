from argparse import *
from functions import *


# argparse calculator

parser = ArgumentParser(description="Welcome to the calculator, use this to do some calculations", epilog="Have fun!") 
subparsers = parser.add_subparsers(dest="command")

# Create calculator parser
calculator_parser = subparsers.add_parser("calculate", help="use this to calculate.")
calculator_parser.add_argument("calculation_type", type=str, help="Specify which type of calculation you whish to do")
calculator_parser.add_argument("number_1", type=int, help="The first number")
calculator_parser.add_argument("number_2", type=int, help="The second number")


# time parser
time_parser = subparsers.add_parser("time", help="Display current date and time.")


# parse arguments
args = parser.parse_args()

if args.command == "calculate":
    if args.calculation_type == "add":
        outcome = addition(args.number_1, args.number_2)

    if args.calculation_type == "subtract":
        outcome = substraction(args.number_1, args.number_2)

if args.command =="time":
    outcome = time()

if __name__ == "__main__":
    print(f"The outcome is: {outcome}")