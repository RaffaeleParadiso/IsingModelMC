import numpy as np
from scipy.optimize import curve_fit
import model.costants as c
import sympy as sp
import matplotlib.pyplot as plt

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
#---------------Indici gamma e nu----------------------------------------
def func_gamma_su_nu(x, b, c):
    return b*x**c

for i in range(latt_dim_start, latt_dim_stop, passo_latt_dim):
    beta_r = np.loadtxt(
        f'results_analysis/beta_riscalato/beta_riscalato_lattice_dim_{i}.txt')
    chi = np.loadtxt(
        f'results_analysis/suscettività/suscettività_lattice_dim_{i}.txt')
    chi_max_not_rescaled.append(max(chi))
    beta_pseudo_critici.append(beta_r[np.argmax(chi)])
    beta_pseudo.append(beta[np.argmax(chi)])


def func_nu(x, c):
    'Funzione per il calcolo di nu tramite beta_pc=beta_c+xL^(-1/nu)'
    return beta_c+max(beta_pseudo_critici)*x**(-1/c)


opt_par1, cov_1 = curve_fit(
    func_gamma_su_nu, L_array, chi_max_not_rescaled, maxfev=100000)  # ok funziona
opt_par2, cov_2 = curve_fit(func_nu, np.arange(
    10, 60, 10), beta_pseudo, maxfev=100000)

# vedi meglio come registra le covarianze
print(f'Parametri fit gamma/nu: {opt_par1}, sigma = {np.sqrt(cov_1)}')
print(f'Parametri fit nu : {opt_par2}, sigma = {np.sqrt(cov_2[0])}')
#----------------------------------------------------------------------------------------------

#---------------Indice delta-------------------------------------------------------------------
#Cerchiamo di plottare l'esponente critico della magnetizzazione alla transizione di fase:
#steps: 1) scrivo la funzione che approssima l'andamento della magnetizzazione
#       2) curve_fit su func_magnetization
#       3) derivo func_magnetization per trovare i massimi della derivata corrispondenti ai cambi di concavità della magn.
#       4) salvo i punti della magnetizzazione a cui ho trovato i cambi di concavità, quindi i massimi di fprimo
#       5) curve_fit su M = xi^(-delta/nu) con xi = approx L

#1)
def func_magnetization(x, a, b, c, d):
   return a+b*np.tanh(c*x-d)

#Derivo simbolicamente e riconverto in funzione numerica
x, a, b, c, d =sp.symbols('x a b c d', real=True)
f=a+b*sp.tanh(c*x-d)
dfdx=sp.diff(f, x)
print(f'Derivata di func_magnetization: {dfdx}')
dfdx_num=sp.lambdify((x, a, b, c, d), dfdx)

beta_critici_magn=[]
valore_magn_corrispondente_beta_c=[]
c=0

#2), 3), 4)
for L in L_array:
   path='results_analysis'
   mean_magn=np.loadtxt(f'{path}/magnetizzazione_media/magnetizzazione_media_lattice_dim_{L}.txt')
   # mean_magn_r=np.loadtxt(f'{path}/magnetizzazione_riscalata/magnetizzazione_riscalata_lattice_dim_{L}.txt')
   beta_array=np.loadtxt(f'{path}/beta/beta_lattice_dim_{L}.txt')
   opt, covar= curve_fit(func_magnetization, beta_array, mean_magn, maxfev=100000)
   fprimo=dfdx_num(beta_array, a=opt[0], b=opt[1], c=opt[2], d=opt[3])
   beta_critici_magn.append(beta_array[np.argmax(fprimo)])
   valore_magn_corrispondente_beta_c.append(mean_magn[np.argmax(fprimo)])
   c+=1
   
#5)
def delta_func(x, b):
   return x**(-b)  #M va come xi^(-delta/nu), dove xi circa L

opt_delta, cov_delta=curve_fit(delta_func, L_array, valore_magn_corrispondente_beta_c, maxfev=100000)
print(f'Valore indice delta: {opt_delta}')
print(f"sigma sull'indice delta: {np.sqrt(cov_delta)}")
print(f'Parametri per L = 50 : a = {opt[0]} +- {np.sqrt(covar[0, 0])}, b = {opt[1]} +- {np.sqrt(covar[1, 1])}, c = {opt[2]} +- {np.sqrt(covar[2, 2])}, d = {opt[3]} +- {np.sqrt(covar[3, 3])}')
#--------------------------------------------------------------------------------------------------------
#plotto la funzione func_magnetization vs M
x=np.arange(0, 0.5, 0.01)
y=func_magnetization(beta_array, a=opt[0], b=opt[1], c=opt[2], d=opt[3])
plt.scatter(beta_array, mean_magn, s=2, c='blue',label=r'$\langle|M|\rangle$')
plt.xlabel(r'$\beta$', fontsize=14)
plt.ylabel(r'$\langle|M|\rangle$', fontsize=14)
plt.plot(beta_array, y, 'g--', label='f(x)=a+b*tanh(cx-d)')
plt.title('Plot a confronto per L = 50', fontsize=18)
plt.legend()
plt.show()






