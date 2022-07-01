import numpy
K_fitness = []
fitness = [100, 200, 300, 400, 500, 600, 700, 800, 900, 1000]

rand_index = numpy.random.randint(0, len(fitness), size = 3)

print(f"rand_index: {rand_index}")




K_fitness = [fitness[idx] for idx in rand_index]
print(f"K_fitness: {K_fitness}")