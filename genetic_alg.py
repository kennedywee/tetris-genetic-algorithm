from random import random
from re import I
from turtle import position
import numpy
import tetris
import copy

K_tournament = 3
crossover_probability = None

# calculate the population fitness
def cal_pop_fitness(pop, pieceLimit, seed):
    fitness = []
    for indv in range(len(pop)):
        fitness.append(tetris.TetrisApp(True, seed).run(pop[indv], pieceLimit))
    return fitness

# Generic selection
def selection(population, fitness, num_parents):
    # Selecting the best individuals in the current generation as parents for producing the offspring of the next generation.
    parents = numpy.empty((num_parents, population.shape[1]))
    for parent_num in range(num_parents):
        max_fitness_idx = numpy.where(fitness == numpy.max(fitness))
        max_fitness_idx = max_fitness_idx[0][0]
        parents[parent_num, :] = population[max_fitness_idx, :]
        fitness[max_fitness_idx] = -99999999999 # To avoid selecting the same parent again, set the current fitness to lowest.
    #print(f"parents: {parents}")
    return parents

# single point crossover
def crossover(parents, offspring_size):
    # The point at which crossover takes place between two parents. Usually, it is at the center.
    offspring = numpy.empty(offspring_size)
    #print(f"offspring_size: {offspring_size}")
    crossover_point = numpy.uint8(offspring_size[1] / 2)
    for k in range(offspring_size[0]):
        parent1_idx = k % parents.shape[0]
        parent2_idx = (k + 1) % parents.shape[0]
        offspring[k, 0:crossover_point] = parents[parent1_idx, 0:crossover_point]
        offspring[k, crossover_point:] = parents[parent2_idx, crossover_point:]
    #print(f"offspring: \n {offspring}")
    return offspring

def two_points_crossover(parents, offspring_size):
    offspring = numpy.empty(offspring_size)

    for k in range(offspring_size[0]):
        if parents.shape[1] == 1:
            crossover_point1 = 0
        else:
            crossover_point1 = numpy.random.randint(low=0, high=numpy.ceil(parents.shape[1]/2), size=1)[0]
        
        crossover_point2 = crossover_point1 + int(parents.shape[1]/2)

        if not (crossover_probability is None):
            probs = numpy.random.random(size=parents.shape[0])
            indices = numpy.where(probs < crossover_probability)[0]

            if len(indices) == 0:
                offspring[k, :] = parents[k % parents.shape[0], :]
                continue
            elif len(indices) == 1:
                parent1_idx = indices[0]
                parent2_idx = parent1_idx
            else:
                indices = random.sample(set(indices), 2)
                parent1_idx = indices[0]
                parent2_idx = indices[1]
        else:
            parent1_idx = k % parents.shape[0]
            parent2_idx = (k + 1) % parents.shape[0]
        
        offspring[k, 0:crossover_point1] = parents[parent1_idx, 0:crossover_point1]
        offspring[k, crossover_point2:] = parents[parent1_idx, crossover_point2:]
        offspring[k, crossover_point1:crossover_point2] = parents[parent2_idx, crossover_point1:crossover_point2]

    return offspring


# swap mutation
def swap_mutation(offspring_crossover):
    
    mutation_rate = numpy.uint8(offspring_crossover.shape[0]/2)
    
    for idx in range(mutation_rate): # Mutation only half of the offsprings
        mutation_gene1 = numpy.random.randint(low=0, high=offspring_crossover.shape[1]/2, size=1)[0]
        mutation_gene2 = mutation_gene1 + int(offspring_crossover.shape[1]/2)
        temp = offspring_crossover[idx, mutation_gene1]
        offspring_crossover[idx, mutation_gene1] = offspring_crossover[idx, mutation_gene2]
        offspring_crossover[idx, mutation_gene2] = temp
    #print(f"offspring_crossover: \n {offspring_crossover}")
    return offspring_crossover

def mutation(offspring_crossover):
    mutation_point = 2
    for idx in range(offspring_crossover.shape[0]):
        random_value = numpy.random.uniform(-1.0, 1.0, 1)
        offspring_crossover[idx, mutation_point] = offspring_crossover[idx, mutation_point] + random_value
    return offspring_crossover

def tournament_selection(population, fitness, num_parents):
    parents = numpy.empty((num_parents, population.shape[1]))
        
    for parent_num in range(num_parents):
        rand_indices = numpy.random.randint(low=0.0, high=len(fitness), size = K_tournament)
        K_fitnesses = [fitness[idx] for idx in rand_indices]
        selected_parent_idx = numpy.where(K_fitnesses == numpy.max(K_fitnesses))[0][0]
        parents[parent_num, :] = population[selected_parent_idx, :]
    return parents


def stochastic_selection(population, fitness, num_parents):
    
    fitness_sum = numpy.sum(fitness)
    probs = fitness / fitness_sum
    probs_start = numpy.zeros(probs.shape, dtype=numpy.float)
    probs_end = numpy.zeros(probs.shape, dtype=numpy.float)

    curr = 0

    for _ in range(probs.shape[0]):
        min_probs_idx = numpy.where(probs == numpy.min(probs))[0][0]
        probs_start[min_probs_idx] = curr
        curr += probs[min_probs_idx]
        probs_end[min_probs_idx] = curr
        probs[min_probs_idx] = 99999999999


    pointers_distance = 1.0 / num_parents
    first_pointer = numpy.random.uniform(low=0.0, high=pointers_distance, size=1)

    parents = numpy.empty((num_parents, population.shape[1]))

    for parent_num in range(num_parents):
        rand_pointer = first_pointer + parent_num * pointers_distance

        for idx in range(probs.shape[0]):
            if (rand_pointer >=probs_start[idx] and rand_pointer < probs_end[idx]):
                parents[parent_num, :] = population[idx, :]
                break

    return parents

def sort_by_fitness(population, fitness):

    sorted_idx = numpy.argsort(fitness) # arrage the fitness in ascending order
    sorted_population = population[sorted_idx, :]
    sorted_fitness = [fitness[x] for x in sorted_idx]
    return sorted_population
