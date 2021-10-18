import numpy as np
from pathlib import Path
import module.func as boot

pathlist= Path("results/lattice_dim_10").glob("**/*.txt")

nomefile=[]
sigma_measures=[]
observable=[]

for path in pathlist:
    nomefile=path.name
    if nomefile[0]=='m':
      beta=int(nomefile[21:23])/100
    if nomefile[0]=='e':
      beta=int(nomefile[16:18])/100
    observable=np.loadtxt(path)
    sigma_measures.append(boot.bootstrap_binning(observable, 2, beta, 10))
    print('siamo al file n° ',path, 'e ne mancano ', len(pathlist)-path)

print(sigma_measures)

# pathlist= Path("IsingModelMC/results/lattice_dim_10").glob("**/*.txt")

# '''Qui fa il bootstrap per tutti i file nella directory selezionata'''
# sigma_measures=[]
# for path in pathlist:
#     array_osservabile=np.loadtxt(path)
#     sigma_measures.append(bootstrap_binning(array_osservabile, 1))

# print(sigma_measures)
