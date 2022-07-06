import pandas as pd
import numpy as np
import random
from scipy.stats import qmc

def euribor() -> pd.DataFrame:
    euribor = pd.read_csv('euribor_1m.csv', sep=';', header=None)
    euribor_rates = euribor.values[:,1]
    return euribor_rates

def r_sign():
    if random.random() < 0.5: return -1
    return 1

def sobol_index(n: int) -> np.array:
    return qmc.Sobol(1, scramble=True).random(n)

def halton_index(n: int) -> np.array:
    return qmc.Halton(1, scramble=True).random(n)

def simulations_matrix(n_months, starting_index, n_simulations, differential):
    
    euribor_volatility = (euribor()/100).std()
    salty_trend = np.concatenate([np.linspace(200,150,120)/100000,
                                  np.linspace(50,0,120)/100000,
                                  np.linspace(0,-100,120)/100000])
    
    sims = []
    for _ in range(n_simulations):
        sims.append(halton_index(n_months))
    
    for i, index in enumerate(sims):
        current_val = euribor()[0]/100
        for j,_ in enumerate(index):
            current_val = current_val + (r_sign()*euribor_volatility*index[j]+salty_trend[j])
            if current_val < 0:
                current_val += 0.005
            index[j] = current_val/10
            if j < starting_index:
                index[j] = 0
        sims[i] = index.flatten()+differential
                
    return sims


simulations_matrix(12, 0, 100, 0)