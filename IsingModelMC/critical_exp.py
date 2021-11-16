import os
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit
import model.costants as c

def func_gamma_su_nu(x, a, b, c):
   return a+b*x**c

def func_nu(x, a, b, c):
   return a+b*x**c

if __name__ == '__main__':

   flag = c.FLAG
   latt_dim_start = c.LATT_DIM_START
   latt_dim_stop = c.LATT_DIM_STOP
   passo_latt_dim = c.PASSO_LATT_DIM
   i_decorrel = c.IDECORREL
   measures = c.MEASURES
   extfield = c.EXTFIELD
   beta_start = c.BETA_START
   beta_stop = c.BETA_STOP
   passo_beta = c.PASSO_BETA
   beta_c=c.BETA_CRITICO

   path='results_analysis/suscettività/'
   chi_max=[]
   beta_pseudo_critici = []
   beta_pseudo=[]
   beta=np.loadtxt('results_analysis/beta/beta_lattice_dim_10.txt')
   for i in range(latt_dim_start, latt_dim_stop, passo_latt_dim):
      beta_r=np.loadtxt(f'results_analysis/beta_riscalato/beta_riscalato_lattice_dim_{i}.txt')
      chi=np.loadtxt(f'results_analysis/suscettività_riscalata/suscettività_riscalata_lattice_dim_{i}.txt')
      chi_max.append(max(chi))
      beta_pseudo_critici.append(beta_r[np.argmax(chi)])
      beta_pseudo.append(beta[np.argmax(chi)])
   # param_opt = curve_fit(func_gamma_su_nu, chi_max, np.arange(latt_dim_start, latt_dim_stop, passo_latt_dim), maxfev=5000)
   # coeff, _ = param_opt
   # print(coeff[2]**(-1))

   y_teorico = func_nu(np.arange(latt_dim_start, latt_dim_stop, passo_latt_dim), beta_c, -0.49, -1.)
   # print(beta_pseudo_critici)
   # print(y_teorico)
   def func_nu(x, c):
      return beta_c+beta_pseudo_critici[3]*x**(-1/c)
   param_opt_2 = curve_fit(func_nu, np.arange(10,60,10), beta_pseudo, maxfev=100000)
   coeff, pcov = param_opt_2
   print(np.sqrt(np.diag(pcov)))
   print(coeff)
   plt.figure()
   plt.scatter(y_teorico,np.arange(latt_dim_start, latt_dim_stop, passo_latt_dim), label='Teorico')
   plt.scatter(coeff[0]+coeff[1]*np.arange(latt_dim_start, latt_dim_stop, passo_latt_dim)**(coeff[2]), np.arange(latt_dim_start, latt_dim_stop, passo_latt_dim), label='Sperimentale')
   plt.legend()
   plt.show()
