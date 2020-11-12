import math
import numpy as np
import matplotlib.pyplot as plt

from enum import Enum
from glob import glob

class DynamicInputState(Enum):
    START = 1
    COMMENT = 2
    PARTICLE = 3

def distance(x1, y1, x2, y2):
    return math.sqrt((x2-x1) ** 2 + (y2-y1) ** 2)

def module(x, y):
    return math.sqrt(x*x + y*y)

def get_metrics(dynamic_input_path):
    state = DynamicInputState.START # initial state

    total_time = 0 # we need to know how long the simulation was
    first_iteration = True
    first_particle = True

    prev_x = 0 # for distance calculation
    prev_y = 0 # for distance calculation

    total_distance = 0

    v_modules = [] # for mean velocity calculation

    xs = []
    ys = []

    with open(dynamic_input_path) as in_f:
        for line in in_f:
            if state == DynamicInputState.START:
                remaining = int(line)
                state = DynamicInputState.COMMENT
            elif state == DynamicInputState.COMMENT:
                total_time = float(line)
                if remaining == 0:
                    state = DynamicInputState.START
                else:
                    state = DynamicInputState.PARTICLE
            elif state == DynamicInputState.PARTICLE:
                if first_particle:
                    first_particle = False
                    elements = line.split('\t')
                    if not first_iteration: # I want to calculate distance from previous point
                        curr_x = float(elements[0])
                        curr_y = float(elements[1])
                        total_distance += distance(prev_x, prev_y, curr_x, curr_y) # adds this distance to total distance
                    prev_x = float(elements[0])
                    prev_y = float(elements[1])
                    xs.append(prev_x)
                    ys.append(prev_y)
                    v_modules.append(module(float(elements[2]), float(elements[3]))) # velocity module
                remaining -= 1
                if remaining == 0:
                    state = DynamicInputState.START
                    first_iteration = False
                    first_particle = True

    # returns total simulation time, total distance and mean velocity
    return total_time, total_distance, np.array(v_modules).sum()/total_time, xs, ys

values = [0.1, 0.5, 1.0, 1.5, 2.0, 2.5, 3, 3.5, 4]
prefix = [] # complete here with file prefixes
for val in values:
    prefix.append(f"sim_{val}")

def plot_several_runs(input_fodler):
    times_means = []
    times_stds = []

    distances_means = []
    distances_stds = []

    mean_velocities_means = []
    mean_velocities_stds = []

    for pref in prefix:
        pref_times = []
        pref_distances = []
        pref_mean_velocities = []
        files = np.sort(glob(f"{input_fodler}/{pref}*"))
        for file in files:
            total_time, total_distance, mean_velocity, _, _ = get_metrics(file)
            if total_time < 0:
                print(f"{file} {total_time}")
            if total_distance == 0:
                print(f"{file} {total_distance}")
            pref_times.append(total_time)
            pref_distances.append(total_distance)
            pref_mean_velocities.append(mean_velocity)

        # Once I finished with my prefix

        times_means.append(np.array(pref_times).mean())
        times_stds.append(np.array(pref_times).std())

        distances_means.append(np.array(pref_distances).mean())
        distances_stds.append(np.array(pref_distances).std())

        mean_velocities_means.append(np.array(pref_mean_velocities).mean())
        mean_velocities_stds.append(np.array(pref_mean_velocities).std())

    for i in range(len(values)):
        values[i] = values[i] + 1 # 1 is radius of pedestrian

    # print(len(values))
    #
    # print(len(times_means))
    # print(len(times_stds))
    #
    # print(len(distances_means))
    # print(len(distances_stds))
    #
    # print(len(mean_velocities_means))
    # print(len(mean_velocities_stds))

    plt.clf()
    ax = plt.gca()
    ax.set_yscale('log')
    plt.errorbar(values, times_means, times_stds, color='blue', linestyle='None', solid_capstyle='projecting', capsize=5, marker='o')
    plt.xlabel("Distancia psicofísica desde CM [m]")
    plt.ylabel("Tiempo de Tránsito [s]")
    plt.savefig("/home/marina/SimulacionDeSistemas/tp5/results/tiempos.png")

    plt.clf()
    ax = plt.gca()
    ax.set_yscale('log')
    plt.errorbar(values, distances_means, distances_stds, color='blue', linestyle='None', solid_capstyle='projecting', capsize=5, marker='o')
    plt.xlabel("Distancia psicofísica desde CM [m]")
    plt.ylabel("Longitud del recorrido [m]")
    plt.savefig("/home/marina/SimulacionDeSistemas/tp5/results/longitudes.png")

    plt.clf()
    plt.errorbar(values, mean_velocities_means, mean_velocities_stds, color='blue', linestyle='None', solid_capstyle='projecting', capsize=5, marker='o')
    plt.xlabel("Distancia psicofísica desde CM [m]")
    plt.ylabel("Velocidad media [m/s]")
    plt.savefig("/home/marina/SimulacionDeSistemas/tp5/results/velocidades.png")


def run_file_metrics():
    total_time, total_distance, mean_velocity, xs, ys = get_metrics("/home/marina/SimulacionDeSistemas/tp5/output/unnamed_dynamic.xyz")

    print("Total simulation time " + str(total_time))
    print("Total distance " + str(total_distance))
    print("Mean velocity " + str(mean_velocity))

    # plots trajectory
    plt.clf()
    plt.plot(xs, ys, color='blue')
    plt.xlabel("x [m]")
    plt.ylabel("y [m]")
    plt.savefig("/home/marina/SimulacionDeSistemas/tp5/results/trajectory.png")



plot_several_runs("/home/marina/SimulacionDeSistemas/tp5/output")
