#
# This file contains logtic to generate markdown files of the applicants info which is nice to read
#

from __future__ import annotations
from io import TextIOWrapper
from vars import *
from dataclasses import dataclass


@dataclass(frozen=True, order=True)
class GeneralInfo:
    email: str
    name: str
    pronoun: str
    slack_handle: str
    github_handle: str
    affiliation: str

@dataclass(frozen=True, order=True)
class NewcomerInfo():
    general_info: str
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
class ReturnerInfo():
    general_info: str
    previous_roles: str
    previous_release_and_role: str
    interested_roles: str
    timezone: str
    can_volunteer_for_up_coming_cycles: str
    goals: str
    contribution_plans: str
    interested_in_stable_roster: str


def write_newcomer_applications_to_file(team, newcomerInfos: list[NewcomerInfo]):
    f = _new_application_file(team, group_newcomers)
    i = 1
    for newcomer in newcomerInfos:
        f.writelines("\n")
        _write_applicant_header(f, f"N{i}", team, newcomer.general_info)
        f.writelines(f"\n* **Timezone**: {newcomer.timezone}\n")
        f.writelines(f"* **Read handbook**: {newcomer.read_role_handbook}\n")
        f.writelines(
            f"* **Scheduled conflicts**: {newcomer.scheduled_conflicts}\n")

        f.writelines(f"\n**Why interested**:\n{newcomer.why_interested}\n")
        f.writelines(f"\n**Goals**:\n{newcomer.goals}\n")
        f.writelines(
            f"\n**Contribution plans**:\n{newcomer.contribution_plans}\n")
        f.writelines(f"\n**Comments**:\n{newcomer.comments}\n")
        f.writelines(
            f"\n**Relevant experience**:\n{newcomer.relevant_experience}\n")
        f.writelines(
            f"\n**Handbook feedback**:\n{newcomer.feedback_handbook}\n")

        f.writelines(
            f"\n**Experience contributing**:\n{newcomer.experience_contributing}\n")
        f.writelines(
            f"\n**Prior release teams**:\n{newcomer.prior_release_teams}\n")

        f.writelines(
            f"\n* **Timestimate to spare per week**: {newcomer.timeestimate_commit_to_releaseteam}\n")
        f.writelines(
            f"* **Able to attend release team meetings**: {newcomer.able_to_attend_release_team_meetings}\n")
        f.writelines(
            f"* **Able to attend burndown meetings**: {newcomer.able_to_attend_burndown_meetings}\n")
        f.writelines(
            f"* **Volunteer for upcoming cycles**: {newcomer.volunteer_for_upcoming_cycles}\n")
        f.writelines(
            f"* **Applied previously**: {newcomer.applied_previously}\n")

        f.writelines(f"\n* **K8s org member**: {newcomer.k8s_org_member}\n")
        f.writelines(f"* **Signed CLA**: {newcomer.signed_cla}\n")
        i += 1
    f.close()

# method used to write returner applicants to a local file


def write_returner_applications_to_file(team, returnerInfos: list[ReturnerInfo]):
    f = _new_application_file(team, group_returners)
    i = 1
    for returner in returnerInfos:
        f.writelines("\n")
        _write_applicant_header(f, f"R{i}", team, returner.general_info)
        f.writelines(f"\n* **Timezone**: {returner.timezone}\n")
        f.writelines(f"* **Previous Roles**: {returner.previous_roles}\n")
        f.writelines(
            f"* **Previous Release**: {returner.previous_release_and_role}\n")
        f.writelines(f"\n**Goals**:\n{returner.goals}\n")
        f.writelines(
            f"\n**Contribution plans**:\n{returner.contribution_plans}\n")
        f.writelines(
            f"\n* **Interest in stable rooster**: {returner.interested_in_stable_roster}\n")
        f.writelines(
            f"* **Can volunteer for up coming cycles**: {returner.can_volunteer_for_up_coming_cycles}\n")
        i += 1
    f.close()


# create a new file to store applicant information to
def _new_application_file(team: str, group: str) -> TextIOWrapper:
    application_file = open(get_applicants_file(team, group), "w+")
    application_file.writelines(
        f"# {group.capitalize()} applicant for team {team}\n")
    application_file.writelines("---\n")
    return application_file


def _write_applicant_header(f: TextIOWrapper, id: str, team: str, general_info: GeneralInfo):
    f.writelines(f"\n## {id} {general_info.name} for {team}\n")
    f.writelines(
        f"**Pronoun**: {general_info.pronoun}, **Slack** {general_info.slack_handle}, **GitHub** {general_info.github_handle}, **Affiliation**: {general_info.affiliation}, **Email**: {general_info.email}\n")
