import csv
from prettytable import PrettyTable

data = list()
years = 5
years_c_var = 4

with open('lab_2_data.csv', newline='') as csv_file:
    reader = csv.reader(csv_file, delimiter=',', skipinitialspace=True)
    for line in reader:
        data.append(line)


def get_data_variables(var_data: list):
    M, D1, P1, D2, P2 = float(var_data[0]), float(var_data[1]), float(var_data[2]), float(var_data[3]), \
                        float(var_data[4])
    return M, D1, P1, D2, P2


def calculate_expected_revenue(yearly_revenue, years, expenses):
    return years * yearly_revenue - expenses


def calculate_emv(expected_revenue, probability):
    return expected_revenue * probability


def calculate_simple_variant_emv(var_data: list, years):
    """
    :param var_data: list of parameters in the following order: M, D1, D2, P1, P2
    :param years: number for years for this variant
    :return: emv for this variant
    """
    M, D1, P1, D2, P2 = get_data_variables(var_data)
    expected_revenue_d1 = calculate_expected_revenue(D1, years, M)
    expected_revenue_d2 = calculate_expected_revenue(D2, years, M)
    emv = calculate_emv(expected_revenue_d1, P1) + calculate_emv(expected_revenue_d2, P2)
    return emv


var_a_data = data[0].copy()
var_a_emv = calculate_simple_variant_emv(var_a_data, years)

var_b_data = data[1].copy()
var_b_emv = calculate_simple_variant_emv(var_b_data, years)

# варіант В позначимо як C - який складається із варіантів D та E - при позитивній інформації
P1, P2, P3, P4 = float(data[2][0]), float(data[2][1]),  float(data[2][2]), float(data[2][3])

var_d_data = data[0].copy()
var_d_data[2], var_d_data[4] = P3, P4
var_d_emv = calculate_simple_variant_emv(var_d_data, years_c_var)

var_e_data = data[1].copy()
var_e_data[2], var_e_data[4] = P3, P4
var_e_emv = calculate_simple_variant_emv(var_e_data, years_c_var)

if var_d_emv > var_e_emv:
    var_c_emv = calculate_emv(var_d_emv, P1) + calculate_emv(0, P2)
else:
    var_c_emv = calculate_emv(var_e_emv, P1) + calculate_emv(0, P2)


def form_rows(var_data, names, years):
    M, D1, P1, D2, P2 = get_data_variables(var_data)
    expected_revenue_row_1 = calculate_expected_revenue(D1, years, M)
    expected_revenue_row_2 = calculate_expected_revenue(D2, years, M)
    row_1 = [names[0], D1, years, expected_revenue_row_1, P1]
    row_2 = [names[0], D2, years, expected_revenue_row_2, P2]
    return [row_1, row_2]


def output_variants():
    table = PrettyTable(['Варіант', 'EMV'])
    rows = list()
    rows.append(["A", var_a_emv])
    rows.append(["B", var_b_emv])
    rows.append(["C", var_c_emv])
    for row in rows:
        table.add_row(row)
    return table


def output_general():
    table = PrettyTable(['Альтернатива', 'Дохід', 'К-сть років', 'Очікуваний дохід', 'Імовірність'])
    rows = list()
    rows.append(form_rows(var_a_data, ["Великий завод, великий попит", "Великий завод, низький попит"], years))
    rows.append(form_rows(var_b_data, ["Маленький завод, великий попит", "Маленький завод, низький попит"], years))
    for row in rows:
        table.add_row(row[0])
        table.add_row(row[1])
    table.add_row(["Відкласти будівництво, позитивна інформація", 0, 1, 0, P1])
    rows = list()
    rows.append(form_rows(var_d_data, ["Великий завод, великий попит", "Великий завод, низький попит"], years_c_var))
    rows.append(form_rows(var_e_data, ["Великий завод, великий попит", "Великий завод, низький попит"], years_c_var))
    for row in rows:
        table.add_row(row[0])
        table.add_row(row[1])
    table.add_row(["Відкласти будівництво, негативна інформація", 0, 1, 0, P2])
    return table


print(output_variants())
print(output_general())
