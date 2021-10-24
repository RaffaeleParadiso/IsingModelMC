import module.func as fnc
import matplotlib.pyplot as plt

chi = True

latt_dim_start = 10
latt_dim_stop = 60
passo_latt_dim = 10

if chi == True:
    plt.figure()
    for i in range(latt_dim_start, latt_dim_stop, passo_latt_dim):
        chi, bet = fnc.susceptivity(i)
        plt.scatter(bet, chi)
    chi100, bet100 = fnc.susceptivity(100)
    plt.scatter(bet100, chi100)
    plt.show()