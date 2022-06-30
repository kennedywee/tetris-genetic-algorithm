from turtle import position
import numpy
import tetris
import copy

# calculate the population fitness
def cal_pop_fitness(pop, pieceLimit, seed):
    fitness = []
    for indv in range(len(pop)):
        fitness.append(tetris.TetrisApp(True, seed).run(pop[indv], pieceLimit))
    return fitness

# tournament selection
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
    crossover_point = numpy.uint8(offspring_size[1] / 2)
    for k in range(offspring_size[0]):
        parent1_idx = k % parents.shape[0]
        parent2_idx = (k + 1) % parents.shape[0]
        offspring[k, 0:crossover_point] = parents[parent1_idx, 0:crossover_point]
        offspring[k, crossover_point:] = parents[parent2_idx, crossover_point:]
    print(f"offspring: {offspring}")
    return offspring

# swap mutation
def mutation(offspring_crossover, mutation_probability):

    index_range = round(offspring_crossover.shape[1] * mutation_probability)

    print(f"offspring_crossover: {offspring_crossover.shape[1]}")
    print("index_range: ", index_range)
    
    for idx in range(offspring_crossover.shape[0]):
        mutation_gene1 = numpy.random.randint(low=0, high=offspring_crossover.shape[1]/2, size=1)[0]
        mutation_gene2 = mutation_gene1 + int(offspring_crossover.shape[1]/2)
        temp = offspring_crossover[idx, mutation_gene1]
        offspring_crossover[idx, mutation_gene1] = offspring_crossover[idx, mutation_gene2]
        offspring_crossover[idx, mutation_gene2] = temp
    print(f"offspring_crossover: {offspring_crossover}")
    return offspring_crossover

