import supportfuncs as soup
import random


def fitness(population, distances, primes):
    gaps = list()
    for i in population:
        gaps.append(soup.calculate_route(i, distances, primes))
    return gaps


def reprodection(parants):
    return 0


def mutate(children):
    return 0


def build_new_population(population, mutated_children, gaps, new_gaps):
    return 0


def selection_wheel(choose_n, choose_from, distances, primes):  #returns indexes of chosen parents in population
    fitness_results = list()
    chance = list()
    chosen_ones = list()
    sum = 0
    for i in choose_from:
        fitness_results.append(soup.calculate_route(i, distances, primes))
        sum += fitness_results[len(fitness_results) - 1]
    temp = 0
    for i in fitness_results:
        temp += i / sum
        chance.append(temp)
    chance[len(chance) - 1] = 1 #in case when total sum would be 0.999 and random may run out of boundries
    for i in range(choose_n):
        while True:
            temp = random.random()
            index = 0
            while temp > chance[index]:
                index += 1
            if not (index in chosen_ones):
                chosen_ones.append(index)
                break

    return chosen_ones


def genetic_evolution(gen_num, pure_ids, distances, pop_num, per_num, primes):
    gen_count = 0
    population = soup.generate_start_points(pop_num, pure_ids, distances)
    gaps = fitness(population, distances, primes)
    while (gen_count != gen_num):
        parants = selection_wheel(per_num, population, distances, primes)
        children = reprodection(parants)
        mutated_children = mutate(children)
        new_gaps = fitness(mutated_children, distances, primes)
        population = build_new_population(population, mutated_children, gaps, new_gaps)
        gen_count += 1
    return population[0]