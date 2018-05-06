import pandas as pd
import numpy as np

def main():
    print("Please enter total number of companies: ")
    companies = 5 #int(input()), total number of companies
    markovian = False
    print("Please enter you seed company: ")
    s = 3 #int(input()), seed_company
    participation_vector = [1]*companies
    a = create_matrix_set_seed(s,companies)
    a = compute_participation(a, companies, participation_vector)
    print(pd.DataFrame(a))

def create_matrix_set_seed(s,companies):
    a = [[0 for i in range(companies)] for j in range(companies)]
    a[s][s] = 1
    return a

def compute_participation(a, companies, participation_vector):
    pv = participation_vector[:]
    for i in range(companies):
        for j in range(companies):
            if j != s: #seed company does not sell shares and retains full ownership
                if i == j:
                    pass # main diagonal remains 0 apart from seed company
                else:
                    participation = round(np.random.uniform(0.00,(pv[j])),2) ##random percent to 2 d.p
                    a[i][j] = participation
                    #a[i][i] = a[i][i] - t_sell
                    pv[j] = pv[j] - participation
    return a




