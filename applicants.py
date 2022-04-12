# Copyright 2022 The Kubernetes Authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

#
# This file contains logtic to generate markdown files of the applicants info which is nice to read
#

from __future__ import annotations
from io import TextIOWrapper
from dataclasses import dataclass, field
from abc import ABC
import string
from vars import *
from fake_data import *


class Applicants():
    def __init__(self, all: list[ApplicantData], returners: list[ApplicantData], newcomers: list[ApplicantData], applicants_by_team) -> None:
        # all applicant data
        self.all = all
        # subset: only applicant data from returner applicants
        self.returners = returners
        # subset: only applicant data from newcomer applicants
        self.newcomers = newcomers
        # subset map for each release-team sub-team
        self.applicants_by_team = applicants_by_team

    # def key_series_all(self, k) -> tuple(list[ReturnerApplicant], list[NewcomerApplicant]):
    #     returner_applicant_keys = []
    #     newcomer_applicant_keys = []

    #     for r in self.returners:
    #         returner_applicant_keys.append(r.)

    #     for n in self.returners:
    #         pass

    #     return returner_applicant_keys, newcomer_applicant_keys


@dataclass(order=True)
class ApplicantData:
    """ApplicantData wrapper for applicant dataclasses"""
    a_general_info: GeneralInfo
    a_specific_info: Applicant

    def __repr__(self) -> str:
        return f'{repr(self.a_general_info)}\n{repr(self.a_specific_info)}'


@dataclass(order=True)
class GeneralInfo:
    """GeneralInfo defines the data every applicants provides"""
    email: string = field(default_factory=fake_get_email)
    name: string = field(default_factory=fake_get_name)
    pronoun: string = field(default_factory=fake_get_pronoun)
    slack_handle: string = field(default_factory=fake_get_number_code)
    github_handle: string = field(default_factory=fake_get_number_code)
    affiliation: string = field(default_factory=fake_get_company)

    # This method can be called to set empty string instead of the defaults
    def clean(self) -> GeneralInfo:
        for key in vars(self):
            self.__dict__[key] = ""
        return self

    def __repr__(self) -> str:
        class_vars = {k: v for k, v in vars(self).items() if v is not None}
        s = ""
        for k in class_vars:
            s += f"**{k.replace('_', ' ').capitalize()}**: {class_vars[k]}, "
        # cut off ", " from the tail of the string
        return s[:-2]


class Applicant(ABC):
    """Applicant abstract class for a kind of applicant (newcomer & returner)"""


@dataclass(order=True)
class NewcomerApplicant(Applicant):
    """NewcomerApplicant implemented Applicant that defines the data newcomer applicants provides"""
    interested_roles: string = field(
        default_factory=fake_get_release_team_team)
    read_role_handbook: string = field(default_factory=fake_get_bool)
    why_interested: string = field(default_factory=fake_get_pargraph)
    feedback_handbook: string = field(default_factory=fake_get_pargraph)
    timeestimate_commit_to_releaseteam: string = field(
        default_factory=fake_get_pargraph)
    able_to_attend_release_team_meetings: string = field(
        default_factory=fake_get_bool)
    able_to_attend_burndown_meetings: string = field(
        default_factory=fake_get_bool)
    scheduled_conflicts: string = field(default_factory=fake_get_pargraph)
    volunteer_for_upcoming_cycles: string = field(default_factory=fake_get_bool)
    timezone: string = field(default_factory=fake_get_timezone)
    experience_contributing: string = field(default_factory=fake_get_pargraph)
    signed_cla: string = field(default_factory=fake_get_bool)
    k8s_org_member: string = field(default_factory=fake_get_bool)
    prior_release_teams: string = field(default_factory=fake_get_pargraph)
    relevant_experience: string = field(default_factory=fake_get_text)
    goals: string = field(default_factory=fake_get_text)
    contribution_plans: string = field(default_factory=fake_get_text)
    comments: string = field(default_factory=fake_get_pargraph)
    applied_previously: string = field(default_factory=fake_get_bool)

    # This method can be called to set empty string instead of the defaults
    def clean(self) -> NewcomerApplicant:
        for key in vars(self):
            self.__dict__[key] = ""
        return self

    def __repr__(self) -> str:
        class_vars = {k: v for k, v in vars(self).items() if v is not None}
        s = ""
        for k in class_vars:
            s += f"* **{k.replace('_', ' ').capitalize()}**: {class_vars[k]} \n"
        return s


@dataclass(order=True)
class ReturnerApplicant(Applicant):
    """ReturnerApplicant implemented Applicant that defines the data returner applicants provides"""
    previous_roles: string = field(default_factory=fake_get_release_team_team)
    previous_release_and_role: string = field(
        default_factory=fake_get_release_team_team)
    interested_roles: string = field(
        default_factory=fake_get_release_team_team)
    timezone: string = field(default_factory=fake_get_timezone)
    can_volunteer_for_up_coming_cycles: string = field(
        default_factory=fake_get_bool)
    goals: string = field(default_factory=fake_get_text)
    contribution_plans: string = field(default_factory=fake_get_text)
    interested_in_stable_roster: string = field(default_factory=fake_get_bool)

    # This method can be called to set empty string instead of the defaults
    def clean(self) -> ReturnerApplicant:
        for key in vars(self):
            self.__dict__[key] = ""
        return self

    def __repr__(self) -> str:
        class_vars = {k: v for k, v in vars(self).items() if v is not None}
        s = ""
        for k in class_vars:
            s += f"* **{k.replace('_', ' ').capitalize()}**: {class_vars[k]} \n"
        return s


def write_applications_to_file(team, group, applicant_data_list: list[ApplicantData]):
    """write_applications_to_file is used to generate markdown
    file from the above specified dataclasses for returners and newcomers"""
    file = _create_md_file(team, group)
    i = 1
    for d in applicant_data_list:
        # write header line
        file.writelines(
            f"\n\n\n## {group[0].capitalize()}{i} {d.a_general_info.name} for {team}\n\n")

        file.writelines(repr(d.a_general_info))
        file.writelines("\n")
        file.writelines(repr(d.a_specific_info))

        i += 1
    file.close()


def _create_md_file(team: str, group: str) -> TextIOWrapper:
    """create a new file to store applicant information to"""
    file = open(get_applicants_file(team, group), "w+")
    file.writelines(
        f"# {group.capitalize()} applicant for team {team}\n")
    file.writelines("---\n")
    return file


def create_dummy_applicants(n: int) -> Applicants:
    if n < 2:
        raise ValueError(
            f'invalid input: amount of dummy applicants {n} is too low')
    all_applicants, newcomer_applicants, returner_applicants = [], [], []
    for _ in range(0, n):
        new_applicant = ApplicantData(GeneralInfo(), NewcomerApplicant())
        all_applicants.append(new_applicant)
        newcomer_applicants.append(new_applicant)
    for _ in range(0, n):
        new_applicant = ApplicantData(GeneralInfo(), ReturnerApplicant())
        all_applicants.append(new_applicant)
        returner_applicants.append(new_applicant)

    applicants_by_team = {TEAM: {
        GROUP_NEWCOMERS: list(filter(lambda a: a.a_specific_info.interested_roles.__contains__(TEAM), newcomer_applicants)),
        GROUP_RETURNERS: list(filter(lambda a: a.a_specific_info.interested_roles.__contains__(TEAM), returner_applicants))
    } for TEAM in RELEASE_TEAM_TEAMS }

    return Applicants(all_applicants, returner_applicants, newcomer_applicants, applicants_by_team)


if __name__ == "__main__":
    applicants = create_dummy_applicants(10)
    print(repr(applicants.applicants_by_team[TEAM_CISIGNAL][GROUP_NEWCOMERS]))
        