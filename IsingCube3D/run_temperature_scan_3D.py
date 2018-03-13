import numpy as np
from Wolff_Algorithm.Wolff import *
import matplotlib.pyplot as plt
from variable_calculations.order_measures import *
from metropolis_hastings.metropolis import *
from fitting_module.critical_exponents import fit_power_law
import pickle

N = (20,20,20);
lattice_size_name = str(N[0])+'x'+str(N[1])+'x'+str(N[2]);


mag_v_temp =list();
beta_scan = np.linspace(0.1, 0.21, 10);
beta_near_crit = np.linspace(0.22, 0.3, 50);
beta_scan = np.append(beta_scan, beta_near_crit);
beta_scan = np.append(beta_scan, np.linspace(0.3, 0.5, 10));

# we will run the simulation ONCE and save the lattice history and then simply analyze the lattice history
# so we don't have to continuously run the simulation again and again;

simulation_data = dict(); #keys will be betas

## ===========LATTICE INITIALIZATION ============##
# we claim that it is better to do the initialization once and then run the simulation
# as we run to the next temperature, the previous lattice will actually be not too far from thesteady state lattice of the next
Lattice = 2 * np.random.randint(0, 2, N) - 1;

## ===============================================

for K in beta_scan:
    lattice_history = list();
    epochs = 1000;
    print(K)
    p = 1 - np.exp(-2 * K);
    magn = list();
    if(K> 0.2): #as temperature get higher, the lattice will equilibrate faster
        epochs = 400;
    if(K> 0.3):
        epochs = 100;

    ## simulation_runs
    if(K > 0.3):
        print('metropolis')
        epochs = 100;
        #run a metropolis hastings simulation
        for t in range(epochs):
            Lattice = metropolis_sim_epoch(Lattice, K, nearest_neighbors = 1);
            magn.append(magnetization(Lattice));
            if(t%100 == 0):
                print('epoch: '+str(t))

            lattice_history.append(Lattice);

    else:
        for t in range(epochs):
            Lattice = run_Wolff_epoch(Lattice, N, p);
            if(t%400 == 0):
                print(t);
                # plt.imshow(Lattice)
                # plt.show();
            if(t > 100):
                magn.append(magnetization(Lattice));

            lattice_history.append(Lattice);

    simulation_data[K] = lattice_history;

    M = np.mean(magn);
    mag_v_temp.append(M);

plt.figure();
plt.plot(1/beta_scan, mag_v_temp)
plt.show()

T_c = 1/4.511;
## fit power laws
critical_mag = fit_power_law(1/beta_scan, mag_v_temp, T_c);
print(critical_mag);

## ============= SAVE LATTICE HISTORY DATA =====================##
pickle.dump([simulation_data, epochs, beta_scan, N], open(lattice_size_name+'_Ising_3D_Lattice_Temp_Scan_large.p', 'wb'));
## ==============================================================


# vars = ['m per site', 'E per site', 'spin_corr', 'chi', 'heat_capacity'];
# for i in range(len(vars)):
#     plt.figure();
#     plt.plot(1/beta_scan, avg_data[:,i]);
#     plt.title(vars[i])
#     plt.xlabel('temperature')
#     plt.ylabel(vars[i])
#     plt.savefig(vars[i]+'_vs_T.png');
#
# plt.show()