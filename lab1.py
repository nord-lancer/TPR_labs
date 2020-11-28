import csv
from prettytable import PrettyTable

data = list()


with open('lab_1_data.csv', newline='') as csv_file:
    reader = csv.reader(csv_file, delimiter=',', skipinitialspace=True)
    first = True
    for line in reader:
        if first:
            probability = list(map(float, line))
            first = False
            continue
        data.append(list(map(float, line)))


def wald():
    criteria = list()
    for row in data:
        criteria.append(min(row))
    return criteria, criteria.index(max(criteria))


def bayes():
    criteria = list()
    for row in data:
        criteria.append(sum(list(map(lambda value, prob: value*prob, row, probability))))
    return criteria, criteria.index(max(criteria))


def hurwitz(opt_coefficient):
    criteria = list()
    for row in data:
        criteria.append((min(row) + max(row)) * opt_coefficient)
    return criteria, criteria.index(max(criteria))


def laplace():
    prob = 1.0 / len(data[0])
    criteria = list()
    for row in data:
        criteria.append(sum([r * prob for r in row]))
    return criteria, criteria.index(max(criteria))


def output():
    table = PrettyTable(['Strategy', 'S1', 'S2', 'S3', 'Wald', 'Bayes', 'Hurwitz', 'Laplace'])
    wald_full, wald_res = (wald())
    bayes_full, bayes_res = (bayes())
    hurwitz_full, hurwitz_res = (hurwitz(0.42))
    laplace_full, laplace_res = (laplace())
    for i in range(len(data[0])):
        row = [f'A{i}'] + data[i]
        row += [f'{wald_full[i]:.2f}', f'{bayes_full[i]:.2f}', f'{hurwitz_full[i]:.2f}', f'{laplace_full[i]:.2f}']
        table.add_row(row)
    table.add_row(['Pj']+probability+[f'A{wald_res+1}', f'A{bayes_res+1}', f'A{hurwitz_res+1}', f'A{laplace_res+1}'])
    return table


print(output())
