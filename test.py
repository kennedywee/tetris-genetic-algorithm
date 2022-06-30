import random
import copy

def mutation(solution):
    n = len(solution)
    position_1 = random.randint(0, n-1)
    position_2 = random.randint(0, n-1)

    result = swap(solution, position_1, position_2)
    return result

def swap(solution, position_1, position_2):
    result = solution.copy()
    elA = solution[position_1]
    elB = solution[position_2]
    result[position_1] = elB
    result[position_2] = elA
    return result

