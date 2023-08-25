"""
voting_methods.py
author: Owen Mathay
"""

import pandas as pd
from candidate import Candidate


def set_file(fn: str):
    print(f"Attempting file {fn}...")
    file_temp = pd.read_csv(fn).reset_index()
    print(file_temp)
    print(f"File {fn} initialized.")
    return file_temp


def initialize(data, candidates, total_votes):
    print("Now initializing candidates...")
    for j in range(len(data.index)):
        update_candidate(True, data.iloc[j].drop(labels=['index', 'Timestamp']), total_votes,
                         candidates)
    print("Candidates initialized! Now sorting candidates...")


def sort_votes(ranked: list, all: list, candidates: dict):
    for c in candidates.values():
        print(f"Sorting {c.name}.")
        ranked.append(c)
        all.append(c)


def review_path(filename: str, candidates: dict, total_votes: int, ranked: list, all: list):
    temp_name = set_file(f"{filename[:-11]}.csv")
    total_votes = len(temp_name.index)
    initialize(temp_name, candidates, total_votes)
    sort_votes(ranked, all, candidates)


def update_candidate(initializing: bool, data: pd.Series, num_votes: int, candidates_dict: dict):
    if len(data) == 0:
        num_votes -= 1
        print(f"One voter was removed early :(")
    elif data[0] in candidates_dict:
        candidates_dict.get(data[0]).ballots.append(data)
        print(f"Adding another vote to {data[0]}")
    elif initializing:
        new_cand = Candidate(data[0])
        candidates_dict[new_cand.name] = new_cand
        candidates_dict.get(data[0]).ballots.append(data)
        print(f"Made a new candidate! {new_cand.name}")
    else:
        update_candidate(initializing, data[1:], num_votes, candidates_dict)


def create_dict(candidates: dict):
    temp = dict()
    for c in candidates.values():
        temp[c.name] = [c.n_votes(), c.eliminated, "---"]
    return temp


def redistribute(queue: list, ranking: list, candidates: dict, total_votes: int):
    for cand in queue:
        print(f"Moving the votes for {cand.name} to their next choice.")
        del candidates[cand.name]
        cand.eliminate()
        ranking.remove(cand)
        for vote in cand.ballots:
            update_candidate(False, vote[1:], total_votes, candidates)


def num_with_min(ranking: list, minimum: int):
    count = 0
    for cand in ranking:
        if cand.n_votes() == minimum:
            count += 1
    return count


# RETURNS CANDIDATE(S) TO ELIMINATE
def tie_last(tied_candidates: list):
    global_max = 0
    checklist = dict()
    cand_best = Candidate("Inconclusive")
    for cand in tied_candidates:
        local_max = 0
        for check in [ele for ele in tied_candidates if ele is not cand]:
            local_max += check.tally_for(cand)
        checklist[cand] = local_max
        if local_max > global_max:
            global_max = local_max
            cand_best = cand
    count = 0
    for x in checklist.values():
        if x == global_max:
            count += 1
    if count > 1:
        return tied_candidates
    else:
        return [ele for ele in tied_candidates if ele is not cand_best]


# RETURNS CANDIDATE TO ELIMINATE
def tie_first(tied_candidates: list, total_votes: int):
    maxi = total_votes
    cand_less = Candidate("Inconclusive")
    for c in tied_candidates:
        if c.first_tally <= maxi:
            maxi = c.first_tally
            cand_less = c
    return cand_less
