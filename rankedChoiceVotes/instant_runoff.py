"""
instant_runoff.py
author: Owen Mathay
"""

import sys
import os
import math
import pygame
import pandas as pd
import voting_methods as vm
import bargraphs as bg
import tkinter as tk
from button import Button
from tkinter.filedialog import askopenfilename
tk.Tk().withdraw()  # Part of the import - Leave!

pygame.init()
pygame.event.set_allowed([pygame.KEYDOWN, pygame.QUIT, pygame.MOUSEBUTTONDOWN])
SCREEN_DIM = WIDTH, HEIGHT = 600, 600
SCREEN = pygame.display.set_mode(SCREEN_DIM)
CLOCK = pygame.time.Clock()
FPS = 60

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (28, 128, 28)
YELLOW = (100, 85, 0)
BROWN = (118, 92, 72)
GRAY = (175, 175, 175)
BLUE = (0, 0, 175)
RED = (175, 0, 0)

FONT = pygame.font.Font('resources/Lato-Bold.ttf', 20)
MENU_BIG = pygame.font.Font('resources/Lato-Bold.ttf', 60)
MENU_MED = pygame.font.Font('resources/Lato-Bold.ttf', 25)
MENU_EHH = pygame.font.Font('resources/Lato-Bold.ttf', 20)
MENU_SMALL = pygame.font.Font('resources/Lato-Bold.ttf', 15)
MENU_FILE = pygame.font.Font('resources/Lato-Bold.ttf', 10)

TITLE_SCREEN = True
INFO_SCREEN = False
FILE_SELECT = False
PROCESS = False  # Change state of file select screen but also function of the program
REVIEW = False  # Change state of file select screen but also function of the program
CONFIRM_FILE = False  # Additional state for the File Select screen
INIT = False
INIT2 = False
RUNNING = False
COMPLETE = False
DISPLAY_RESULTS = False
EXPORTED = False
BREAKDOWN = False
DONE_BREAKDOWN = False

b_process = Button('process1', 135, 400)
b_review = Button('review', 315, 400)
b_info = Button('info', 525, 25)
b_back = Button('back', 25, 25)
b_yes = Button('yes', 315, 400)
b_yes.norm_color = (28, 128, 28)
b_yes.hover_color = (23, 105, 23)
b_no = Button('no', 135, 400)
b_no.norm_color = (125, 0, 0)
b_no.hover_color = (100, 0, 0)
b_file = Button('select_file', WIDTH / 2 - 75, 375)
b_home = Button('home_screen', 135, 400)
b_breakdown = Button('detailed_breakdown', 315, 400)
b_next = Button('next', WIDTH / 2 - 75, 500)

back = MENU_MED.render("<-", True, WHITE)
back_r = back.get_rect(center=(50, 50))

execution = ""
filename = ""
win_type = "majority"
tied = "._._."

data = None
df_export = pd.DataFrame()
candidates = dict()
order_candidates = []
all_candidates = []
elim_queue = []
winner_s = []
review_candidates = []
total_votes = 0
total_candidates = 0

while True:

    while TITLE_SCREEN:
        CLOCK.tick(15)
        SCREEN.fill(WHITE)

        title = MENU_BIG.render("INSTANT RUNOFF", True, BLACK)
        title2 = MENU_BIG.render("VOTE APP", True, BLACK)
        title_r = title.get_rect(center=(WIDTH / 2, 120))
        title2_r = title2.get_rect(center=(WIDTH / 2, 170))
        BALLOT_BOX = pygame.transform.scale(pygame.image.load('resources/ballotbox.png'), (225, 225))
        ballot_r = BALLOT_BOX.get_rect(center=(WIDTH / 2, HEIGHT / 2))
        process = MENU_MED.render("PROCESS", True, WHITE)
        process_r = process.get_rect(center=((WIDTH / 2) - 90, (HEIGHT / 2) + 125))
        review = MENU_MED.render("REVIEW", True, WHITE)
        review_r = review.get_rect(center=((WIDTH / 2) + 90, (HEIGHT / 2) + 125))
        info_t = MENU_MED.render("i", True, WHITE)
        info_tr = info_t.get_rect(center=(550, 50))

        mouse = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if b_process.hover(mouse):
                    print("Clicked Process")
                    PROCESS = True
                    FILE_SELECT = True
                    INIT = True
                    TITLE_SCREEN = False
                    execution = "PROCESS"
                elif b_review.hover(mouse):
                    print("Clicked Review")
                    REVIEW = True
                    FILE_SELECT = True
                    TITLE_SCREEN = False
                    execution = "REVIEW"
                elif b_info.hover(mouse):
                    print("Clicked Info")
                    INFO_SCREEN = True
                    TITLE_SCREEN = False
                else:
                    print("Click")

        SCREEN.blit(title, title_r)
        SCREEN.blit(title2, title2_r)
        SCREEN.blit(BALLOT_BOX, ballot_r)

        if b_process.hover(mouse):
            SCREEN.fill(b_process.color, b_process.rect)
        else:
            SCREEN.fill(b_process.color, b_process.rect)
        SCREEN.blit(process, process_r)
        if b_review.hover(mouse):
            SCREEN.fill(b_review.color, b_review.rect)
        else:
            SCREEN.fill(b_review.color, b_review.rect)
        SCREEN.blit(review, review_r)
        if b_info.hover(mouse):
            pygame.draw.circle(SCREEN, (0, 0, 175), (550, 50), 25)
        else:
            pygame.draw.circle(SCREEN, (0, 5, 210), (550, 50), 25)
        SCREEN.blit(info_t, info_tr)

        pygame.display.update()

    while INFO_SCREEN:
        CLOCK.tick(15)
        SCREEN.fill(WHITE)

        header = MENU_BIG.render("Information", True, BLACK)
        header_r = header.get_rect(center=(WIDTH / 2, 50))
        mouse = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if b_back.hover(mouse):
                    print("Clicked back!")
                    TITLE_SCREEN = True
                    INFO_SCREEN = False

        if b_back.hover(mouse):
            pygame.draw.circle(SCREEN, (150, 35, 0), (50, 50), 25)
        else:
            pygame.draw.circle(SCREEN, (175, 50, 0), (50, 50), 25)
        SCREEN.blit(back, back_r)
        SCREEN.blit(header, header_r)

        pygame.display.update()

    while FILE_SELECT:
        CLOCK.tick(15)
        SCREEN.fill(WHITE)
        mouse = pygame.mouse.get_pos()

        if not CONFIRM_FILE:
            prompt1 = MENU_BIG.render("Please select a file", True, BLACK)
            prompt2 = MENU_BIG.render("to continue.", True, BLACK)
            prompt1_r = prompt1.get_rect(center=(WIDTH / 2, HEIGHT / 4))
            prompt2_r = prompt2.get_rect(center=(WIDTH / 2, HEIGHT / 4 + 50))
            file_t = MENU_EHH.render("Click to choose", True, BLUE)
            file_tr = file_t.get_rect(center=(WIDTH / 2, 400))

            if b_back.hover(mouse):
                pygame.draw.circle(SCREEN, (150, 35, 0), (50, 50), 25)
            else:
                pygame.draw.circle(SCREEN, (175, 50, 0), (50, 50), 25)
            SCREEN.blit(back, back_r)
            if b_file.hover(mouse):
                SCREEN.fill(b_file.color, b_file.rect)
            else:
                SCREEN.fill(b_file.color, b_file.rect)
            SCREEN.blit(file_t, file_tr)
        else:
            prompt1 = MENU_BIG.render("Is this the file you", True, BLACK)
            prompt2 = MENU_BIG.render("want to examine?", True, BLACK)
            prompt1_r = prompt1.get_rect(center=(WIDTH / 2, HEIGHT / 4))
            prompt2_r = prompt2.get_rect(center=(WIDTH / 2, HEIGHT / 4 + 50))
            yes_t = MENU_MED.render("YES", True, WHITE)
            yes_tr = yes_t.get_rect(center=((WIDTH / 2) + 90, (HEIGHT / 2) + 125))
            no_t = MENU_MED.render("NO", True, WHITE)
            no_tr = no_t.get_rect(center=((WIDTH / 2) - 90, (HEIGHT / 2) + 125))
            if b_yes.hover(mouse):
                SCREEN.fill(b_yes.color, b_yes.rect)
            else:
                SCREEN.fill(b_yes.color, b_yes.rect)
            SCREEN.blit(yes_t, yes_tr)
            if b_no.hover(mouse):
                SCREEN.fill(b_no.color, b_no.rect)
            else:
                SCREEN.fill(b_no.color, b_no.rect)
            SCREEN.blit(no_t, no_tr)

        name_t = MENU_SMALL.render(f"{filename}", True, BLACK)
        name_tr = name_t.get_rect(center=(WIDTH / 2, HEIGHT / 2 + 25))
        SCREEN.blit(prompt1, prompt1_r)
        SCREEN.blit(prompt2, prompt2_r)
        pygame.draw.rect(SCREEN, BLACK, pygame.Rect((50, HEIGHT / 2), (500, 50)), 2)
        SCREEN.blit(name_t, name_tr)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if b_back.hover(mouse):
                    TITLE_SCREEN = True
                    FILE_SELECT = False
                    REVIEW = False
                    PROCESS = False
                    INIT = False
                    INIT2 = False
                    execution = ""
                    tied = "._._."

                if b_file.hover(mouse) and not CONFIRM_FILE:
                    print("User selecting a file")
                    filename = askopenfilename(initialdir="resources")
                    if not filename == "":
                        print(f"User selected {filename}")
                        CONFIRM_FILE = True
                    else:
                        print("User failed to select a file.")
                        filename = "Please try again."
                if b_yes.hover(mouse) and CONFIRM_FILE:
                    CONFIRM_FILE = False
                    RUNNING = True
                    FILE_SELECT = False
                    print("User confirmed.")
                if b_no.hover(mouse) and CONFIRM_FILE:
                    print("User declined.")
                    filename = "Please try again."
                    CONFIRM_FILE = False

        pygame.display.update()

    while RUNNING:
        CLOCK.tick(15)
        SCREEN.fill(WHITE)

        if INIT:
            INIT = False
            data = vm.set_file(filename)
            total_votes = len(data.index)
            total_candidates = len(data.columns)
            vm.initialize(data, candidates, total_votes)
            vm.sort_votes(order_candidates, all_candidates, candidates)
            order_candidates = sorted(order_candidates, key=lambda x: len(x.ballots), reverse=True)

        if PROCESS:
            tied = "._._."
            order_candidates = sorted(order_candidates, key=lambda x: len(x.ballots), reverse=True)
            temp_minimum = vm.num_with_min(order_candidates, order_candidates[-1].n_votes())

            if temp_minimum == 1:
                elim_queue.append(order_candidates[-1])
                order_candidates[-1].eliminated = True
            else:
                if len(order_candidates) == 2:
                    temp = vm.tie_first(order_candidates, total_votes)
                    if temp.name == "Inconclusive":
                        RUNNING = False
                        DISPLAY_RESULTS = True
                        winner_s.extend(order_candidates)
                        temp_dict = dict()
                        for winner in winner_s:
                            temp_dict[winner.name] = [winner.name]
                        df_results = pd.DataFrame(temp_dict, index=["inconclusive"])
                        df_export = pd.concat([df_export, df_results])
                    else:
                        win_type = "tiebreaker"
                        tied = 'tied'
                        cand = candidates[temp.name]
                        elim_queue.append(cand)
                else:
                    temp = vm.tie_last(order_candidates[-1 * temp_minimum:])
                    tied = "tied"
                    for ele in temp:
                        ele.eliminated = True
                    elim_queue.extend(temp)

            if order_candidates[0].n_votes() >= math.ceil(total_votes / 2):
                tied = "end"
            df_temp = pd.DataFrame(
                vm.create_dict(candidates),
                index=["# Votes", "Eliminated?", f"{tied}"])
            df_export = pd.concat([df_export, df_temp])

            vm.redistribute(elim_queue, order_candidates, candidates, total_votes)
            elim_queue.clear()
            if len(order_candidates) == 1:
                COMPLETE = True
                RUNNING = False
                DISPLAY_RESULTS = True
                df_results = pd.DataFrame({order_candidates[0].name: [order_candidates[0].name]}, index=[f"{win_type}"])
                df_export = pd.concat([df_export, df_results])
                winner_s.extend(order_candidates)

            pygame.draw.rect(SCREEN, BLACK, pygame.Rect((50, HEIGHT / 2), (500, 50)), 2)
            pygame.draw.rect(SCREEN, GREEN, pygame.Rect((55, HEIGHT / 2), (
                max(0, int(490 * (total_candidates - len(candidates) + 1) / total_candidates)),
                45)))  # max of 490 to leave pixels

        elif REVIEW:
            data = vm.set_file(filename)
            vm.review_path(filename, candidates, total_votes, order_candidates, all_candidates)
            hold_list = data.iloc[-1].tolist()[1:]
            yo = [i for i in hold_list[1:] if i != "---"]
            winner_s.append(candidates.get(yo[0]))
            win_type = hold_list[0]
            RUNNING = False
            DISPLAY_RESULTS = True
            EXPORTED = True
            COMPLETE = True
            PROCESS = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        pygame.display.update()

    while DISPLAY_RESULTS:

        CLOCK.tick(15)
        SCREEN.fill(WHITE)
        mouse = pygame.mouse.get_pos()

        export_disclaimer = MENU_FILE.render("Processed file exported as", True, BLACK)
        export_disclaimer2 = MENU_FILE.render(f"{filename[:-4]}_export.csv.", True, BLUE)
        export_dr = export_disclaimer.get_rect(center=(WIDTH / 2, 500))
        export_dr2 = export_disclaimer2.get_rect(center=(WIDTH/2, 520))
        home_text = MENU_MED.render("Main Screen", True, BLACK)
        home_tr = home_text.get_rect(center=(210, 425))
        break_text = MENU_MED.render("Details", True, BLACK)
        break_tr = break_text.get_rect(center=(380, 425))
        results_text = MENU_BIG.render("RESULTS", True, BLACK)
        results_tr = results_text.get_rect(center=(WIDTH/2, 100))
        tiebreaker_ex = MENU_SMALL.render("First-round votes were recalled, and this candidate", True, BLACK)
        tiebreaker_ex2 = MENU_SMALL.render("had more than their opponent in the last round.", True, BLACK)
        tiebreaker_etr = tiebreaker_ex.get_rect(center=(WIDTH/2, 250))
        tiebreaker_etr2 = tiebreaker_ex2.get_rect(center=(WIDTH/2, 270))

        if not EXPORTED:
            EXPORTED = True
            df_export.to_csv(f"{filename[:-4]}_export.csv", na_rep="---")
            print(df_export)
            print("Exported file to same location as original data.")

        # If PROCESS: Display the location of the exported CSV file
        if PROCESS:
            SCREEN.blit(export_disclaimer, export_dr)
            SCREEN.blit(export_disclaimer2, export_dr2)

        if COMPLETE:  # Found a winner
            # Display the name of the winner (and if it was found by majority or first tally tiebreaker)
            winner_text = MENU_MED.render(f"{winner_s[0].name} wins by {win_type}.", True, BLACK)
            winner_tr = winner_text.get_rect(center=(WIDTH/2, 200))
            if win_type == "tiebreaker":
                SCREEN.blit(tiebreaker_ex, tiebreaker_etr)
                SCREEN.blit(tiebreaker_ex2, tiebreaker_etr2)
            SCREEN.blit(winner_text, winner_tr)

        else:  # Reached the end, but inconclusive. Recommend a tiebreaker election between two
            # Display the top two that the tiebreaker couldn't fix and recommend another tiebreaker
            winner_text = MENU_MED.render(f"{winner_s[0].name} and {winner_s[1].name} have tied.")
            tie_text3 = MENU_SMALL.render("A first-tally tiebreaker was attempted, but inconclusive.",
                                          True, BLACK)
            tie_text4 = MENU_SMALL.render("A follow-up special election is recommended", True, BLACK)
            winner_tr = winner_text.get_rect(center=(WIDTH/2, 200))
            tie_text_tr3 = tie_text3.get_rect(center=(WIDTH/2, 250))
            tie_text_tr4 = tie_text4.get_rect(center=(WIDTH/2, 270))
            SCREEN.blit(tie_text3, tie_text_tr3)
            SCREEN.blit(tie_text4, tie_text_tr4)

        if b_home.hover(mouse):
            SCREEN.fill(b_home.color, b_home.rect)
        else:
            SCREEN.fill(b_home.color, b_home.rect)
        SCREEN.blit(home_text, home_tr)
        if b_breakdown.hover(mouse):
            SCREEN.fill(b_breakdown.color, b_breakdown.rect)
        else:
            SCREEN.fill(b_breakdown.color, b_breakdown.rect)
        SCREEN.blit(break_text, break_tr)
        SCREEN.blit(results_text, results_tr)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if b_home.hover(mouse):
                    filename = ""
                    win_type = "majority"
                    execution = ""
                    tied = "._._."

                    candidates = dict()
                    order_candidates = []
                    all_candidates = []
                    elim_queue = []
                    winner_s = []
                    review_candidates = []
                    total_votes = 0
                    total_candidates = 0
                    TITLE_SCREEN = True
                    INIT = False
                    DISPLAY_RESULTS = False
                    PROCESS = False
                    REVIEW = False
                    EXPORTED = False
                    COMPLETE = False
                    RUNNING = False
                if b_breakdown.hover(mouse):
                    if not REVIEW:
                        filename = f"{filename[:-4]}_export.csv"
                    datareview = pd.read_csv(filename).reset_index()
                    review_candidates = list(datareview.columns.values.tolist())[2:]
                    datareview.set_index('Unnamed: 0', inplace=True)
                    DISPLAY_RESULTS = False
                    BREAKDOWN = True
                    PROCESS = False
                    REVIEW = False
                    INIT2 = True

        pygame.display.update()

        ROUND_NUM = 0
        while BREAKDOWN:
            CLOCK.tick(15)
            SCREEN.fill(WHITE)
            mouse = pygame.mouse.get_pos()

            if INIT2:
                INIT2 = False
                graph_dict = dict()
                removal = []
                for candidate in review_candidates:
                    graph_dict[candidate] = datareview.iloc[(ROUND_NUM * 3)][candidate]
                    if datareview.iloc[((ROUND_NUM * 3) + 1)][candidate] == "True":
                        print(f"Uh oh, {candidate} got eliminated!")
                        removal.append(candidate)
                if datareview.index[((ROUND_NUM * 3) + 2)] == "end":
                    print("That's all, we've reached the end")
                    DONE_BREAKDOWN = True
                elif datareview.index[((ROUND_NUM * 3) + 2)] == "tied" and len(review_candidates) == 2:
                    print("A tie was reached!")
                    DONE_BREAKDOWN = True
                ROUND_NUM += 1
                print(graph_dict)
                bg.design(graph_dict, ROUND_NUM)
                graph_img = pygame.transform.smoothscale(pygame.image.load('cache_bar_graphs/graph.png'),
                                                         (480, 360))
                review_candidates = [x for x in review_candidates if x not in removal]


            top = MENU_BIG.render(f"Round {ROUND_NUM}", True, BLACK)
            top_r = top.get_rect(center=(WIDTH/2, 50))
            next_text = MENU_MED.render("NEXT", True, BLACK)
            next_tr = next_text.get_rect(center=(WIDTH / 2, 525))
            call_race = MENU_MED.render(f"{review_candidates[0]} has reached 50% and won.", True, BLACK)
            call_rr = call_race.get_rect(center=(WIDTH/2, 100))

            if DONE_BREAKDOWN:
                SCREEN.blit(call_race, call_rr)

            SCREEN.blit(top, top_r)
            SCREEN.blit(graph_img, (60, 120))
            if b_next.hover(mouse):
                SCREEN.fill(b_next.color, b_next.rect)
            else:
                SCREEN.fill(b_next.color, b_next.rect)
            SCREEN.blit(next_text, next_tr)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if b_next.hover(mouse):
                        if not DONE_BREAKDOWN:
                            INIT2 = True
                        else:
                            BREAKDOWN = False
                            DONE_BREAKDOWN = False
                            filename = ""
                            datareview = None
                            data = None
                            df_export = pd.DataFrame()
                            win_type = "majority"
                            execution = ""
                            tied = "._._."
                            candidates = dict()
                            order_candidates = []
                            all_candidates = []
                            elim_queue = []
                            winner_s = []
                            review_candidates = []
                            total_votes = 0
                            total_candidates = 0
                            TITLE_SCREEN = True
                            INIT = False
                            DISPLAY_RESULTS = False
                            PROCESS = False
                            REVIEW = False
                            EXPORTED = False
                            COMPLETE = False
                            RUNNING = False
                            if os.path.exists("cache_bar_graphs/graph.png"):
                                os.remove("cache_bar_graphs/graph.png")

            pygame.display.update()
