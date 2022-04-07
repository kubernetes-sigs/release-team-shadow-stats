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
from vars import *
from fake_data import *

class Applicants():
    def __init__(self, all: list[Applicant], returners: list[ReturnerApplicant], newcomers: list[ReturnerApplicant], applicants_by_team) -> None:
        # all applicant data
        self.all = all
        # subset: only applicant data from returner applicants
        self.returners = returners
        # subset: only applicant data from newcomer applicants
        self.newcomers = newcomers
        # subset map for each release-team sub-team
        self.applicants_by_team = applicants_by_team

    def key_series_all(self, k) -> tuple(list[ReturnerApplicant], list[NewcomerApplicant]):
        returner_applicant_keys = []
        newcomer_applicant_keys = []

        for r in self.returners:
            pass

        return returner_applicant_keys, newcomer_applicant_keys

@dataclass(order=True)
class ApplicantData:
    """ApplicantData wrapper for applicant dataclasses"""
    general_info: GeneralInfo
    applicant: Applicant

    def __repr__(self) -> str:
        return f'{repr(self.general_info)}\n{repr(self.applicant)}'


@dataclass(order=True)
class GeneralInfo:
    """GeneralInfo defines the data every applicants provides"""
    email: str = field(default_factory=fake_get_email)
    name: str = field(default_factory=fake_get_name)
    pronoun: str = field(default_factory=fake_get_pronoun)
    slack_handle: str = field(default_factory=fake_get_number_code)
    github_handle: str = field(default_factory=fake_get_number_code)
    affiliation: str = field(default_factory=fake_get_company)

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
    interested_roles: str = field(
        default_factory=fake_get_release_team_team)
    read_role_handbook: str = field(default_factory=fake_get_bool)
    why_interested: str = field(default_factory=fake_get_pargraph)
    feedback_handbook: str = field(default_factory=fake_get_pargraph)
    timeestimate_commit_to_releaseteam: str = field(
        default_factory=fake_get_pargraph)
    able_to_attend_release_team_meetings: str = field(
        default_factory=fake_get_bool)
    able_to_attend_burndown_meetings: str = field(
        default_factory=fake_get_bool)
    scheduled_conflicts: str = field(default_factory=fake_get_pargraph)
    volunteer_for_upcoming_cycles: str = field(default_factory=fake_get_bool)
    timezone: str = field(default_factory=fake_get_timezone)
    experience_contributing: str = field(default_factory=fake_get_pargraph)
    signed_cla: str = field(default_factory=fake_get_bool)
    k8s_org_member: str = field(default_factory=fake_get_bool)
    prior_release_teams: str = field(default_factory=fake_get_pargraph)
    relevant_experience: str = field(default_factory=fake_get_text)
    goals: str = field(default_factory=fake_get_text)
    contribution_plans: str = field(default_factory=fake_get_text)
    comments: str = field(default_factory=fake_get_pargraph)
    applied_previously: str = field(default_factory=fake_get_bool)
    
    # This method can be called to set empty string instead of the defaults 
    def clean(self) -> NewcomerApplicant:
        for key in vars(self):
            self.__dict__[key] = ""
        return self

    def __repr__(self) -> str:
        class_vars = {k: v for k, v in vars(self).items() if v is not None}
        s = ""
        for k in class_vars:
            s += f"**{k.replace('_', ' ').capitalize()}**: {class_vars[k]} \n"
        return s

@dataclass(order=True)
class ReturnerApplicant(Applicant):
    """ReturnerApplicant implemented Applicant that defines the data returner applicants provides"""
    previous_roles: str = field(default_factory=fake_get_release_team_team)
    previous_release_and_role: str = field(
        default_factory=fake_get_release_team_team)
    interested_roles: str = field(
        default_factory=fake_get_release_team_team)
    timezone: str = field(default_factory=fake_get_timezone)
    can_volunteer_for_up_coming_cycles: str = field(
        default_factory=fake_get_bool)
    goals: str = field(default_factory=fake_get_text)
    contribution_plans: str = field(default_factory=fake_get_text)
    interested_in_stable_roster: str = field(default_factory=fake_get_bool)

    # This method can be called to set empty string instead of the defaults 
    def clean(self) -> ReturnerApplicant:
        for key in vars(self):
            self.__dict__[key] = ""
        return self

    def __repr__(self) -> str:
        class_vars = {k: v for k, v in vars(self).items() if v is not None}
        s = ""
        for k in class_vars:
            s += f"**{k.replace('_', ' ').capitalize()}**: {class_vars[k]} \n"
        return s


def write_applications_to_file(team, group, applicant_data_list: list[ApplicantData]):
    """write_applications_to_file is used to generate markdown
    file from the above specified dataclasses for returners and newcomers"""
    file = _create_md_file(team, group)
    i = 1
    for d in applicant_data_list:
        # write header line
        file.writelines(
            f"\n\n\n## {group[0].capitalize()}{i} {d.general_info.name} for {team}\n\n")

        file.writelines(repr(d.general_info))
        file.writelines("\n")
        file.writelines(repr(d.applicant))

        i += 1
    file.close()


def _create_md_file(team: str, group: str) -> TextIOWrapper:
    """create a new file to store applicant information to"""
    file = open(get_applicants_file(team, group), "w+")
    file.writelines(
        f"# {group.capitalize()} applicant for team {team}\n")
    file.writelines("---\n")
    return file



if __name__ == "__main__":
    print(repr(GeneralInfo()))
    print("\n\n\n")
    print(repr(NewcomerApplicant()))
    print("\n\n\n")
    print(repr(ReturnerApplicant()))