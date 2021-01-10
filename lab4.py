import csv
import os
from decimal import Decimal
from prettytable import PrettyTable

expert_data = list()

data_path = 'lab4_data'
parameter_names = ['Зручність для пасажира', 'Зручність для пілотів',
                   'Економність', 'Безпека']


for root, dirs, files in os.walk(data_path, topdown=False):
    for name in files:
        with open(f'{os.path.join(root, name)}', newline='') as csv_file:
            reader = csv.reader(csv_file, delimiter=',', skipinitialspace=True)
            data = list()
            for line in reader:
                data.append(line)
            expert_data.append(data)


def get_sum_list(expert_range):
    param_sum = list()
    for i in expert_range:
        weight = Decimal(i.pop(0))
        param_sum.append([weight * Decimal(x) for x in i])
    return add_params_sums(param_sum)


def add_params_sums(param_sum: list):
    sum = param_sum.pop(0)
    for i in param_sum:
        for j in range(len(i)):
            sum[j] += i[j]
    return sum


all_sums = list()


def get_expert_table(exp_data):
    table = PrettyTable(['№', 'Параметр', 'Вага', 'А', 'Б', 'В'])
    for index in range(len(exp_data)):
        row = [index, parameter_names[index]]
        for i in exp_data[index]:
            row.append(i)
        table.add_row(row)
    sums = get_sum_list(exp_data)
    all_sums.append(sums)
    last_row = ['Сума', '', '']
    for s in sums:
        last_row.append(s)
    table.add_row(last_row)
    return table


def get_last_table(data):
    table = PrettyTable(["Об'єкт", 'Сума рангів по зростанню'])
    column_1 = ['А', 'Б', 'В']
    column_2 = add_params_sums(data)
    rows = sorted(list((zip(column_1, column_2))), key=lambda x: x[1])
    for i in rows:
        table.add_row([x for x in i])
    return table


counter = 1
for d in expert_data:
    print(f"Експерт №{counter}")
    print(get_expert_table(d))
    counter += 1

print('')
print(get_last_table(all_sums))
