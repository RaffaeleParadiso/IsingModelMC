import numpy as np
from numba import njit

def initialize_lattice(start, dim_latt):
    '''
    Assegno la configurazione di partenza della catena di Markov
    '''
    lattice_n = np.zeros((dim_latt, dim_latt))
    if start == 0:
        lattice_n = np.ones((dim_latt, dim_latt))
    if start == 1:
        init_matrix_random = np.random.random((dim_latt, dim_latt))
        lattice_n[init_matrix_random>=0.5]=1
        lattice_n[init_matrix_random<0.5]=-1
    return lattice_n

@njit(cache = True)
def geometry(dim_latt):
    '''Per ogni coordinata definisco il passo in avanti o indietro
       con le opportune condizioni al bordo
    '''
    npp = [i+1 for i in range(0,dim_latt)]
    nmm = [i-1 for i in range(0,dim_latt)]
    npp[dim_latt-1] = 0
    nmm[0] = dim_latt-1
    return (npp, nmm)

@njit(cache = True)
def metropolis(start, dim_latt, lattice_n, beta, extfield):
    '''
    Faccio aggiornamenti locali delle variabili di spin con metropolis.
    La variabile di spin di prova è sempre quella opposta a quella attuale.
    '''
    (npp, nmm) = geometry(dim_latt)
    for i in range(dim_latt**2):
        i=int(np.random.random()*(dim_latt))
        j=int(np.random.random()*(dim_latt))
        ip_ = npp[i]
        im_ = nmm[i]
        jp_ = npp[j]
        jm_ = nmm[j]
        force = lattice_n[i,jp_]+lattice_n[i,jm_]+lattice_n[ip_,j]+lattice_n[im_,j]
        force = beta*(force+extfield)
        phi = lattice_n[i,j]
        x_rand = np.random.random()
        if x_rand < np.exp(-2.0*phi*force):
            lattice_n[i,j] = -phi
    return lattice_n

@njit(cache = True)
def  magnetization(dim_latt, lattice_n):
    '''
    Calcolo della magnetizzazione media del reticolo
    '''
    xmagn = 0.0
    for i in range(0,dim_latt):
        for j in range(0,dim_latt):
            xmagn = xmagn + lattice_n[i,j]
    xmagn = xmagn/float(dim_latt**2)
    return xmagn

@njit(cache = True)
def energy(dim_latt, lattice_n, extfield):
    '''
    Calcolo dell'energia media del reticolo.
    Energia media = 0 per configurazione ordinata e campo esterno nullo.
    '''
    (npp, nmm) = geometry(dim_latt)
    nvol = dim_latt**2
    xene = 0.0
    for i in range(0,dim_latt):
        for j in range(0,dim_latt):
            ip_ = npp[i]
            im_ = nmm[i]
            jp_ = npp[j]
            jm_ = nmm[j]
            force = lattice_n[i,jp_]+lattice_n[i,jm_]+lattice_n[ip_,j]+lattice_n[im_,j]
            xene = xene -  0.5*force*lattice_n[i,j]
            xene = xene - extfield*lattice_n[i,j]
    xene = xene/float(nvol)
    return xene
