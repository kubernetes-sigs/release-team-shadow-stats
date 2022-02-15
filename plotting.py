#
# This file contains logic to generate diagrams with matplotlib
#

from collections import Counter
from dataclasses import dataclass
import logging
import matplotlib.pyplot as plt
from vars import *


def make_autopct(values):
    """generic method to display percentage and amount on charts"""
    def my_autopct(pct):
        total = sum(values)
        val = int(round(pct*total/100.0))
        return f"{pct:.2f}%  ({val:d})"
    return my_autopct

#
# CHARTS
#


def applicants_by_team(total_applicants, release_teams_dict_df):
    """Applicants by team"""
    release_team_applicants = [
        len(v[GROUP_NEWCOMERS]) + len(v[GROUP_RETURNERS])
        for _, v in release_teams_dict_df.items()]
    _, ax1 = plt.subplots()
    ax1.pie(release_team_applicants, labels=release_teams_dict_df.keys(),
            autopct=make_autopct(release_team_applicants))
    ax1.axis('equal')
    logging.info("sig-release applicants by team")
    logging.info("Total applicants: %s, which applied to one or multiple teams", total_applicants)
    plt.style.use(THEME_MARPLOTLIB)
    plt.savefig(get_plot_file("applicants-by-team"))


def reapplying_newcomers(newcomers_applied_previously, team=""):
    """Rejected newcomers which apply again"""
    logging.info("Rejected newcomers which apply again")
    apply_again = {
        "Reapplying newcomers": 0,
        "First time applicants": 0,
        "Unclear": 0
    }
    for s in newcomers_applied_previously:
        s = str(s).lower()
        if "yes" in s or "yeah" in s:
            apply_again["Reapplying newcomers"] += 1
        elif "no" in s or "n/a" in s:
            apply_again["First time applicants"] += 1
        else:
            apply_again["Unclear"] += 1
    _, ax5 = plt.subplots()
    ax5.pie(apply_again.values(), labels=apply_again.keys(),
            autopct=make_autopct(apply_again.values()))
    ax5.axis('equal')
    plt.style.use(THEME_MARPLOTLIB)
    plt.savefig(get_plot_file(
        f"reapplying-newcomers-{team.replace(' ', '').lower()}"))


def pronouns_chart(pronouns_data: list[str], team=""):
    """chart to highlight applicant pronouns"""
    logging.warning("Pronouns for %s", team)
    _, ax4 = plt.subplots()
    applicant_pronouns = {
        "he/they": 0,
        "he/him": 0,
        "she/her": 0,
        "she/they": 0,
        "they/them": 0,
        "ze": 0,
        "neopronouns": 0,
        "other": 0
    }
    for pronoun_in_data in pronouns_data:
        clean_e = str(pronoun_in_data).replace("https://www.mypronouns.org/", "", 1).lower()
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
            logging.warning("could not find matching pronoun for %s, add it to others", clean_e)
            applicant_pronouns["other"] += 1
    # delete all pronous that do not occur
    resize_applicant_pronouns = applicant_pronouns.copy()
    for pronoun, count in applicant_pronouns.items():
        if count == 0:
            del resize_applicant_pronouns[pronoun]
    ax4.pie(resize_applicant_pronouns.values(), labels=resize_applicant_pronouns.keys(
    ), autopct=make_autopct(resize_applicant_pronouns.values()))
    ax4.axis('equal')
    plt.style.use(THEME_MARPLOTLIB)
    plt.savefig(get_plot_file(f"pronouns-{team.replace(' ', '').lower()}"))


def applied_for_multiple_teams(applicant_applied_to_teams: list[list[str]], team="", release_teams=None):
    """filter applicants which also applied to another team"""
    if release_teams is None:
        release_teams = {}
    logging.info("%s applicants applied to other teams", team)
    number_of_applicants_which_also_applied_to_another_team = 0
    _, ax3 = plt.subplots()
    applied_to_team_as_well = {}
    for applicant in applicant_applied_to_teams:
        for selected_teams in applicant:
            interested_in_teams = selected_teams.split(", ")
            if len(interested_in_teams) > 1:
                number_of_applicants_which_also_applied_to_another_team += 1
            for interested_in_team in interested_in_teams:
                applied_to_team_as_well[interested_in_team.strip()] = applied_to_team_as_well.get(
                    interested_in_team.strip(), 0) + 1 
    if team != "" and team in applied_to_team_as_well.keys():
        del applied_to_team_as_well[team]
        total_team_applicants = len(release_teams[team][GROUP_RETURNERS]) + \
            len(release_teams[team][GROUP_NEWCOMERS])
        logging.info("%s of %s also applied to one or more of the other teams", \
            number_of_applicants_which_also_applied_to_another_team, total_team_applicants)
        ax3.pie(applied_to_team_as_well.values(), labels=applied_to_team_as_well.keys(
        ), autopct=make_autopct(applied_to_team_as_well.values()))
        ax3.axis('equal')
        plt.style.use(THEME_MARPLOTLIB)
        plt.savefig(get_plot_file(
            f"applied-to-other-teams-{team.replace(' ', '').lower()}"))


def newcomers_and_returners(returners_df, newcomers_df, team=""):
    """filter newcomers and returners by team"""
    if team != "":
        team = f" for {team}"
    logging.info("Newcomer & Returner applicants %s", team)
    _, ax2 = plt.subplots()
    team_returners_and_newcomers = [len(returners_df), len(newcomers_df)]
    if team_returners_and_newcomers != [0, 0]:
        ax2.pie(team_returners_and_newcomers,
                labels=[GROUP_RETURNERS.capitalize(
                ), GROUP_NEWCOMERS.capitalize()],
                autopct=make_autopct(team_returners_and_newcomers)
                )
        ax2.axis('equal')
        plt.style.use(THEME_MARPLOTLIB)
        plt.savefig(get_plot_file(
            f"returners-and-newcomers{team.replace(' ', '').lower()}"))

@dataclass()
class EntityPlottingConfig:
    """EntityFilter defines data used to generate filtered plots"""
    entities_list: list[str]
    description: str = ""
    keywords: list[str] = None
    aliases: dict = None
    threshold: int = 1
    unreached_threshold_print: bool = False
    team: str = ""


def filter_entities(cfg: EntityPlottingConfig):
    """generic filter for entities"""
    if cfg.keywords is None:
        cfg.keywords = []
    if cfg.aliases is None:
        cfg.aliases = {}
    clean_entities = []
    for entity in cfg.entities_list:
        if entity is not None and isinstance(entity, str):
            entity = entity.lower()
            keyword_or_alias_found = False
            for keyword in cfg.keywords:
                if keyword in entity:
                    clean_entities.append(keyword)
                    keyword_or_alias_found = True
                    break
            if not keyword_or_alias_found:
                for alias, alias_repl in cfg.aliases.items():
                    if alias in entity:
                        clean_entities.append(alias_repl)
                        keyword_or_alias_found = True
                        break
            if not keyword_or_alias_found:
                clean_entities.append(entity)
    # count up entities
    affiliation_dict = Counter(clean_entities)
    affiliation_dict_threshold = {}
    if cfg.unreached_threshold_print:
        logging.info("Entities which do not reach threshold")
    for affiliation, count in affiliation_dict.items():
        if count > cfg.threshold:
            affiliation_dict_threshold[affiliation] = count
        elif cfg.unreached_threshold_print:
            logging.info("- %s", affiliation)
    # create chart
    logging.info("%s of applicants with a threshold of %s", cfg.description, cfg.threshold)
    _, ax6 = plt.subplots()
    ax6.pie(affiliation_dict_threshold.values(), labels=affiliation_dict_threshold.keys(
    ), autopct=make_autopct(affiliation_dict_threshold.values()))
    ax6.axis('equal')
    plt.style.use(THEME_MARPLOTLIB)
    plt.savefig(get_plot_file(
        f"entities-{cfg.description.replace(' ', '').lower()}{cfg.team.replace(' ', '').lower()}"))
