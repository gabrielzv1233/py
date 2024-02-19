import re
import math

# leave blank for program to ask for input, or enter a pre-defined number and the program will input it for you, do not enter any other non-number chars besides a period
# do not set pay_rate, hours, or goal to "0"
pay_rate = "9.5"
hours = "5"
goal = "1600"
spending = "5"
current = "48"

def checkvar(question, var):
    while True:
        if not re.match(r'^\d+(\.\d+)?$', var):
            text = input(question)
            if re.match(r'^\d+(\.\d+)?$', text):
                return float(text)
            else:
                print("Invalid input. Please enter a valid number.")
        else:
            return float(var)

def calculate_time_to_goal():
    global pay_rate, hours, goal, current, spending
    pay_rate = checkvar("Enter your hourly pay rate: ", pay_rate)
    hours = checkvar("Enter the number of hours you work per week: ", hours)
    goal = checkvar("Enter your financial goal: ", goal)
    spending = checkvar("Enter your average spendings in a week: ", spending)
    current = checkvar("Enter the current ammount you have saved: ", current)
    pay_rate = float(pay_rate)
    hours = float(hours)
    current = float(current)
    goal = float(goal) - float(current)
    spending = float(spending)
    money_per_week = pay_rate * hours
    if current >= goal:
        print("you already have enough")
        exit(0)
    weeks = math.ceil(goal / (money_per_week - spending))
    days = weeks * 7
    months = weeks / 4

    print(f"\nIt will take you roughly {days} days/{weeks} weeks/{months} months")
    print("to reach your goal (assuming you spend no money)")
    print(f"data:\n You make ${money_per_week}/week\n and spend ${spending}/week\n so you can add ${(money_per_week - spending)} to your savings every week")

calculate_time_to_goal()