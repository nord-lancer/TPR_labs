import csv
import itertools
import operator
from prettytable import PrettyTable

data = dict()
candidates = str()

with open('lab_3_data.csv', newline='') as csv_file:
    reader = csv.reader(csv_file, delimiter=',', skipinitialspace=True)
    first = True
    for line in reader:
        if first:
            candidates = line[0]
            first = False
        buff = [line[0], int(line[1])]
        data[buff[0]] = buff[1]


def get_winner(candidate_1, candidate_2, votes_bucket):
    all_candidates = list(votes_bucket)
    if all_candidates.index(candidate_1) < all_candidates.index(candidate_2):
        return candidate_1
    else:
        return candidate_2


def get_votes_for_candidate_pair(candidates_pair):
    candidate_1, candidate_2 = candidates_pair[0], candidates_pair[1]
    candidate_1_votes = 0
    candidate_2_votes = 0
    for votes_bucket in data:
        winner = get_winner(candidate_1, candidate_2, votes_bucket)
        if winner == candidate_1:
            candidate_1_votes += data[votes_bucket]
        else:
            candidate_2_votes += data[votes_bucket]
    votes = dict()
    votes[candidate_1] = candidate_1_votes
    votes[candidate_2] = candidate_2_votes
    return votes


def get_pair_combinations(candidates):
    candidates_combinations = list()
    for i in itertools.combinations(candidates, 2):
        candidates_combinations.append(i)
    return candidates_combinations


def condorcet():
    print("\nМетод Кондорсе")
    candidates_combinations = get_pair_combinations(candidates)
    pairs_and_votes = [get_votes_for_candidate_pair(i) for i in candidates_combinations]
    wins = dict()
    for i in candidates:
        wins[i] = 0
    for i in pairs_and_votes:
        wins[max(i, key=i.get)] += 1
    winner = max(wins, key=wins.get)
    print_condorcet_tables(pairs_and_votes, wins, winner)


def get_empty_candidates_votes():
    candidates_votes = dict()
    for i in list(candidates):
        candidates_votes[i] = 0
    return candidates_votes


def count_points_for_bucket(vote_bucket):
    candidates_votes = get_empty_candidates_votes()
    candidates_number = len(candidates_votes)
    vote_number = data[vote_bucket]
    preferences = list(vote_bucket)
    multiplier = candidates_number - 1
    for i in range(candidates_number):
        candidate = preferences[i]
        candidates_votes[candidate] += vote_number * multiplier
        multiplier -= 1
    return candidates_votes


def borda():
    print('Метод Борда')
    candidates_votes = get_empty_candidates_votes()
    for key in data:
        points = count_points_for_bucket(key)
        for candidate in points:
            candidates_votes[candidate] += points[candidate]
    winner = max(candidates_votes, key=candidates_votes.get)
    print_borda(candidates_votes, winner)


def print_borda(candidates_votes, winner):
    table = PrettyTable(['Кандидат', 'Кількість голосів'])
    for candidate in candidates_votes:
        table.add_row([candidate, candidates_votes[candidate]])
    print(table)
    print(f'Переможець: {winner}')


def print_condorcet_tables(pairs_and_votes, wins, winner):
    for pairs in pairs_and_votes:
        table = PrettyTable(['Кандидат', 'Кількість голосів'])
        for candidate in pairs:
            table.add_row([candidate, pairs[candidate]])
        print(table)
    table = PrettyTable(['Кандидат', 'Кількість перемог'])
    for i in wins:
        table.add_row([i, wins[i]])
    print(table)
    print(f"Переможець: {winner}")


def print_all_data():
    table = PrettyTable(['Ранжування кандидатів', 'Кількість голосів'])
    for key in data:
        table.add_row([key, data[key]])
    print(table)


borda()
condorcet()
