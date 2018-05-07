import pandas as pd
import numpy as np
import time
import matplotlib.pyplot as plt

def main(companies,markovian):
    print("Please enter total number of companies: ")
    #companies = companies #int(input()), total number of companies
    print("Please enter your seed company: ")
    s = 0 #int(input()), seed_company
    participation_vector = [1]*companies
    a = create_matrix_set_seed(s,companies)
    print("Markovian True or False: ")
    markovian = markovian #input()
    if markovian == False:
        a = compute_participation_non_markovian(a, companies, participation_vector, s)
    else:
        a = compute_participation_markovian(a, companies, participation_vector, s)
    print(pd.DataFrame(a))
    corporate_control_list, indirect_control_list = corporate_control(a, s, companies)
    print('The seed company has corporate control over the following companies: ', corporate_control_list)
    print('The seed company has indirect corporate control over the following companies: ', indirect_control_list)

def create_matrix_set_seed(s,companies):
    a = [[0 for i in range(companies)] for j in range(companies)]
    a[s][s] = 1
    return a

def compute_participation_non_markovian(a, companies, participation_vector, s):
    pv = participation_vector[:]
    for i in range(companies):
        for j in range(companies):
            if (i == (companies - 1)) and (j == (companies -1)):
                pass
            else:##this ensures the bottom right matrix value always remains 0.00
                if j != s: #seed company does not sell shares and retains full ownership
                    if i == j:
                        pass # main diagonal remains 0 apart from seed company
                    else:
                        participation = round(np.random.uniform(0.00,(pv[j])),2) ##random percent to 2 d.p
                        a[i][j] = participation
                        pv[j] = round(pv[j] - participation,2)
    return a

def compute_participation_markovian(a, companies, participation_vector, s):
    pv = participation_vector[:]
    pv[s] = 0
    for i in range(companies):
        if i != (companies-1):
            for j in range(companies):
                if j != s: #seed company does not sell shares and retains full ownership
                    if i == j:
                        pass # main diagonal remains 0 apart from seed company
                    else:
                        participation = round(np.random.uniform(0.00,(pv[j])),2) ##random percent to 2 d.p
                        a[i][j] = participation
                        pv[j] = round(pv[j] - participation,2)
        else:
            for j in range(companies-1):
                if j!=s: ##so the bottom right matrix value remains 0
                    a[i][j]=pv[j]
            a[companies - 2][companies - 1] = a[companies - 2][companies - 1] + pv[companies - 1] ##this ensures main diagonal remains 0 and last column aggrigates to 100%
    return a

def corporate_control(a,s,companies):
    corporate_control_list = []
    indirect_control_list = []
    indirect_control_calculation_list = [0]*companies
    for j in range(companies):
        if j != s:
            if a[s][j] > 0.5:
                corporate_control_list.append(int(j))
    if len(corporate_control_list)== 0:
        corporate_control_list = 'No companies'
        indirect_control_list= 'No indirect control'
        return corporate_control_list, indirect_control_list
    else: # len(corporate_control_list) != 0:
        for i in range(companies):
            if int(i) in corporate_control_list:
                pass ##we already have full control, no need for indirect control
            else:
                for j in range(companies):
                    indirect_control_calculation_list[i] = a[i][j] + indirect_control_calculation_list[i]
    for i in range(companies):
        if i != s:
            if indirect_control_calculation_list[i] > 0.5:
                indirect_control_list.append(int(i))
    if len(indirect_control_list) == 0:
        indirect_control_list = 'No indirect control'
    return corporate_control_list, indirect_control_list


def scalibility_testing():
    k = [2,4,6,8]
    n_makovian = []
    n_non_markovian = []
    average_time_non_markovian = []
    average_time_markovian = []
    for i in range(len(k)):
        companies = int(2**k[i])
        for i in range(2):
            if i == 0:
                total_elapsed = 0
                markovian = False
                for i in range(10):
                    start_time = time.time()
                    main(companies,markovian)
                    end_time = time.time()
                    elapsed = end_time - start_time
                    total_elapsed = total_elapsed + elapsed
                average_time_non_markovian.append(total_elapsed/10)
                n_non_markovian.append(companies)
            if i == 1:
                total_elapsed = 0
                markovian = True
                for i in range(10):
                    start_time = time.time()
                    main(companies,markovian)
                    end_time = time.time()
                    elapsed = end_time - start_time
                    total_elapsed = total_elapsed + elapsed
                average_time_markovian.append(total_elapsed/10)
                n_makovian.append(companies)
    plt.plot(n_non_markovian, average_time_non_markovian,color = 'red', label='Non-Markovian')
    plt.plot(n_makovian, average_time_markovian, color ='blue', label='Markovian')
    plt.xlabel("N - Companies")
    plt.ylabel("Average Time")
    plt.title("Scalibility Testing")
    plt.legend()
    plt.show()

scalibility_testing()


