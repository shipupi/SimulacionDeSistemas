import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

folder = "postprocessing/results/"

def dataframe_fp(statistics):
    list_n = statistics.n.unique()
    list_tabique = statistics.tabique.unique()

    for n in list_n:
        table = pd.DataFrame(columns=["N", "Tabique", "Promedio", "Desvío Estándar"])

        # Get statistics for different opening sizes
        for t in list_tabique:
            filtered = statistics.loc[
                (statistics["n"] == n) & (statistics["tabique"] == t)
            ]
            mean = filtered.tiempo.mean()
            std = filtered.tiempo.std()

            row = {'N':n,'Tabique':t,'Promedio':mean,'Desvío Estándar':std}
            table = table.append(row, ignore_index=True)

        # Save results table
        table.to_csv(folder + "dataframe_fp_{}.csv".format(n), index=False, header=True)

        # Plot fp vs. opening size and save plots to files
        means = np.array(table["Promedio"])
        stds = np.array(table["Desvío Estándar"])

        filepath = folder + "dataframe_fp_{}".format(n)

        plt.xlabel("Apertura del tabique [m]")
        plt.ylabel("Tiempo de corte de la simulación (fp ~ 0.5) [s]")
        plt.errorbar(list_tabique, means, stds, linestyle='None', solid_capstyle='projecting', capsize=5, marker='o')
        plt.savefig(filepath)
        plt.clf()

def calculate_energy(temperatures, n):
    energy = []
    for temp in temperatures:
        energy.append((1/2)*n*temp*temp)
    return np.array(energy)
        

def dataframe_gas_law(statistics):
    list_n = statistics.n.unique()
    list_tabique = statistics.tabique.unique()

    for n in list_n:
        t = list_tabique[0]

        filtered = statistics.loc[
                (statistics["n"] == n) & (statistics["tabique"] == t)]
        
        # gets temperatures and pressure from file
        temperatures = statistics.temperatura.unique()
        means = []
        stds = []

        energies = calculate_energy(temperatures, n) # x

        for temp in temperatures:
            new_filtered = filtered.loc[filtered["temperatura"] == temp]
            means.append(new_filtered.presion.mean()) # y 
            stds.append(new_filtered.presion.std())
        

        # least square method for linear regression
        slope,intercept = np.polyfit(energies, means, 1)

        filepath = folder + "dataframe_gas_law_{}".format(n)

        # plots and saves figure
        plt.xlabel("Energía del sistema [J]")
        plt.ylabel("Presión del sistema [N/m]")
        plt.errorbar(energies, means, stds, linestyle='None', solid_capstyle='projecting', capsize=5, marker='o')
        plt.plot(energies, slope*energies + intercept)
        plt.savefig(filepath, bbox_inches="tight", pad_inches=0.3)
        plt.clf()
