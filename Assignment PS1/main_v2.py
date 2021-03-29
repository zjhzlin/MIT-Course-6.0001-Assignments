# Name: Lynn ZHANG
# Time used:
def get_month_from_portion(invest_ratio, portion_down_payment, total_cost, current_savings, portion_saved, annual_salary,
                           semi_annual_raise):
    '''
    Given the params below, return how many months it takes to save up to the down payment.
    :param invest_ratio: annual investment ratio
    :param portion_down_payment: portion of down payment
    :param total_cost: total cost of the house
    :param current_savings: current savings
    :param portion_saved: portion saved per month
    :param annual_salary: annual salary
    :param semi_annual_raise: semi annual raise
    :return:how many months it takes to save up to the down payment
    '''
    month = 0
    while current_savings < (portion_down_payment * total_cost):
        # print(current_savings - (portion_down_payment * total_cost))
        invest_return = current_savings * invest_ratio / 12
        current_savings += portion_saved * annual_salary / 12 + invest_return
        month += 1
        if month % 6 == 0:
            annual_salary *= (1 + semi_annual_raise)
            # print("month",month,"salary increase",annual_salary)
    return month


def get_savings_from_portion(target_month, invest_ratio, current_savings, annual_salary, portion_saved):
    '''
    Return the savings with known portion and known target month
    :param target_month: target month to get the down payment
    :param invest_ratio: invest ratio
    :param current_savings: current savings
    :param annual_salary: annual salary
    :param portion_saved: portion saved per month
    :return:the savings with known portion and known target month
    '''
    for m in range(target_month):
        invest_return = current_savings * invest_ratio / 12
        current_savings += portion_saved * annual_salary / 12 + invest_return
        if m % 6 == 0:
            annual_salary *= (1 + semi_annual_raise)
    return current_savings

# Main
if __name__ == '__main__':
    portion_down_payment = 0.25
    invest_ratio = 0.04
    total_cost = 1000000
    semi_annual_raise = 0.07
    annual_salary = float(input("Enter your starting salary: "))

    # calculate if using all the money, whether it is possible to have the down payment in 36 months
    target_month = 36
    current_savings = 0
    max_savings = get_savings_from_portion(target_month, invest_ratio, current_savings, annual_salary, 1)
    # if not able to get the money in 36 months, state the fact
    if(max_savings < portion_down_payment * total_cost):
        print("It is not possible to pay the down payment in 36 months")

    # else, start the bisection search 0 - 10000
    else:
        low = 0
        high = 10000
        portion_saved = (low+high) / 2 / 10000
        month = 0
        steps = 0
        # exit condition: month == target
        while month != target_month:
            current_savings = 0
            month = get_month_from_portion(invest_ratio, portion_down_payment, total_cost, current_savings,
                                           portion_saved, annual_salary, semi_annual_raise)
            if month < target_month:
                high = portion_saved * 10000
            elif month > target_month:
                low = portion_saved * 10000
            else:
                break
            portion_saved = ( low + high ) / 2 / 10000
            steps += 1
        # print out the results
        print('Best savings rate: ', portion_saved)
        print('Steps in bisection search: ', steps)
