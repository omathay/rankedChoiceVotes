"""
bargraphs.py
author: Owen Mathay
"""
import math
import matplotlib.pyplot as plt


def design(data: dict, round: int):
    sorted_data = dict(sorted(data.items()))
    candidates = list(sorted_data.keys())
    votes = [int(element) for element in sorted_data.values()]
    total_votes = sum([int(i) for i in votes if type(i) == int or i.isdigit()])
    threshold = math.ceil(total_votes / 2)

    plt.bar(candidates, votes, color="red", width=0.4)
    plt.axhline(y=threshold + 1, color="black", linestyle=":")
    plt.axhline(y=threshold, color="orange", linestyle="--")
    plt.text((len(candidates) - 1) / 2, threshold, f"{threshold} Votes to Win",
             fontsize=10, va="center", ha="center",backgroundcolor="w")
    plt.xlabel("CANDIDATES", fontstyle="italic")
    plt.ylabel("No. of Votes", fontstyle="italic")
    plt.title(f"Round {round}")
    plt.savefig('cache_bar_graphs/graph.png')
    plt.close()
