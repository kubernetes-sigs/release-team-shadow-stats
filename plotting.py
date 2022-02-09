#
# This file contains logic to generate diagrams
#

import matplotlib.pyplot as plt
from collections import Counter
from vars import *

# generic method to display percentage and amount on charts


def make_autopct(values):
    def my_autopct(pct):
        total = sum(values)
        val = int(round(pct*total/100.0))
        return '{p:.2f}%  ({v:d})'.format(p=pct, v=val)
    return my_autopct

#
# CHARTS
#

# Applicants by team


def applicants_by_team(total_applicants, release_teams_dict_df):
    release_team_applicants = [len(v[group_newcomers]) + len(v[group_returners])
                               for _, v in release_teams_dict_df.items()]
    fig1, ax1 = plt.subplots()
    ax1.pie(release_team_applicants, labels=release_teams_dict_df.keys(),
            autopct=make_autopct(release_team_applicants))
    ax1.axis('equal')
    print("SIG-Release applicants by team")
    print(
        f"Total applicants: {total_applicants}, which applied to one or multiple teams")
    plt.savefig(get_plot_file("applicants-by-team"))
    plt.style.use(theme_matplotlib)
    # plt.show()

# Rejected newcomers which apply again


def reapplying_newcomers(newcomers_applied_previously, team=""):
    print("Rejected newcomers which apply again")
    apply_again = {"Reapplying newcomers": 0,
                   "First time applicants": 0, "Unclear": 0}
    for s in newcomers_applied_previously:
        s = str(s).lower()
        if "yes" in s or "yeah" in s:
            apply_again["Reapplying newcomers"] += 1
        elif "no" in s or "n/a" in s:
            apply_again["First time applicants"] += 1
        else:
            apply_again["Unclear"] += 1
    fig4, ax5 = plt.subplots()
    ax5.pie(apply_again.values(), labels=apply_again.keys(),
            autopct=make_autopct(apply_again.values()))
    ax5.axis('equal')
    plt.savefig(get_plot_file(f"reapplying-newcomers{team}"))
    plt.style.use(theme_matplotlib)
    # plt.show()

# chart to highlight applicant pronouns
# @data: string[]


def pronouns_chart(data, team=""):
    print(f"Pronouns {team}")
    fig4, ax4 = plt.subplots()
    applicant_pronouns = {"he/they": 0, "he/him": 0, "she/her": 0, "she/they": 0,
                          "they/them": 0, "ze": 0, "neopronouns": 0, "other": 0}
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
            print(clean_e)
            applicant_pronouns["other"] += 1
    # delete all pronous that do not occur
    resize_applicant_pronouns = applicant_pronouns.copy()
    for k in applicant_pronouns:
        if applicant_pronouns[k] == 0:
            del resize_applicant_pronouns[k]
    ax4.pie(resize_applicant_pronouns.values(), labels=resize_applicant_pronouns.keys(
    ), autopct=make_autopct(resize_applicant_pronouns.values()))
    ax4.axis('equal')
    plt.savefig(get_plot_file(f"pronouns{team}"))
    plt.style.use(theme_matplotlib)
    # plt.show()

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
                number_of_applicants_which_also_applied_to_another_team += 1
            for e in interested_in_teams:
                applied_to_team_as_well[e.strip()] = applied_to_team_as_well.get(
                    e.strip(), 0) + 1

    if team != "":
        del applied_to_team_as_well[team]
        print(
            f"{number_of_applicants_which_also_applied_to_another_team} of {len(release_teams[team][group_returners]) + len(release_teams[team][group_newcomers])} also applied to one or more of the other teams")
    ax3.pie(applied_to_team_as_well.values(), labels=applied_to_team_as_well.keys(
    ), autopct=make_autopct(applied_to_team_as_well.values()))
    ax3.axis('equal')
    plt.savefig(get_plot_file(f"applyied-to-other-teams-{team}"))
    plt.style.use(theme_matplotlib)
    # plt.show()

# filter newcomers and returners by team


def newcomers_and_returners(returners_df, newcomers_df, team=""):
    if team != "":
        team = f" for {team}"
    print(f"Newcomer & Returner applicants{team}")
    fig2, ax2 = plt.subplots()
    team_returners_and_newcomers = [len(returners_df), len(newcomers_df)]
    print(team_returners_and_newcomers)
    ax2.pie(team_returners_and_newcomers, 
        labels=[group_returners.capitalize(), group_newcomers.capitalize()], 
        autopct=make_autopct(team_returners_and_newcomers)
        )
    ax2.axis('equal')
    plt.savefig(get_plot_file(f"returners-and-newcomers{team}"))
    plt.style.use(theme_matplotlib)
    # plt.show()

# generic filter of entities


def filter_entities(entities_list, entities_description="Entities", keywords=[], aliases={}, threshold=1, unreached_threshold_print=False, team=""):
    # clean entities
    clean_entities = []
    for a in entities_list:
        if a is not None and type(a) is str:
            a = a.lower()
            keyword_or_alias_found = False
            for keyword in keywords:
                if keyword in a:
                    clean_entities.append(keyword)
                    keyword_or_alias_found = True
                    break
            if not keyword_or_alias_found:
                for alias, alias_repl in aliases.items():
                    if alias in a:
                        clean_entities.append(alias_repl)
                        keyword_or_alias_found = True
                        break
            if not keyword_or_alias_found:
                clean_entities.append(a)
    # count up entities
    affiliation_dict = Counter(clean_entities)
    affiliation_dict_threshold = dict()
    if unreached_threshold_print:
        print("Entities which do not reach threshold")
    for affiliation, count in affiliation_dict.items():
        if count > threshold:
            affiliation_dict_threshold[affiliation] = count
        elif unreached_threshold_print:
            print(affiliation)

    # create chart
    print(f"\n{entities_description} of applicants with a threshold of {threshold}")
    fig6, ax6 = plt.subplots()
    ax6.pie(affiliation_dict_threshold.values(), labels=affiliation_dict_threshold.keys(
    ), autopct=make_autopct(affiliation_dict_threshold.values()))
    ax6.axis('equal')
    plt.savefig(get_plot_file(f"entites{entities_description}{team}"))
    plt.style.use(theme_matplotlib)
    # plt.show()
