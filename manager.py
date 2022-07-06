from sklearn.metrics import max_error
from ref_index import simulations_matrix
from mortgage import mortgage_life
from matplotlib import pyplot as plt
import numpy as np

def full_simulation(n_months:int, n_months_left:int, amount, n_simulations:int,
                    differential:float, best_fixed_rate:float, worst_variable_rate:float): 
    
    simulations = simulations_matrix(n_months, n_months - n_months_left, n_simulations, differential)
    
    # Calculate the mortgage life for the best fixed rate
    i_rate_array = np.zeros(n_months)
    i_rate_array[n_months-n_months_left:] = best_fixed_rate
    _, _, fix_interest = mortgage_life(amount, i_rate_array)
    b_fix_cum_interest = np.cumsum(fix_interest)
    
    # Calculate the mortgage life for the worst variable rate
    i_rate_array = np.zeros(n_months)
    i_rate_array[n_months-n_months_left:] = worst_variable_rate
    _, _, fix_interest = mortgage_life(amount, i_rate_array)
    w_fix_cum_interest = np.cumsum(fix_interest)
    
    #boundaries for the plot
    boundaries = np.array(simulations).flatten()
    min_boundary = boundaries.min()
    max_boundary = boundaries.max()
    
    fig, ax = plt.subplots(figsize=(20,15))
    fig.suptitle(f'Euribor monte carlo (n_sims = {n_simulations})', fontsize=30)
    for i in simulations[:]:
        ax.plot(i, alpha=0.7)
        
    ax.axhline(0.0135, color='black', lw=5, label='1,35%')
    ax.axhline(0.03, color='blue', lw=5, label='3,0%')
    ax.legend(title='Fixed interest rates')
    ax.xaxis.label.set_text('Months')
    ax.yaxis.label.set_text('Interest rate')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    for i in range(3, n_months, 12):
        ax.vlines(i, min_boundary , max_boundary, color='black', linestyle='dashed', alpha=0.5)
    
    plt.show()
    fig.savefig(f'euribor_monte_carlo_n_sims_{n_simulations}.png')
    
    fig, ax = plt.subplots(figsize=(20,15), tight_layout=True)
    fig.suptitle(f'Total interests paid (n_sims = {n_simulations})', fontsize=30)
    min_interest = 0
    max_interest = 0
    for i in simulations:
        _, _, interest = mortgage_life(amount, i)
        cum_interest = np.cumsum(interest)
        if cum_interest.max() > max_interest: max_interest = cum_interest.max()
        color = 'green'
        if cum_interest[-1] > b_fix_cum_interest[-1] and cum_interest[-1] < w_fix_cum_interest[-1]:
            color = 'orange'
        if cum_interest[-1] > w_fix_cum_interest[-1]:
            color = 'red'
            
        ax.plot(cum_interest, color=color)
        
    ax.axhline(b_fix_cum_interest[-1], color='black', lw=5, label='1,35%')
    ax.axhline(w_fix_cum_interest[-1], color='blue', lw=5, label='3,0%')
    ax.legend(title='Fixed interest rates')
    ax.xaxis.label.set_text('Months')
    ax.yaxis.label.set_text('Interest rate')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    for i in range(3, n_months, 12):
        ax.vlines(i, min_interest, max_interest, color='black', linestyle='dashed', alpha=0.3)
    
    plt.show()
    
    fig.savefig(f'total_interests_paid_n_sims_{n_simulations}.png')