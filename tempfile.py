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
