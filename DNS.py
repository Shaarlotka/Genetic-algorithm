import copy


def expand_clusters(solution):
    return 0


def combine_clusters(solution):
    return 0


def change(solution, matrix, total_parts, mod):
    optimal = calculate_clusters(solution, matrix, total_parts)
    for i in range(len(solution[mod])):
        for j in  range(len(set(solution[mod]))):
            if (solution[mod][i] != j):
                new_solution = copy.deepcopy(solution)
                new_solution[mod][i] = j
                new_optimal = calculate_clusters(new_solution, matrix, total_parts)
                if (optimal < new_optimal):
                    solution = copy.deepcopy(new_solution)
                    optimal = new_optimal
    return solution

def change_machine_cluster(solution, matrix, total_parts):
    return change(solution, matrix, total_parts, 0)


def change_parts_cluster(solution, matrix, total_parts):
    return change(solution, matrix, total_parts, 1)


def greedy_algorithm_vns(clusters, matrix):
    columns_sum = {index : 0 for index in range(len(clusters[1]))}
    rows_sum = {index : 0 for index in range(len(clusters[0]))}
    for i in range(len(clusters[0])):
        for j in range(len(clusters[1])):
            rows_sum[i] += matrix[i][j]
            columns_sum[j] += matrix[i][j]
    rows_sum = [(v, k) for k, v in rows_sum.items()]
    columns_sum = [(v, k) for k, v in columns_sum.items()]
    columns_sum.sort(key=lambda value: value[0], reverse=True)
    rows_sum.sort(key=lambda value: value[0], reverse=True)
    for i in range(len(clusters[0]) // 2 + len(clusters[0]) %2):
        clusters[0][rows_sum[i][1]] = 1
    for i in range(len(clusters[1]) // 2 + len(clusters[1]) %2):
        clusters[1][columns_sum[i][1]] = 1

    return clusters


def calculate_clusters(clusters, matrix, total_parts):
    in_clusters = 0
    in_clusters_zero = 0
    for i in range(len(clusters[0])):
        for j in range(len(clusters[1])):
            if matrix[i][j] == 1 and clusters[0][i] == clusters[1][j]:
                in_clusters += 1
            elif matrix[i][j] == 0 and clusters[0][i] == clusters[1][j]:
                in_clusters_zero += 1
    return in_clusters / (total_parts + in_clusters_zero)


def convert(height, width):
    matrix = list()
    total_parts = 0
    for i in range(height):
        temp = [int(m) for m in input().split(' ')]
        matrix.append(list())
        index = 1
        for j in range(width):
            if index < len(temp) and j + 1 == temp[index]:
                matrix[i].append(1)
                index += 1
                total_parts += 1
            else:
                matrix[i].append(0)
    return matrix, total_parts


def GDNS(clusters, matrix, total_parts):
    shaking_structures = [expand_clusters, combine_clusters]
    neighdorhood_structure = [change_machine_cluster, change_parts_cluster]
    final_solution = greedy_algorithm_vns(clusters, matrix)
    k = 0
    while k != len(shaking_structures):
        solution = shaking_structures[k](final_solution)
        l = 0
        while l != len(neighdorhood_structure):
            new_solution = neighdorhood_structure[l](solution, matrix, total_parts)
            if (calculate_clusters(solution, matrix, total_parts) <
                calculate_clusters(new_solution, matrix, total_parts)):
                solution = copy.deepcopy(new_solution)
                l = 1
            else:
                l += 1
        if (calculate_clusters(solution, matrix, total_parts) >
            calculate_clusters(final_solution, matrix, total_parts)):
            final_solution = copy.deepcopy(solution)
            k = 1
        else:
            k += 1
    return final_solution


if __name__ == '__main__':
    quantity = input()
    quantity = [int(i) for i in quantity.split(' ')]
    matrix, total_parts = convert(quantity[0], quantity[1])
    for i in matrix:
        print(i)
    print("-------------------------------------------------")
    clusters = list()
    clusters.append([0 for i in range(quantity[0])])
    clusters.append([0 for i in range(quantity[1])])
    print(clusters) # 1st line - machines, 2nd line - parts
    clusters = GDNS(clusters, matrix, total_parts)
    print("-------------------------------------------------")
    print(clusters)
    print(calculate_clusters(clusters, matrix, total_parts))