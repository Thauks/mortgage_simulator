import numpy as np

def actualization(interest:float, n_months:int) -> float:
    
    if interest==0:
        return 0
    
    return (1-((1+(interest/12))**-n_months))/(interest/12)

def fee(amount:float, interest:float, n_months:int) -> float:
    
    if interest==0:
        return round(amount/n_months, 2)
    
    return round(amount/actualization(interest, n_months), 2)

def interest_paid(amount:float, interest:float) -> float:
    
    if interest == 0:
        return 0
    return round(amount*interest/12, 2)

def mortgage_life(amount:float, i_rate_array:np.array):
    n_months = len(i_rate_array)
    amount_array = np.zeros(n_months)
    amount_array[0] = amount
    fee_array = np.zeros(n_months)
    interest_array = np.zeros(n_months)

    last_interest = -1
    fee_paid = fee(amount, i_rate_array[0], n_months)
    for i in range(n_months-1):
        if last_interest != i_rate_array[i]:
            fee_paid = fee(amount_array[i], i_rate_array[i], n_months-i)

        i_paid = interest_paid(amount_array[i], i_rate_array[i])
        if i_paid < 0:
            i_paid = 0
        amortization = fee_paid - i_paid
        fee_array[i] = fee_paid
        amount_array[i+1] = amount_array[i] - amortization
        interest_array[i] = i_paid
    
    fee_array[-1] = amount_array[-1]   
    interest_array[-1] = interest_paid(amount_array[-1], i_rate_array[-1]) 
        
    return amount_array, fee_array, interest_array