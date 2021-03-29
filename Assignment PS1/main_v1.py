# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    portion_down_payment = 0.25
    r = 0.04
    total_cost = 1000000
    semi_annual_raise = 0.07
    annual_salary_original = float(input("Enter your starting salary: "))

    # calculate if using all the money, whether it is possible to have the money in 36 months
    max_savings = 0
    annual_salary = annual_salary_original
    for m in range(36):
        invest_return = max_savings * r / 12
        max_savings += 1 * annual_salary / 12 + invest_return
        if m%6 == 0:
            annual_salary *= (1 + semi_annual_raise)
    # if not able to get the money in 36 months, state the fact
    if(max_savings < portion_down_payment * total_cost):
        print("It is not possible to pay the down payment in 36 months")
    # else, then continue
    # bisection search 0 - 10000
    else:
        low = 0
        high = 10000
        portion_saved = (low+high) / 2 / 10000
        month = 0
        steps = 0
        while month != 36:
            print('portion_saved is', portion_saved)
            current_savings = 0
            annual_salary = annual_salary_original
            while current_savings < (portion_down_payment * total_cost):
                print(current_savings - (portion_down_payment * total_cost))
                invest_return = current_savings * r / 12
                current_savings += portion_saved * annual_salary / 12 + invest_return
                month += 1
                if month%6 == 0:
                    annual_salary *= (1 + semi_annual_raise)
                    #print("month",month,"salary increase",annual_salary)
            print('month:',month)
            if month < 36:
                high = portion_saved * 10000
            elif month > 36:
                low = portion_saved * 10000
            else:
                break
            portion_saved = ( low + high ) / 2 / 10000
            steps += 1
            month = 0
            print(low, high, portion_saved)
        print('Best savings rate: ', portion_saved)
        print('Steps in bisection search: ', steps)
