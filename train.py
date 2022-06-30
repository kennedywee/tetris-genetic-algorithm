import numpy
import genetic_alg as ga

f = open("record.txt", "w")

num_weights = 4
sol_per_pop = 10
num_generations = 4
num_parents_mating = 2
pieceLimit = 500
# seeds: if seed<0: random else random.seed = seed
seed = 1

# mutation
mutation_probability = 0.5 # meaning we do only half of the mutations

pop_size = (sol_per_pop, num_weights)
new_population = numpy.random.uniform(low=-3.0, high=3.0, size=pop_size)


print(new_population)
f.write(f"new population: \n {new_population} \n")
fitness = ga.cal_pop_fitness(new_population, pieceLimit, seed)
print(f"Original Generation fitnesses: \n {fitness}")
f.write(f"Original Generation fitnesses: \n {fitness} \n")

for generation in range(num_generations):
    print(f"Generation {generation + 1} fitnesses: ")
    f.write(f"Generation {generation + 1} fitnesses: ")
    parents = ga.selection(new_population, fitness, num_parents_mating)
    offspring_crossover = ga.crossover(parents, offspring_size=(pop_size[0] - parents.shape[0], num_weights))
    offspring_mutation = ga.mutation(offspring_crossover, mutation_probability)
    
    # survivor
    new_population[0:parents.shape[0],     :] = parents
    new_population[parents.shape[0]:, :] = offspring_mutation
    fitness = ga.cal_pop_fitness(new_population, pieceLimit, seed)

    print(fitness)
    f.write(f"{fitness}\n")
    best_match_idx = numpy.where(fitness == numpy.max(fitness))[0][0]
    print(f"current best {new_population[best_match_idx, :]}")
    f.write(f"current best {new_population[best_match_idx, :]}\n")

    print(f"New Population: \n {new_population}")

best_match_idx = numpy.where(fitness == numpy.max(fitness))[0][0]
print(f"new pop : {new_population}")

print("Best solution : ", new_population[best_match_idx, :])
print("Best solution fitness : ", fitness[best_match_idx])
f.write(f"Best solution: {new_population[best_match_idx, :]}\n")
f.write(f"best solution fitness: {fitness[best_match_idx]}\n")
f.close()
