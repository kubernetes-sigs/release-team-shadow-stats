# Copyright 2022 The Kubernetes Authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0xsx
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import polars
#
# This file contains logic to create dummy data which is used to present the application
# and its also used for testing.
#

from faker import Faker
from faker.providers import BaseProvider, company, python, lorem
import secrets

from src.charts import BasicChart, plotting_count_entities_up
from src.data_clean_up import CLEAN_KEYWORDS, CLEAN_SPLIT_INTO_KEYWORDS, CLEAN_THRESHOLD
from src.defaults import timezone_aliases, RELEASE_TEAM_TEAMS, company_keywords
from src.summary import SummaryConfig


# Timezone provider class
class TimezoneProvider(BaseProvider):
    def timezone(self) -> str:
        return secrets.choice(list(timezone_aliases.keys()))


# Yes/No provider class
class YesNoProvider(BaseProvider):
    def yes_no(self) -> str:
        return secrets.choice(["Yes", "No"])


# Company provider class
class CompanyProvider(BaseProvider):
    def company2(self) -> str:
        return secrets.choice(["Company-A", "Company-B", "Company-C", "Company-D", "Company-E", "Company-F"])


# Release Team provider class
class ReleaseTeamProvider(BaseProvider):
    def release_team(self) -> str:
        return secrets.choice(RELEASE_TEAM_TEAMS)


fake = Faker()
fake.add_provider(company)
fake.add_provider(python)
fake.add_provider(lorem)
fake.add_provider(TimezoneProvider)
fake.add_provider(ReleaseTeamProvider)
fake.add_provider(CompanyProvider)
fake.add_provider(YesNoProvider)


TESTING_SCHEMA_CHARTS = [
        BasicChart("Test Company", ["Company"],
                   plotting_count_entities_up,
                   {CLEAN_KEYWORDS: company_keywords, CLEAN_THRESHOLD: 2}),
        BasicChart("Test Timezone",
                   ["Timezone"],
                   plotting_count_entities_up, {CLEAN_THRESHOLD: 2}),
        BasicChart("Test Interested in Teams", ["Interested in roles"],
                   plotting_count_entities_up, {CLEAN_SPLIT_INTO_KEYWORDS: RELEASE_TEAM_TEAMS}),
        BasicChart("Test Previously served on the Kubernetes Release Team", ["Previously served"],
                   plotting_count_entities_up, {}),
        BasicChart("Test Times applied",
                   ["Times applied"], plotting_count_entities_up, {}),
        BasicChart("Test Previous Roles",
                   ["Previous role"],
                   plotting_count_entities_up, {CLEAN_SPLIT_INTO_KEYWORDS: RELEASE_TEAM_TEAMS, CLEAN_THRESHOLD: 2}),
        BasicChart("Test Able to attend Release Team meetings",
                   ["Attend Release Team Meetings"],
                   plotting_count_entities_up, {CLEAN_THRESHOLD: 2}),
        BasicChart("Test Able to attend Burndown meetings",
                   ["Attend Release Burndown Meetings"],
                   plotting_count_entities_up, {CLEAN_THRESHOLD: 2})
    ]


TESTING_SCHEMA_SUMMARY = SummaryConfig(
        # returner_column_name
        "Previously served",
        # team_column_name
        ["Interested in roles",
         "Interested in roles.1"],
        # deactivated_columns
        [],
        # column_rename
        {"Goals.1": "Goals"},
        # teams
        RELEASE_TEAM_TEAMS,
        # file_prefix
        "./applicants/test-")


def get_dataframe_random(records: int = 100) -> polars.DataFrame:
    data = {
        "Email Address": [f"{i}@example.com" for i in range(records)],
        "Name": [_fake_get_name() for _ in range(records)],
        "Pronouns": ["others" for _ in range(records)],
        "GitHub": [_fake_get_number_code() for _ in range(records)],
        "Slack": [_fake_get_number_code() for _ in range(records)],
        "Company": [_fake_get_company() for _ in range(records)],
        "Data processing": ["Yes" for _ in range(records)],
        "Times applied": [secrets.choice(["This is my first time", "Once before",
                                          "Twice before", "Three or more times before",
                                          "It's complicated"]) for _ in range(records)],
        "Previously served": [_fake_get_bool() for _ in range(records)],
        "Served in roles": [_fake_get_release_team_team() for _ in range(records)],
        "Previous role": [_fake_get_release_team_team() for _ in range(records)],
        "Interested in roles": [_fake_get_release_team_team() for _ in range(records)],
        "Volunteer for next Cycles": [secrets.choice(["Yes", "No", "Maybe"]) for _ in range(records)],
        "Stable Roster": [_fake_get_bool() for _ in range(records)],
        "Goals": [_fake_get_text() for _ in range(records)],
        "Contribution Plans": [_fake_get_text() for _ in range(records)],
        "Interested in roles.1": [_fake_get_release_team_team() for _ in range(records)],
        "Read the Handbook": [_fake_get_bool() for _ in range(records)],
        "Why interested": [_fake_get_paragraph() for _ in range(records)],
        "Handbook Feedback": [_fake_get_paragraph() for _ in range(records)],
        "Time spare for the release team": [_fake_get_paragraph() for _ in range(records)],
        "Attend Release Team Meetings": [secrets.choice(["Yes, most of them", "Some, but not all of them",
                                                         "I will not be abe to attend the meetings if they fall during my work hours",
                                                         "I cannot attend these meetings for some other reason"]) for _
                                         in range(records)],
        "Attend Release Burndown Meetings": [secrets.choice(["Yes, most of them", "Some, but not all of them",
                                                             "I will not be abe to attend the meetings if they fall during my work hours",
                                                             "I cannot attend these meetings for some other reason"])
                                             for _ in range(records)],
        "Scheduled conflict": [_fake_get_paragraph() for _ in range(records)],
        "Volunteer for next cycles": [secrets.choice(["Yes", "No", "Maybe"]) for _ in range(records)],
        "Timezone": [_fake_get_timezone() for _ in range(records)],
        "Experience contributing": [_fake_get_paragraph() for _ in range(records)],
        "Signed CLA": [_fake_get_bool() for _ in range(records)],
        "K8s Org Member": [_fake_get_bool() for _ in range(records)],
        "Relevant Experience": [_fake_get_paragraph() for _ in range(records)],
        "Goals.1": [_fake_get_text() for _ in range(records)],
        "Contribution plans": [_fake_get_paragraph() for _ in range(records)],
        "Comments": [_fake_get_paragraph() for _ in range(records)],
    }
    return polars.DataFrame(data)


def _fake_get_name() -> str:
    return fake.name()


def _fake_get_email() -> str:
    return f'{fake.ssn()}@example.com'


def _fake_get_paragraph() -> str:
    return fake.paragraph(nb_sentences=1)


def _fake_get_bool() -> str:
    return fake.yes_no()


def _fake_get_company() -> str:
    return fake.company2()


def _fake_get_text() -> str:
    return fake.paragraph(nb_sentences=4)


def _fake_get_timezone() -> str:
    return fake.timezone()


def _fake_get_number_code() -> str:
    return fake.ssn()


def _fake_get_release_team_team() -> str:
    return fake.release_team()
