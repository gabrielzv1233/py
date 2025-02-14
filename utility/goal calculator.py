import re
import math
from datetime import datetime, timedelta

# Leave blank (should look like var = "") for the program to ask for input, or enter a pre-defined number and the program will input it for you. Do not enter any other non-number characters besides a period.
# Do not set pay_rate, hours, or goal to "0".

pay_rate = "7.5"
hours = "69"
goal = "3200"
spending = "255"
current = ""

if not any(char.isdigit() and '1' <= char <= '9' for char in pay_rate):
  if not pay_rate == "":
    exit("pay_rate cannot be 0")
if not any(char.isdigit() and '1' <= char <= '9' for char in hours):
  if not hours == "":
    exit("hours cannot be 0")
if not any(char.isdigit() and '1' <= char <= '9' for char in goal):
  if not goal == "":
    exit("goal cannot be 0")

def checkvar(question, var):
    while True:
        if not re.match(r'^\d+(\.\d+)?$', var):
            text = input(question)
            if re.match(r'^\d+(\.\d+)?$', text):
                return float(text)
            else:
                print("Invalid input. Please enter a valid number.")
        else:
            print(question + var)
            return float(var)

def calculate_time_to_goal():
    global pay_rate, hours, goal, current, spending
    pay_rate = checkvar("Enter your hourly pay rate: ", pay_rate)
    hours = checkvar("Enter the number of hours you work per week: ", hours)
    goal = checkvar("Enter your financial goal: ", goal)
    spending = checkvar("Enter your average spendings in a week: ", spending)
    current = checkvar("Enter the current amount you have saved: ", current)
    pay_rate = float(pay_rate)
    hours = float(hours)
    current = float(current)
    goal = float(goal) - float(current)
    spending = float(spending)
    money_per_week = pay_rate * hours
    if current >= goal:
        print("You already have enough")
        exit(0)
    weeks = math.ceil(goal / (money_per_week - spending))
    days = weeks * 7
    months = weeks / 4
    today = datetime.now()
    target_date = today + timedelta(weeks=weeks)
    date = target_date.strftime("%Y/%m/%d")
    weekly_income = money_per_week
    net_savings_per_week = money_per_week - spending
    print(f"\nIt will take you roughly {days} days ({weeks} weeks or {months:.2f} months) to reach your goal. (Calculated to reach by {date}.)")
    print(f"Data:\n You make ${weekly_income:.2f} per week\n and spend ${spending:.2f} per week\n so you can add ${net_savings_per_week:.2f} to your savings every week")
calculate_time_to_goal()