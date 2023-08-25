"""
candidate.py
author: Owen Mathay
"""


class Candidate:
    active = True
    eliminated = False
    first_tally = 0

    def __init__(self, name):
        self.name = name
        self.first_round_tally = 0
        self.ballots = []
        self.color = (0, 0, 0)

    def n_votes(self):
        return len(self.ballots)

    def eliminate(self):
        self.color = (185, 0, 0)
        # self.name = self.name + "(Eliminated)"
        self.active = False
        self.eliminated = True

    def remember_first(self):
        self.first_tally = self.n_votes()

    def tally_for(self, that):
        count = 0
        for vote in self.ballots:
            if vote[1] == that.name:
                count += 1
        return count
