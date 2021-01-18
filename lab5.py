import csv
from prettytable import PrettyTable
import numpy as np
import pulp


solver = pulp.PULP_CBC_CMD(msg=False)
data = list()

with open('lab_5_data.csv', newline='') as csv_file:
    reader = csv.reader(csv_file, delimiter=',', skipinitialspace=True)
    for line in reader:
        data.append(list(map(float, line)))

game = np.array(data)


def solve_game_first_player(game: np.array):
    x1 = pulp.LpVariable("x1", lowBound=0)
    x2 = pulp.LpVariable("x2", lowBound=0)
    x3 = pulp.LpVariable("x3", lowBound=0)
    x4 = pulp.LpVariable("x4", lowBound=0)
    x5 = pulp.LpVariable("x5", lowBound=0)
    prob = pulp.LpProblem('p', pulp.LpMinimize)
    prob += x1 + x2 + x3 + x4 + x5
    prob += game[0][0] * x1 + game[1][0] * x2 + game[2][0] * x3 + game[3][0] * x4 + game[4][0] * x5 >= 1
    prob += game[0][1] * x1 + game[1][1] * x2 + game[2][1] * x3 + game[3][1] * x4 + game[4][1] * x5 >= 1
    prob += game[0][2] * x1 + game[1][2] * x2 + game[2][2] * x3 + game[3][2] * x4 + game[4][2] * x5 >= 1
    prob += game[0][3] * x1 + game[1][3] * x2 + game[2][3] * x3 + game[3][3] * x4 + game[4][3] * x5 >= 1
    prob += game[0][4] * x1 + game[1][4] * x2 + game[2][4] * x3 + game[3][4] * x4 + game[4][4] * x5 >= 1
    prob += x1 >= 0
    prob += x2 >= 0
    prob += x3 >= 0
    prob += x4 >= 0
    prob += x5 >= 0
    status = prob.solve(solver)
    p = list()
    u = 1 / pulp.value(prob.objective)
    for variable in prob.variables():
        print(variable, "=", variable.varValue)
        p.append(variable.varValue*u)
    print("Рішення гри (сідлова точка):")
    print(pulp.value(prob.objective))
    print("Першому гравцю треба обирати свої стратегії із наступними імовірностями для максимального прибутку:")
    output_strategy(p, 1)


def solve_game_second_player(game: np.array):
    x1 = pulp.LpVariable("x1", lowBound=0)
    x2 = pulp.LpVariable("x2", lowBound=0)
    x3 = pulp.LpVariable("x3", lowBound=0)
    x4 = pulp.LpVariable("x4", lowBound=0)
    x5 = pulp.LpVariable("x5", lowBound=0)
    prob = pulp.LpProblem('p', pulp.LpMaximize)
    prob += x1 + x2 + x3 + x4 + x5
    prob += game[0][0] * x1 + game[0][1] * x2 + game[0][2] * x3 + game[0][3] * x4 + game[0][4] * x5 <= 1
    prob += game[1][0] * x1 + game[1][1] * x2 + game[1][2] * x3 + game[1][3] * x4 + game[1][4] * x5 <= 1
    prob += game[2][0] * x1 + game[2][1] * x2 + game[2][2] * x3 + game[2][3] * x4 + game[2][4] * x5 <= 1
    prob += game[3][0] * x1 + game[3][1] * x2 + game[3][2] * x3 + game[3][3] * x4 + game[3][4] * x5 <= 1
    prob += game[4][0] * x1 + game[4][1] * x2 + game[4][2] * x3 + game[4][3] * x4 + game[4][4] * x5 <= 1
    prob += x1 >= 0
    prob += x2 >= 0
    prob += x3 >= 0
    prob += x4 >= 0
    prob += x5 >= 0
    status = prob.solve(solver)
    p = list()
    u = 1 / pulp.value(prob.objective)
    for variable in prob.variables():
        print(variable, "=", variable.varValue)
        p.append(variable.varValue*u)
    print("Рішення гри (сідлова точка):")
    print(pulp.value(prob.objective))
    print("Другому гравцю треба обирати свої стратегії із наступними імовірностями для мінімального програшу:")
    output_strategy(p, 2)


def compare_arrays(array1: np.array, array2: np.array):
    if (array1>array2).all():
         # array1 is bigger element by element
        return 1
    elif (array2>array1).all():
        # array2 is bigger element by element
        return 2
    elif (array2 == array1).all():
        # arrays are equal element by element
        return 0
    else:
        # array are different element by element
        return -1


def simplify_cols(data: np.array):
    copy_data = data.copy()
    change_made = False
    row_len = len(copy_data.transpose()[0])
    if row_len == 1:
        return change_made, copy_data
    for i in range(row_len-1):
        row = copy_data[i]
        for j in range(i+1, row_len):
            next_row = copy_data[j]
            comparison = compare_arrays(row, next_row)
            if comparison == 1:
                copy_data = np.delete(copy_data, i, 0)
                change_made = True
                return change_made, copy_data
            if comparison == 2:
                copy_data = np.delete(copy_data, j, 0)
                change_made = True
                return change_made, copy_data
    return change_made, copy_data


def simplify_rows(data: np.array):
    copy_data = data.copy()
    change_made = False
    row_len = len(copy_data.transpose()[0])
    if row_len == 1:
        return change_made, copy_data
    for i in range(row_len-1):
        row = copy_data[i]
        for j in range(i+1, row_len):
            next_row = copy_data[j]
            comparison = compare_arrays(row, next_row)
            if comparison == 1:
                copy_data = np.delete(copy_data, j, 0)
                change_made = True
                return change_made, copy_data
            if comparison == 2:
                copy_data = np.delete(copy_data, i, 0)
                change_made = True
                return change_made, copy_data
    return change_made, copy_data


def simplify_game(data: np.array):
    changed_game: np.array = data.copy()
    while True:
        change_row, changed_game = simplify_rows(changed_game)
        change_col, changed_game = simplify_cols(changed_game.transpose())
        if change_row is False and change_col is False:
            break
    return changed_game


def equilibrium_point(data: np.array):
    first_player_min = list()
    second_player_max = list()
    for i in data:
        first_player_min.append(min(i))
    for i in data.transpose():
        second_player_max.append(max(i))
    maxmin = (max(first_player_min), first_player_min.index(max(first_player_min)))
    minmax = (min(second_player_max), second_player_max.index(min(second_player_max)))
    if maxmin[0] == minmax[0]:
        print('Гра має вирішення у чистих стратегіях')
        print(f'Позиція сідлової точки: ({maxmin[1]+1},{minmax[1]+1})')
        return 0
    else:
        print('Гра не має вирішення у чистих стратегіях')
        return 1


def output_game(data: np.array):
    row_len = len(data[0])
    col_len = len(data.transpose()[0])
    top_row = ['Гравець 1/Гравець 2']
    first_column = list()
    for i in range(row_len):
        top_row.append(f'{i+1}')
    for i in range(col_len):
        first_column.append(f'{i+1}')
    table = PrettyTable(top_row)
    for i in first_column:
        row = [x for x in data[int(i)-1]]
        row.insert(0, i)
        table.add_row(row)
    return table


def output_strategy(data: list, player_number):
    row_len = len(data)
    top_row = ['Гравець']
    for i in range(row_len):
        top_row.append(f'Стратегія {i + 1}')
    table = PrettyTable(top_row)
    data.insert(0, player_number)
    table.add_row(data)
    print(table)


print("Вхідні дані")
print(output_game(game))
print("Спрощена гра:")
print(output_game(simplify_game(game)))
print("Знайдемо сідлову точку")
if equilibrium_point(game) == 1:
    print('\nЗнайдемо рішення в оптимальних змішаних стратегіях')
    solve_game_first_player(game)
    print()
    solve_game_second_player(game)

