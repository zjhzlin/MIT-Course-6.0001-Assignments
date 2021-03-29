# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    portion_down_payment = 0.25
    current_savings = 0
    r = 0.04

    annual_salary = float(input("Enter your annual salary: "))
    portion_saved = float(input("Enter the percent of your sa12lary to save, as a decimal: "))
    total_cost = float(input("Enter the cost of your dream house: "))
    semi_annual_raise = float(input("Enter the semi-annual raise, as a decimal: "))

    month = 0
    while current_savings < (portion_down_payment * total_cost):
        invest_return = current_savings * r / 12
        current_savings += portion_saved * annual_salary / 12 + invest_return
        month += 1
        if month%6 == 0:
            annual_salary *= (1 + semi_annual_raise)
            #print("month",month,"salary increase",annual_salary)

    print("number of months:", month)


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
