import re
import math

# leave blank for program to ask for input, or enter a pre-defined number and the program will input it for you, do not enter any other non-number chars besides a period
pay_rate = "9.5"
hours = "8"
goal = "1600"

def get_valid_input(prompt):
    while True:
        user_input = input(prompt)
        if re.search(r'^\d+(\.\d+)?$', user_input):
            return user_input
        print("Invalid input. Please enter a valid number.")

def calculate_time_to_goal():
    global pay_rate, hours, goal
    
    if not re.search(r'^\d+(\.\d+)?$', pay_rate):
        pay_rate = get_valid_input("Enter your hourly pay rate: ")
    else:
        print(f"Enter your hourly pay rate: {pay_rate}")
    if not re.search(r'^\d+(\.\d+)?$', hours):
        hours = get_valid_input("Enter the number of hours you work per week: ")
    else:
        print(f"Enter the number of hours you work per week: {hours}")
    if not re.search(r'^\d+(\.\d+)?$', goal):
        goal = get_valid_input("Enter your financial goal: ")
    else:
        print(f"Enter your financial goal: {goal}")
    
    pay_rate = float(pay_rate)
    hours = float(hours)
    goal = float(goal)
    
    total_hours = goal / pay_rate
    weeks = math.ceil(total_hours / hours)
    days = weeks * 7
    months = math.ceil(weeks / 4)

    print(f"\nIt will take you roughly {days} days/{weeks} weeks/{months} months")
    print("to reach your goal (assuming you spend no money)")

calculate_time_to_goal()