import numpy
import genetic_alg as ga
import matplotlib.pyplot as plt 

f = open("record.txt", "w")

num_weights = 4
sol_per_pop = 20
num_generations = 10
num_parents_mating = 4
pieceLimit = 300
# seeds: if seed<0: random else random.seed = seed
seed = 1


pop_size = (sol_per_pop, num_weights)
new_population = numpy.random.uniform(low=-1.0, high=1.0, size=pop_size)


print(f"Initial Population: \n {new_population}")
f.write(f"Initial population: \n {new_population} \n")
fitness = ga.cal_pop_fitness(new_population, pieceLimit, seed)
print(f"Original Generation fitnesses: \n {fitness}")
f.write(f"Original Generation fitnesses: \n {fitness} \n")

for generation in range(num_generations):
    print(f"Generation {generation + 1} fitnesses: ")
    f.write(f"Generation {generation + 1} fitnesses: ")
    #parents = ga.selection(new_population, fitness, num_parents_mating)
    parents = ga.stochastic_selection(new_population, fitness, num_parents_mating)
    offspring_crossover = ga.two_points_crossover(parents, offspring_size=(pop_size[0] - parents.shape[0], num_weights))
    offspring_mutation = ga.mutation(offspring_crossover)
    
    # survivor
    new_population[0:parents.shape[0],     :] = parents
    new_population[parents.shape[0]:, :] = offspring_mutation
    fitness = ga.cal_pop_fitness(new_population, pieceLimit, seed)

    print(fitness)
    f.write(f"{fitness}\n")
    best_match_idx = numpy.where(fitness == numpy.max(fitness))[0][0]
    print(f"Current best: {new_population[best_match_idx, :]}")
    print(f"Current best fitness: {fitness[best_match_idx]}")
    f.write(f"Current best {new_population[best_match_idx, :]}\n")
 
    print(f"New Population: \n {new_population}")

best_match_idx = numpy.where(fitness == numpy.max(fitness))[0][0]
print(f"Best Population : {new_population}")

print("Best solution : ", new_population[best_match_idx, :])
print("Best solution fitness : ", fitness[best_match_idx])
f.write(f"Best solution: {new_population[best_match_idx, :]}\n")
f.write(f"Best solution fitness: {fitness[best_match_idx]}\n")
f.close()
