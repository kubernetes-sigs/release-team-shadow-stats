#
# This file contains logic to generate diagrams
#

import matplotlib.pyplot as plt
from vars import *

# generic method to display percentage and amount on charts
def make_autopct(values):
    def my_autopct(pct):
        total = sum(values)
        val = int(round(pct*total/100.0))
        return '{p:.2f}%  ({v:d})'.format(p=pct,v=val)
    return my_autopct

#
# CHARTS
#

# Applicants by team
def applicants_by_team(total_applicants, release_teams_dict_df):
    release_team_applicants = [len(v[group_newcomers]) + len(v[group_returners]) for _, v in release_teams_dict_df.items()]
    fig1, ax1 = plt.subplots()
    ax1.pie(release_team_applicants, labels=release_teams_dict_df.keys(), autopct=make_autopct(release_team_applicants))
    ax1.axis('equal')
    print("SIG-Release applicants by team")
    print(f"Total applicants: {total_applicants}, which applied to one or multiple teams")
    plt.show()

# Rejected newcomers which apply again
def reapplying_newcomers(newcomers_applied_previously):
    print("Rejected newcomers which apply again")
    apply_again = {"Reapplying newcomers": 0, "First time applicants": 0, "Unclear": 0}
    for s in newcomers_applied_previously:
        s = str(s).lower()
        if "yes" in s or "yeah" in s:
            apply_again["Reapplying newcomers"] += 1
        elif "no" in s or "n/a" in s :
            apply_again["First time applicants"] += 1
        else:
            apply_again["Unclear"] += 1
    fig4, ax5 = plt.subplots()
    ax5.pie(apply_again.values(), labels=apply_again.keys(), autopct=make_autopct(apply_again.values()))
    ax5.axis('equal')
    plt.show()

# chart to highlight applicant pronouns
# @data: string[]
def pronouns_chart(data, team=""):
    print(f"Pronouns {team}")
    fig4, ax4 = plt.subplots()
    applicant_pronouns = {"he/they":0, "he/him":0, "she/her": 0, "she/they": 0, "they/them":0, "ze": 0, "neopronouns": 0, "invalid pronoun": 0}
    for e in data:
        clean_e = str(e).replace("https://www.mypronouns.org/", "", 1).lower()
        if "she" in clean_e or "her" in clean_e:
            if "they" in clean_e or "them" in clean_e:
                applicant_pronouns["she/they"] += 1
            else:
                applicant_pronouns["she/her"] += 1
        elif "him" in clean_e or "he" in clean_e:
            if "they" in clean_e or "them" in clean_e:
                applicant_pronouns["he/they"] += 1
            else:
                applicant_pronouns["he/him"] += 1
        elif "they" in clean_e or "them" in clean_e:
            applicant_pronouns["they/them"] += 1
        elif "ze" in clean_e:
            applicant_pronouns["ze"] += 1
        elif "neopronouns" in clean_e:
            applicant_pronouns["neopronouns"] += 1
        else:
            applicant_pronouns["invalid pronoun"] += 1
    # delete all pronous that do not occur
    resize_applicant_pronouns = applicant_pronouns.copy()
    for k in applicant_pronouns:
        if applicant_pronouns[k] == 0:
            del resize_applicant_pronouns[k]
    ax4.pie(resize_applicant_pronouns.values(), labels=resize_applicant_pronouns.keys(), autopct=make_autopct(resize_applicant_pronouns.values()))
    ax4.axis('equal')
    plt.show()

# filter applicants which also applied to another team
# @applicants_interested_in_roles series[]
def applied_for_multiple_teams(applicants_interested_in_roles, team="", release_teams={}):
    print(f"{team} applicants applied to other teams")
    number_of_applicants_which_also_applied_to_another_team = 0
    fig3, ax3 = plt.subplots()
    applied_to_team_as_well = dict()
    for l in applicants_interested_in_roles:
        for e in l:
            interested_in_teams = e.split(", ")
            if len(interested_in_teams) > 1:
                number_of_applicants_which_also_applied_to_another_team+=1
            for e in interested_in_teams:
                applied_to_team_as_well[e.strip()] = applied_to_team_as_well.get(e.strip(), 0) + 1   

    if team != "":
        del applied_to_team_as_well[team]
        print(f"{number_of_applicants_which_also_applied_to_another_team} of {len(release_teams[team][group_returners]) + len(release_teams[team][group_newcomers])} also applied to one or more of the other teams")
    ax3.pie(applied_to_team_as_well.values(), labels=applied_to_team_as_well.keys(), autopct=make_autopct(applied_to_team_as_well.values()))
    ax3.axis('equal')
    plt.show()

# filter newcomers and returners by team
def newcomers_and_returners(returners_df, newcomers_df, team=""):
    if team != "":
        team = f" for {team}"
    print(f"Newcomer & Returner applicants{team}")
    fig2, ax2 = plt.subplots()
    team_returners_and_newcomers = [len(returners_df), len(newcomers_df)]
    ax2.pie(team_returners_and_newcomers, labels=[group_returners.capitalize(), group_newcomers.capitalize()], autopct=make_autopct(team_returners_and_newcomers))
    ax2.axis('equal')
    plt.show()