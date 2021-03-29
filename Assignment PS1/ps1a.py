# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press ⌘F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    portion_down_payment = 0.25
    current_savings = 0
    r = 0.04

    annual_salary = float(input("Enter your annual salary: "))
    portion_saved = float(input("Enter the percent of your sa12lary to save, as a decimal: "))
    total_cost = float(input("Enter the cost of your dream house: "))

    month = 0
    while current_savings < (portion_down_payment * total_cost):
        invest_return = current_savings * r / 12
        current_savings += portion_saved * annual_salary / 12 + invest_return
        month += 1

    print("number of months:", month)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
