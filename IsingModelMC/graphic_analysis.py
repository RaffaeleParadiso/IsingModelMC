import os
import matplotlib.pyplot as plt
import numpy as np

beta_start=0.34
beta_stop=0.48

#########================provo a costruire array 3D di suscettività, magnetizzazione, calore specifico
#########================con i rispettivi errori================================######################
array_di_tutt_cos=np.ndarray((3, 5, 281)) ####3= numero di elementi, si poteva fa meglio, 5 sono le lattice dim e 281 len(osservabile)
path='results_analysis'
for direttori in os.listdir(path):
    latt=0
    if os.path.join(path, direttori).endswith('suscettività')==True: #### #0 = suscettività
        for lattici in os.listdir(os.path.join(path, direttori)):
            load=os.path.join(path, direttori, lattici)
            array_di_tutt_cos[0, latt]=np.loadtxt(load)
            latt+=1

    cartella_in_questione=os.path.join(path, direttori)
    if cartella_in_questione.endswith('magnetizzazione')==True:  #### #1 = magnetizzazione
        for lattici in os.listdir(cartella_in_questione):
            load1=os.path.join(cartella_in_questione, lattici)
            array_di_tutt_cos[1, latt]=np.loadtxt(load1)
            latt+=1

    if cartella_in_questione.endswith('calore_specifico')==True: #### #2 = calore specifico
        for lattici in os.listdir(cartella_in_questione):
            load2=os.path.join(cartella_in_questione, lattici)
            array_di_tutt_cos[2, latt]=np.loadtxt(load2)
            latt+=1
#####=======array degli errori===========########
#####=======[:,0] sigma suscettività=====########
#####=======[:,1] sigma mean magn========########
#####=======[:,2] sigma calore specifico=########
array_di_tutti_i_sigmi=np.ndarray((5,3,281))
path='results_analysis/sigma'
latto=0
for sigma_latt in os.listdir(path):
    sigma_latt=os.path.join(path, sigma_latt)
    for files in os.listdir(sigma_latt):
        files=os.path.join(sigma_latt,files)
        if files.endswith(f'susceptibility_lattice_dim_{(latto+1)*10}.txt')==True:
            array_di_tutti_i_sigmi[latto,0]=np.loadtxt(files)
        if files.endswith(f'mean_magn_lattice_dim_{(latto+1)*10}.txt') == True:
            array_di_tutti_i_sigmi[latto, 1]=np.loadtxt(files)
        if files.endswith(f'specific_heat_lattice_dim_{(latto+1)*10}.txt') == True:
            array_di_tutti_i_sigmi[latto, 2]=np.loadtxt(files)
    latto+=1

#######============Prendi i graficini piccini picciò=====appena un po'=======############
#######======================================================================############
'''Fa i grafici, i valori 0,1,2 come indici di array sono risp. suscettività,
magnetizzazione media e calore specifico, con i corrispettivi errori'''
beta=np.loadtxt('results_analysis/beta/beta_lattice_10.txt')
plt.figure()
for ii in range(5):
    plt.errorbar(beta, array_di_tutt_cos[0,ii], yerr=array_di_tutti_i_sigmi[ii,0]*2, fmt='.', mfc='red',
                  mec='green', ms=0.4, mew=2, capsize=2)
plt.show()
######============Rescaled quantity====================##################
######=================================================##################
array_rescaled=np.ndarray((3,5,281)) ####3= numero di elementi, si poteva fa meglio, 5 sono le lattice dim e 281 len(osservabile)
path='results_analysis'
for direttori in os.listdir(path):
    latt=0
    if os.path.join(path, direttori).endswith('suscettività_riscalata')==True:
        for lattici in os.listdir(os.path.join(path, direttori)):
            load=os.path.join(path, direttori, lattici)
            array_rescaled[0, latt]=np.loadtxt(load)
            latt+=1

    cartella_in_questione=os.path.join(path, direttori)
    if cartella_in_questione.endswith('magnetizzazione_riscalata')==True:
        for lattici in os.listdir(cartella_in_questione):
            load1=os.path.join(cartella_in_questione, lattici)
            array_rescaled[1, latt]=np.loadtxt(load1)
            latt+=1

    if cartella_in_questione.endswith('beta_riscalato')==True:
        for lattici in os.listdir(cartella_in_questione):
            load2=os.path.join(cartella_in_questione, lattici)
            array_rescaled[2, latt]=np.loadtxt(load2)
            latt+=1

#####=====gli errori riscalano allo stesso modo, qui sotto plot di 2=(beta-beta_c)^... contro suscettività riscalata e
#####=====in yerr gli errori sono riscalati allo stesso modo della sciusciettività
plt.figure()
for ii in range(5):
    plt.errorbar(array_rescaled[2,ii], array_rescaled[0,ii], yerr=array_di_tutti_i_sigmi[ii,0]*2/((ii+1)*10**(7/4)), fmt='.', mfc='red',
                  mec='green', ms=0.4, mew=2, capsize=2)
plt.show()
##########====================================================################
##########==========grafico binder con errori=================################
##########====================================================################
error_binder=np.loadtxt(f'results_analysis/binder_vs_beta/binder_sigma_range_{beta_start}_{beta_stop}.txt')
binder_value=np.loadtxt(f'results_analysis/binder_vs_beta/binder_vs_beta_range_{beta_start}_{beta_stop}.txt')
beta_range=np.loadtxt(f'results_analysis/binder_vs_beta/beta_list_range_{beta_start}_{beta_stop}.txt')

plt.figure()
for ii in range(5):
    plt.errorbar(beta_range, binder_value[ii], yerr=error_binder[ii,:139]*2, fmt='.', mfc='red',
                  mec='green', ms=0.4, mew=2, capsize=2)
plt.show()