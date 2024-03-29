import math
import random
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Population


def generate_path(source, destination):
    path = []
    path.append(source)
    d = destination
    while destination not in path:
        x = xy[path[-1]][0]
        y = xy[path[-1]][1]
        if x < xy[d][0] and y < xy[d][1]:
            path.append(random.choice([val[(x+1, y)], val[(x, y+1)]]))
        elif x > xy[d][0] and y > xy[d][1]:
            path.append(random.choice([val[(x-1, y)], val[(x, y-1)]]))
        elif x > xy[d][0] and y < xy[d][1]:
            path.append(random.choice([val[(x-1, y)], val[(x, y+1)]]))
        elif x < xy[d][0] and y > xy[d][1]:
            path.append(random.choice([val[(x+1, y)], val[(x, y-1)]]))
        elif x == xy[d][0] and y < xy[d][1]:
            path.append(val[(x, y+1)])
        elif x == xy[d][0] and y > xy[d][1]:
            path.append(val[(x, y-1)])
        elif x < xy[d][0] and y == xy[d][1]:
            path.append(val[(x+1, y)])
        elif x > xy[d][0] and y == xy[d][1]:
            path.append(val[(x-1, y)])
    return path


def initialize():
    population = []
    for _ in range(num_of_chromosome):
        chromosome = []
        # making zipped list for source-destination pair
        l = list(zip(source, destination))
        for i in range(num_of_sourcedest):
            chromosome.append(generate_path(*l[i]))
        population.append(chromosome)
    return population


def show(population):
    for chromosome in population:
        print(chromosome)
        print('')

# ============================================================================ #
# ============================================================================ #


# Fitness Function

def FitnessValue(chromosome):
    frequency = [0]*(n*n)           # Frequency Array to find congestion
    for l in chromosome:
        for x in l:
            frequency[x-1] += 1
    return frequency


def FitnessFunction(population):
    fitness = {}
    for i in range(num_of_chromosome):
        l = FitnessValue(population[i])
        fitness[i+1] = sum([val-1 for val in l if val > 1])
    return fitness


def visualize(frequency):
    df = pd.DataFrame()
    y = []
    x = []
    for i in range(1, n+1):
        for j in range(n):
            y.append(i)
    for i in range(n):
        for j in range(1, n+1):
            x.append(j)
    df["Index"] = list(range(1, n*n+1))
    df["Data"] = frequency
    df["Y"] = y
    df["X"] = x

    data = np.asarray(df['Data']).reshape(n, n)
    index = np.asarray(df['Index']).reshape(n, n)

    result = df.pivot(index="Y", columns="X", values="Data")
    label = (np.asarray(['{0} \n'.format(ind, dat) for ind, dat in zip(
        index.flatten(), data.flatten())])).reshape(n, n)

    fig, ax = plt.subplots(figsize=(12, 7))
    title = "Congestion Visualization"
    plt.title(title, fontsize=18)
    ttl = ax.title
    ttl.set_position([0.5, 1.05])
    ax.set_xticks([])
    ax.set_yticks([])
    ax.axis("off")

    sns.heatmap(result, vmin=0, vmax=n, annot=label, fmt="",
                cmap="RdYlGn_r", linewidths=0.30, ax=ax)
    plt.show()


# ============================================================================ #
# ============================================================================ #


# Selection and Crossover

def tournament(population):
    # First Tournament
    k = random.randint(2, num_of_sourcedest)
    l = random.sample(population, k)
    Min = 1000
    for chromosome in l:
        if sum(FitnessValue(chromosome)) < Min:
            chrom1 = chromosome
            Min = sum(FitnessValue(chromosome))

    # Second Tournament
    k = random.randint(2, num_of_sourcedest)
    l = random.sample(population, k)
    Min = 1000
    for chromosome in l:
        if sum(FitnessValue(chromosome)) < Min:
            chrom2 = chromosome
            Min = sum(FitnessValue(chromosome))

    # print(chrom1, chrom2)
    return chrom1, chrom2


def crossover(chrome1, chrome2):                    # Applying Uniform Crossover
    offspring = []
    for i in range(num_of_sourcedest):
        offspring.append(random.choice([chrome1[i], chrome2[i]]))
    return offspring

# ============================================================================ #
# ============================================================================ #


# Mutation

def mutate(population, mutation_rate):
    k = math.ceil(mutation_rate*len(population))
    for _ in range(k):
        random_chromosome = random.randint(0, len(population)-1)
        chromosome = population[random_chromosome]
        random_gene = random.randint(0, len(chromosome)-1)
        gene = chromosome[random_gene]
        new_gene = generate_path(gene[0], gene[-1])
        population[random_chromosome][random_gene] = new_gene
        return population


# Main

if __name__ == "__main__":

    # Constant Parameters

    n = 6       # Mesh size(n x n)
    xy = {}     # Stores coordinate in xy form
    val = {}    # Stores value at coordinate

    for i in range(1, n+1):
        for j in range(1, n+1):
            xy[n*i-n+j] = (i-1, j-1)
            val[(i-1, j-1)] = n*i-n+j

    num_of_chromosome = 7        # number of chromosome
    num_of_sourcedest = 6        # number of source-destination pairs
    num_of_generation = 2500     # number of generation in our Genetic Algorithm
    source = [7, 8, 11, 12, 1, 1]
    destination = [21, 22, 27, 32, 6, 32]

    # Main Code starts here

    population = initialize()
    show(population)
    print()
    fitness_value = FitnessFunction(population)

    # for chromosome in population:
    #     visualize(FitnessValue(chromosome))

    progress = []
    for i in range(num_of_generation):
        chrom1, chrom2 = tournament(population)
        offspring = crossover(chrom1, chrom2)
        population.append(offspring)
        l = FitnessValue(offspring)
        fitness_value[num_of_chromosome+i +
                      1] = sum([val-1 for val in l if val > 1])
        print("Best Fitness value is {} till generation {}".format(
            1/(1+min(fitness_value.values())), i+1))
        progress.append(1/(1+min(fitness_value.values())))
        population = mutate(population, mutation_rate=0.5)
        if progress[-1] == 1:
            break
    key = min(fitness_value, key=fitness_value.get)
    print(population[key-1])
    plt.plot(progress)
    plt.ylabel('Fitness Value')
    plt.xlabel('Generation')
    plt.show()
    # print(fitness_value)
    # print(chrom1,chrom2,offspring,sep='\n')
    # for chromosome in population:
    #     visualize(FitnessValue(chromosome))
