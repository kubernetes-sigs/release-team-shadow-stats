#
# This file contains logtic to generate markdown files of the applicants info which is nice to read
#

from __future__ import annotations
from io import TextIOWrapper
from dataclasses import dataclass
from abc import ABC
from vars import *

@dataclass(frozen=True, order=True)
class ApplicantData:
    """ApplicantData wrapper for applicant dataclasses"""
    general_info: GeneralInfo
    applicant: Applicant

@dataclass(frozen=True, order=True)
class GeneralInfo:
    """GeneralInfo defines the data every applicants provides"""
    email: str
    name: str
    pronoun: str
    slack_handle: str
    github_handle: str
    affiliation: str
class Applicant(ABC):
    """Applicant abstract class for a kind of applicant (newcomer & returner)"""

@dataclass(frozen=True, order=True)
class NewcomerApplicant(Applicant):
    """NewcomerApplicant implemented Applicant that defines the data newcomer applicants provides"""
    interested_roles: str
    read_role_handbook: str
    why_interested: str
    feedback_handbook: str
    timeestimate_commit_to_releaseteam: str
    able_to_attend_release_team_meetings: str
    able_to_attend_burndown_meetings: str
    scheduled_conflicts: str
    volunteer_for_upcoming_cycles: str
    timezone: str
    experience_contributing: str
    signed_cla: str
    k8s_org_member: str
    prior_release_teams: str
    relevant_experience: str
    goals: str
    contribution_plans: str
    comments: str
    applied_previously: str


@dataclass(frozen=True, order=True)
class ReturnerApplicant(Applicant):
    """ReturnerApplicant implemented Applicant that defines the data returner applicants provides"""
    previous_roles: str
    previous_release_and_role: str
    interested_roles: str
    timezone: str
    can_volunteer_for_up_coming_cycles: str
    goals: str
    contribution_plans: str
    interested_in_stable_roster: str


def write_applications_to_file(team, group, applicant_data_list: list[ApplicantData]):
    """write_applications_to_file is used to generate markdown
    file from the above specified dataclasses for returners and newcomers"""
    file = _create_md_file(team, group)
    i = 1
    for d in applicant_data_list:
        # write header line
        file.writelines(
            f"\n\n\n## {group[0].capitalize()}{i} {d.general_info.name} for {team}\n\n")

        # write general information (see dataclass)
        general_vars = {k: v for k, v in vars(
            d.general_info).items() if v is not None}
        for g_key in general_vars:
            file.writelines(
                f"**{g_key.replace('_', ' ').capitalize()}**: {general_vars[g_key]} - ")
        file.writelines("\n")

        # write applicant information (see dataclass newcomer / returner)
        applicant_vars = {k: v for k, v in vars(
            d.applicant).items() if v is not None}
        for a_key in applicant_vars:
            file.writelines(
                f"* **{a_key.replace('_', ' ').capitalize()}**: {applicant_vars[a_key]}\n")
        i += 1
    file.close()


def _create_md_file(team: str, group: str) -> TextIOWrapper:
    """create a new file to store applicant information to"""
    file = open(get_applicants_file(team, group), "w+")
    file.writelines(
        f"# {group.capitalize()} applicant for team {team}\n")
    file.writelines("---\n")
    return file
