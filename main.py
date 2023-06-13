import pandas as pd
from dataclasses import dataclass
import random as ra


@dataclass
class VoterObject:
    votes: list


def create_voters(data):
    total_voters = len(data.index)
    voter_count = 0
    lo_voters = []

    print(data.iloc[voter_count])

    while total_voters > voter_count:
        lo_voters.append(assign_votes(data.iloc[voter_count].drop(labels=['index', 'Timestamp'])))
        voter_count = voter_count + 1

    return lo_voters


def assign_votes(row_data):
    ranked_votes = []
    for candidate in row_data:
        ranked_votes.append(candidate)

    return VoterObject(ranked_votes)


def set_up_file(file):
    election_file = pd.read_csv(file)
    election_file = election_file.reset_index()
    print('file initializing....\n')
    print(election_file)
    return election_file


def initial_subdivision(voters):
    counted_votes = dict()
    for voter in voters:

        if voter.votes[0] not in counted_votes:
            temp_list = [voter]
            counted_votes[voter.votes[0]] = temp_list
        else:
            temp_list = counted_votes[voter.votes[0]]
            temp_list.append(voter)
            counted_votes[voter.votes[0]] = temp_list

    a = counted_votes.keys()
    for key in a:
        print(counted_votes[key])
    return counted_votes


def check_for_winner(divided_votes, eliminated):
    # least_votes = 1
    WINNER_FOUND = False
    percent_dict = dict()
    keys = divided_votes.keys()

    for key in keys:
        temp_list = divided_votes[key]
        percent = len(temp_list) / total_num_voters
        percent_dict[key] = percent
        print('Candidate: ' + key + ', Number of Votes: '
              + str(len(temp_list)) + ', Percentage of Vote: ' + str(int(percent * 10000) / 100) + ' %')

    least_support = []
    minimum_votes = 1.0
    for key in percent_dict:
        if percent_dict[key] > 0.5:
            WINNER_FOUND = True
            winning_candidate = key
        elif percent_dict[key] < minimum_votes:
            minimum_votes = percent_dict[key]
            least_support.clear()
            least_support.append(key)
        elif percent_dict[key] == minimum_votes:
            least_support.append(key)

    if WINNER_FOUND:
        print(winning_candidate + ' is the winner!')

    else:
        print('No candidate has reached a clear majority.')
        if len(least_support) != len(divided_votes):
            last_place = random_from_list(least_support)
            remove_last_place(divided_votes, last_place, eliminated)
        else:
            print('However, there is a tie between the candidates above,')
            print('indicating that a runoff election is necessary.')


def random_from_list(votes_list):
    if len(votes_list) > 0:
        print("There is a tie for last, and the candidate removed will be decided at random.")
        selected = ra.randint(0, len(votes_list) - 1)
    else:
        selected = 0
    print('Removing ' + votes_list[selected] + ' from the options...')
    return votes_list[selected]


def remove_last_place(assigned_votes, last_candidate, eliminated):
    eliminated.append(last_candidate)
    new_dict = dict()
    keys = assigned_votes.keys()
    for key in keys:
        if key is not last_candidate:
            new_dict[key] = assigned_votes[key]

    for voter in assigned_votes[last_candidate]:
        print("A vote for " + voter.votes[0] + " is removed...")
        voter.votes.pop(0)

        while voter.votes[0] in eliminated:
            voter.votes.pop(0)
        print("and this vote will count towards " + voter.votes[0])
        temp_list = new_dict[voter.votes[0]]
        temp_list.append(voter)
        new_dict[voter.votes[0]] = temp_list

    check_for_winner(new_dict, eliminated)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    unsuccessful_input = True
    while unsuccessful_input:
        file_name = input('Please type the name of the file.\n')
        try:
            election = set_up_file(file_name)
        except FileNotFoundError:
            print('No such file was found. ')
        else:
            unsuccessful_input = False

    total_num_voters = len(election.index)
    total_num_candidates = len(election.columns)
    list_of_voters = create_voters(election)
    voter_dict = initial_subdivision(list_of_voters)
    check_for_winner(voter_dict, [])
