#------------------------------------------------------------------------------
FLAG = 1                # flag (Cold start [spin tutti 1]=0, Hot start [spin random]=1)
#------------------------------------------------------------------------------
# costanti per studiare il reticolo in caso di dimensione variabile
LATT_DIM_START = 10
LATT_DIM_STOP = 60
PASSO_LATT_DIM = 10
LATT_DIM_L = [10, 20, 30, 40, 50]
#------------------------------------------------------------------------------
# costanti per l'analisi MonteCarlo attraverso l'algoritmo Metropolis
IDECORREL = 100          # numero di volte che runno il metropolis prima di effettuare la misura
MEASURES = 100000        # number of measures
#------------------------------------------------------------------------------
EXTFIELD = 0             # extfield (valore del campo esterno)
#------------------------------------------------------------------------------
# costanti per studiare il reticolo in caso di temperatura variabile
BETA_START = 0.300
BETA_STOP = 0.500
PASSO_BETA = 0.001
#------------------------------------------------------------------------------
GAMMA_TEORICO=7/4
NU_TEORICO=1
BETA_TEORICO=1/8
ALPHA_TEORICO=0
BETA_CRITICO=0.44068
#------------------------------------------------------------------------------
