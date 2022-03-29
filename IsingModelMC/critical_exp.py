import numpy as np
from scipy.optimize import curve_fit
import model.costants as c


def func_gamma_su_nu(x, b, c):
    return b*x**c

latt_dim_start = c.LATT_DIM_START
latt_dim_stop = c.LATT_DIM_STOP
passo_latt_dim = c.PASSO_LATT_DIM
beta_c = c.BETA_CRITICO
L_array = np.arange(10, 51, 10)

path = 'results_analysis/suscettività/'
chi_max = []
chi_max_not_rescaled = []
beta_pseudo_critici = []
beta_pseudo = []
beta = np.loadtxt('results_analysis/beta/beta_lattice_dim_10.txt')
for i in range(latt_dim_start, latt_dim_stop, passo_latt_dim):
    beta_r = np.loadtxt(
        f'results_analysis/beta_riscalato/beta_riscalato_lattice_dim_{i}.txt')
    chi = np.loadtxt(
        f'results_analysis/suscettività/suscettività_lattice_dim_{i}.txt')
    chi_max_not_rescaled.append(max(chi))
    beta_pseudo_critici.append(beta_r[np.argmax(chi)])
    beta_pseudo.append(beta[np.argmax(chi)])


def func_nu(x, c):
    'Funzione per il calcolo di nu tramite beta_pc=beta_c+xL^(1/nu)'
    return beta_c+max(beta_pseudo_critici)*x**(-1/c)


opt_par1, cov_1 = curve_fit(
    func_gamma_su_nu, L_array, chi_max_not_rescaled, maxfev=100000)  # ok funziona
opt_par2, cov_2 = curve_fit(func_nu, np.arange(
    10, 60, 10), beta_pseudo, maxfev=100000)

# vedi meglio come registra le covarianze
print(f'Parametri fit gamma/nu: {opt_par1}, sigma = {np.sqrt(cov_1[0])}')
print(f'Parametri fit nu : {opt_par2}, sigma = {np.sqrt(cov_2[0])}')
