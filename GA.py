import supportfuncs as soup
import random


def fitness(population, distances, primes):
    gaps = list()
    for i in population:
        gaps.append(soup.calculate_route(i, distances, primes))
    return gaps


def child_production(parent_1, parent_2):
    child = list()
    path_len = len(parent_1)
    child.append(parent_1[0])
    index1 = random.randint(1, path_len)
    index2 = random.randint(1, path_len)
    first = min(index1, index2)
    last = max(index1, index2)
    tmp_1 = [item for item in parent_1[first:last]]
    tmp_2 = [item for item in parent_2 if item not in tmp_1 and item not in child]
    tmp_1_count = 0
    tmp_2_count = 0
    for k in range(1, path_len):
        if (k in range(first, last)):
            child.append(tmp_1[tmp_1_count])
            tmp_1_count += 1
        else:
            child.append(tmp_2[tmp_2_count])
            tmp_2_count += 1
    return child


def reprodection(parents, par_num):
    children = list()
    for i in range(par_num - 1):
        for j in range(i + 1, par_num):
            children.append(child_production(parents[i], parents[j]))
    return children


def mutate(children):
    child_len = len(children[0])
    mutation_volume = int(child_len / 100 * 5 + 0.5)
    for i in range (len(children)):
        index = random.randint(1, child_len - mutation_volume)
        tmp = children[i][index:index+mutation_volume]
        random.shuffle(tmp)
        children[i][index:index+mutation_volume] = tmp
    return children


def sort(population, gaps):
    pop = [y for x,y in sorted(zip(gaps, population))]
    gaps = sorted(gaps)
    return pop, gaps


def build_new_population(population, mutated_children, gaps, new_gaps):
    pop = list()
    gap = list()
    population, gaps = sort(population, gaps)
    mutated_children, new_gaps = sort(mutated_children, new_gaps)
    count = 0
    new_count = 0
    for i in range(len(population)):
        if (gaps[count] < new_gaps[new_count]):
            pop.append(population[count])
            gap.append(gaps[count])
            count += 1
        else:
            pop.append(mutated_children[new_count])
            gap.append(new_gaps[new_count])
            new_count += 1
    return pop, gap


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


def selection(par_num, population, distances, primes):
    parents = list()
    indexes = selection_wheel(par_num, population, distances, primes)
    for i in  indexes:
        parents.append(population[i])
    return parents


def genetic_evolution(gen_num, pure_ids, distances, pop_num, par_num, primes):
    gen_count = 0
    population = soup.generate_start_points(pop_num, pure_ids, distances)
    gaps = fitness(population, distances, primes)
    while (gen_count != gen_num):
        parents = selection(par_num, population, distances, primes)
        children = reprodection(parents, par_num)
        mutated_children = mutate(children)
        new_gaps = fitness(mutated_children, distances, primes)
        population, gaps = build_new_population(population, mutated_children, gaps, new_gaps)
        gen_count += 1
    return population[0]
