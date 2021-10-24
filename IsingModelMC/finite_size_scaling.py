'''Calcolo innanzituttamente tutte le sciusciettività, nella cartella suscettività, e i beta mella cartella beta 
poi il calore specifico, nella cartella calore_specifico, e poi riscalo tutto in funzione degli esponenti 
critici. Nella sezione grafici grafico i grafici graficamente'''

import os
import time
import numpy as np

import model.costants as c
import module.func as func

latt_dim_start=c.LATT_DIM_START
latt_dim_stop=c.LATT_DIM_STOP
latt_dim_passo=c.PASSO_LATT_DIM
gamma=c.GAMMA_TEORICO
nu=c.NU_TEORICO
beta_c=c.BETA_CRITICO

path='results_analysis'
pathernoster0='results_analysis/beta'
pathernoster1='results_analysis/suscettività'
pathernoster2='results_analysis/calore_specifico'
pathernoster3='results_analysis/magnetizzazione_riscalata'
pathernoster4='results_analysis/suscettività_riscalata'
pathernoster5='results_analysis/beta_riscalato'
pathernoster6='results_analysis/magnetizzazione_media'

pathlist=[path, pathernoster0, pathernoster1, pathernoster2, pathernoster3, pathernoster4, pathernoster5, pathernoster6]

for item in pathlist:
    if os.path.exists(item)==True:
        print('cartella %s esistente già' % item)
        continue
    else:
        print('cartella %s creata correttamente' % item)
        os.mkdir(item)

for lattice_dim in range(10, 60, 10):
    start=time.time()
    lista_beta=[]
    lista_suscettività=[]
    lista_calore_specifico=[]
    lista_magnetizzazione_media=[]
    #=========beta per reticolo {lattice_dim}============#
    if os.path.exists(f'results_analysis/beta/dim_{lattice_dim}_beta_list.txt') == True:
        continue
    else:
        lista_suscettività, lista_beta= func.susceptivity(lattice_dim)
        np.savetxt(f'results_analysis/beta/dim_{lattice_dim}_beta_list.txt', lista_beta)
      #=========suscettività per reticolo {lattice_dim}============#
    if os.path.exists(f'results_analysis/suscettività/dim_{lattice_dim}_suscettività.txt') == True:
        continue
    else:
        np.savetxt(f'results_analysis/suscettività/dim_{lattice_dim}_suscettività.txt', lista_suscettività)

    chi_rescaled=[]
    beta_rescaled=[]
    mean_magn_abs_rescaled=[]
    #=========magnetizzazione riscalata e mgnetizzazione media============#
    ##=============troppi if statements in tutte ste istruzioni===========#
    ###============il primo if statement non si puù guardare==============#
    if ((os.path.exists(f'results_analysis/magnetizzazione_riscalata/dim_{lattice_dim}_magn_rescaled.txt') == True) \
        and (os.path.exists(f'results_analysis/magnetizzazione_riscalata/dim_{lattice_dim}_magn_rescaled.txt')== True)):
        continue
    else:
        mean_magn_abs_rescaled, lista_beta = func.mean_magnetization(lattice_dim)
        np.savetxt(f'results_analysis/magnetizzazione_media/dim_{lattice_dim}_mean_magn.txt', mean_magn_abs_rescaled)
        mean_magn_abs_rescaled=np.array(mean_magn_abs_rescaled)*lattice_dim**(1/8)
        np.savetxt(f'results_analysis/magnetizzazione_riscalata/dim_{lattice_dim}_magn_rescaled.txt', mean_magn_abs_rescaled)
        np.savetxt(f'results_analysis/magnetizzazione_media/dim_{lattice_dim}_mean_magn.txt', mean_magn_abs_rescaled)
    #=========beta riscalati============#
    if os.path.exists(f'results_analysis/beta_riscalato/dim_{lattice_dim}_beta_rescaled.txt') == True:
        continue
    else:
        beta_arr_resc=(np.array(lista_beta)-beta_c)*lattice_dim**(1/nu)
        np.savetxt(f'results_analysis/beta_riscalato/dim_{lattice_dim}_beta_rescaled.txt', beta_arr_resc)
    #=========suscettività riscalata============#
    if os.path.exists(f'results_analysis/suscettività_riscalata/dim_{lattice_dim}_suscettività_rescaled.txt') == True:
        continue
    else:    
        lista_suscettività_arr=np.array(lista_suscettività)*1/(lattice_dim**(gamma/nu))
        np.savetxt(f'results_analysis/suscettività_riscalata/dim_{lattice_dim}_suscettività_rescaled.txt', lista_suscettività_arr)
    #=========calore specifico============#
    if os.path.exists(f'results_analysis/calore_specifico/dim_{lattice_dim}_calore_specifico.txt')==True:
        continue
    else:
        lista_calore_specifico, lista_beta = func.specific_heat(lattice_dim)
        np.savetxt(f'results_analysis/calore_specifico/dim_{lattice_dim}_calore_specifico.txt', lista_calore_specifico)
    print('tempo per reticolo:', lattice_dim, 'x', lattice_dim,' ', time.time()-start)
