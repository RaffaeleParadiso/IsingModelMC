FLAG = 1                # flag (Cold start [spin tutti 1]=0, Hot start [spin random]=1)

# in caso di analisi di un singolo reticolo di dimensione stabilita:
LATT_DIM = 10           # lattice dimensions (LxL)

# in caso di analisi di diversi reticoli di dimensione differente
LATT_DIM_START = 10
LATT_DIM_STOP = 70
PASSO_LATT_DIM = 10

# costanti per l'analisi MonteCarlo attraverso l'algoritmo Metropolis
IDECORREL = 100          # numero di volte che runno il metropolis prima di effettuare la misura
MEASURES = 100000        # number of measures

# costanti per studiare il reticolo in caso di un campo magnetico esterno fisso
# e temperatura fissati
EXTFIELD = 0             # extfield (valore del campo esterno)
BETA = 0.3               # beta (valore di 1/(kT) = beta, N.B. in questo caso lavoriamo in unità di k=1 e J(costante di accoppiamento)=1)

# costanti per studiare il reticolo in caso di temperatura variabile
BETA_START = 0.30
BETA_STOP = 0.51
PASSO_BETA = 0.01
