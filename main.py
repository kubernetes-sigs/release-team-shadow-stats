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

import pandas as pd
import flag
from applicants import *
from plotting import *
from vars import *


class ApplicantDataframes():
    """ApplicantDataframes holds different kinds of subsets of the data"""

    def __init__(self, df_all, df_returners, df_newcomers, release_teams) -> None:
        # all applicant data
        self.df_all = df_all
        # subset: only applicant data from returner applicants
        self.df_returners = df_returners
        # subset: only applicant data from newcomer applicants
        self.df_newcomers = df_newcomers
        # subset map for each release-team sub-team
        self.release_teams = release_teams


def load_data(local_excel_f) -> ApplicantDataframes:
    """Use pandas to load the local excel file and generate a dataframe
    additionally filter create sub dataframes to reduce filtering simplify at usage
    """
    dataframe = pd.read_excel(local_excel_f)
    returners = dataframe[dataframe[SCHEMA_PREVIOUSLY_SERVED].str.contains(
        "Yes")]
    newcomers = dataframe[dataframe[SCHEMA_PREVIOUSLY_SERVED].str.contains(
        "No")]

    release_teams = {
        TEAM_BUGTRIAGE: {},
        TEAM_CISIGNAL: {},
        TEAM_COMMUNICATIONS: {},
        TEAM_RELEASE_NOTES: {},
        TEAM_DOCS: {},
        TEAM_ENHANCEMENTS: {}
    }

    for team in release_teams:
        team_applicants_returners = returners[
            returners[
                SCHEMA_RETURNERS_INTERESTED_IN_ROLES
            ].str.contains(team)
        ]
        team_applicants_newcomers = newcomers[
            newcomers[
                SCHEMA_NEWCOMERS_INTERESTED_IN_ROLES
            ].str.contains(team)
        ]
        release_teams[team] = {
            GROUP_RETURNERS: team_applicants_returners,
            GROUP_NEWCOMERS: team_applicants_newcomers
        }
    return ApplicantDataframes(dataframe, returners, newcomers, release_teams)


# Some general plotting
def general_plotting(a_df: ApplicantDataframes):
    """General sig release wide charts"""
    filter_entities(
        EntityPlottingConfig(
            entities_list=a_df.df_all[SCHEMA_NEWCOMERS_TIMEZONE].tolist(),
            description="Timezone",
            aliases=timezone_aliases,
            threshold=1,
            unreached_threshold_print=False
        )
    )
    logging.info("see timezones: https://24timezones.com/timezone-map")
    filter_entities(
        EntityPlottingConfig(
            entities_list=a_df.df_all[SCHEMA_AFFILIATION].tolist(),
            description="Affiliation",
            keywords=[
                "student",
                "liquid reply",
                "vmware",
                "microsoft",
                "red hat",
                "institute",
                "cisco",
                "ibm",
                "apple",
                "suse",
                "google",
                "independent",
                "deloitte",
                "adeste"
            ],
            aliases={
                "redhat": "red hat",
                "freelancer": "independent",
                "independant": "independent"
            }
        )
    )
    applicants_by_team(len(a_df.df_all), a_df.release_teams)
    pronouns_chart(a_df.df_all[SCHEMA_PRONOUNS])
    reapplying_newcomers(
        a_df.df_newcomers[SCHEMA_NEWCOMERS_APPLIED_PREVIOUSLY])
    newcomers_and_returners(a_df.df_returners, a_df.df_newcomers)


def team_plotting(a_df: ApplicantDataframes):
    """Team specific plotting"""
    for team in a_df.release_teams:
        newcomers_and_returners(
            a_df.release_teams[team][GROUP_RETURNERS],
            a_df.release_teams[team][GROUP_NEWCOMERS],
            team
        )
        applied_for_multiple_teams(
            [
                a_df.release_teams[team][GROUP_NEWCOMERS][SCHEMA_NEWCOMERS_INTERESTED_IN_ROLES],
                a_df.release_teams[team][GROUP_RETURNERS][SCHEMA_RETURNERS_INTERESTED_IN_ROLES]
            ],
            team,
            a_df.release_teams
        )
        team_applicants_by_pronouns = a_df.release_teams[team][GROUP_NEWCOMERS][SCHEMA_PRONOUNS].tolist(
        ) + a_df.release_teams[team][GROUP_RETURNERS][SCHEMA_PRONOUNS].tolist()
        pronouns_chart(
            team_applicants_by_pronouns,
            team
        )
        team_applicants_by_timezone = a_df.release_teams[team][GROUP_NEWCOMERS][SCHEMA_NEWCOMERS_TIMEZONE].tolist(
        ) + a_df.release_teams[team][GROUP_RETURNERS][SCHEMA_RETURNERS_TIMEZONE].tolist()
        filter_entities(
            EntityPlottingConfig(
                entities_list=team_applicants_by_timezone,
                description="Timezone",
                aliases=timezone_aliases,
                threshold=1,
                unreached_threshold_print=False,
                team=team
            )
        )


# Create applicant markdown files

def _returner_applications(team, a_df: ApplicantDataframes):
    """Write returner applications to a markdown file"""
    team_returning_applicants = []
    indexes = a_df.release_teams[team][GROUP_RETURNERS].index
    returners = a_df.release_teams[team][GROUP_RETURNERS]
    for i in indexes:
        general_info = GeneralInfo(
            returners[SCHEMA_EMAIL][i],
            returners[SCHEMA_NAME][i],
            returners[SCHEMA_PRONOUNS][i],
            returners[SCHEMA_SLACK][i],
            returners[SCHEMA_GITHUB][i],
            returners[SCHEMA_AFFILIATION][i]
        )
        returner_info = ReturnerApplicant(
            returners[SCHEMA_RETURNERS_PREVIOUS_ROLES][i],
            returners[SCHEMA_RETURNERS_PREVIOUS_RELEASE_AND_ROLE][i],
            returners[SCHEMA_RETURNERS_INTERESTED_IN_ROLES][i],
            returners[SCHEMA_RETURNERS_TIMEZONE][i],
            returners[SCHEMA_RETURNERS_CAN_VOLUNTEER_FOR_UP_COMING_CYCLES][i],
            returners[SCHEMA_RETURNERS_GOALS][i],
            returners[SCHEMA_RETURNERS_CONTRIBUTION_PLANS][i],
            returners[SCHEMA_RETURNERS_INTERESTED_IN_STABLE_ROSTER][i]
        )
        team_returning_applicants.append(
            ApplicantData(general_info, returner_info))
    write_applications_to_file(
        team, GROUP_RETURNERS, team_returning_applicants)


def _newcomer_applications(team, a_df: ApplicantDataframes):
    """Write newcomer applications to a markdown file"""
    team_newcomer_applicants = []
    indexes = a_df.release_teams[team][GROUP_NEWCOMERS].index
    newcomer = a_df.release_teams[team][GROUP_NEWCOMERS]
    for i in indexes:
        general_info = GeneralInfo(
            newcomer[SCHEMA_EMAIL][i],
            newcomer[SCHEMA_NAME][i],
            newcomer[SCHEMA_PRONOUNS][i],
            newcomer[SCHEMA_SLACK][i],
            newcomer[SCHEMA_GITHUB][i],
            newcomer[SCHEMA_AFFILIATION][i]
        )
        newcomer_info = NewcomerApplicant(
            interested_roles=newcomer[SCHEMA_NEWCOMERS_INTERESTED_IN_ROLES][i],
            read_role_handbook=newcomer[SCHEMA_NEWCOMERS_READ_HANDBOOK][i],
            why_interested=newcomer[SCHEMA_NEWCOMERS_WHY_INTERESTED][i],
            feedback_handbook=newcomer[SCHEMA_NEWCOMERS_HANDBOOK_QUESTIONS][i],
            timeestimate_commit_to_releaseteam=newcomer[
                SCHEMA_NEWCOMERS_TIMESTIMATE][i],
            able_to_attend_release_team_meetings=newcomer[
                SCHEMA_NEWCOMERS_ATTEND_RELEASE_TEAM_MEETINGS][i],
            able_to_attend_burndown_meetings=newcomer[
                SCHEMA_NEWCOMERS_ATTEND_BURNDOWN_MEETINGS][i],
            scheduled_conflicts=newcomer[SCHEMA_NEWCOMERS_SCHEDULED_CONFLICTS][i],
            volunteer_for_upcoming_cycles=newcomer[
                SCHEMA_NEWCOMERS_VOLUNTEER_UPCOMING_RELEASE][i],
            timezone=newcomer[SCHEMA_NEWCOMERS_TIMEZONE][i],
            experience_contributing=newcomer[SCHEMA_NEWCOMERS_EXPERIENCE_CONTRIBUTING][i],
            signed_cla=newcomer[SCHEMA_NEWCOMERS_SIGNED_CLA][i],
            k8s_org_member=newcomer[SCHEMA_NEWCOMERS_K8S_ORG_MEMBER][i],
            prior_release_teams=newcomer[SCHEMA_NEWCOMERS_PRIOR_RELEASE_TEAMS][i],
            relevant_experience=newcomer[SCHEMA_NEWCOMERS_RELEVANT_EXPERIENCE][i],
            goals=newcomer[SCHEMA_NEWCOMERS_GOALS][i],
            contribution_plans=newcomer[SCHEMA_NEWCOMERS_CONTRIBUTION_PLANS][i],
            comments=newcomer[SCHEMA_NEWCOMERS_COMMENTS][i],
            applied_previously=newcomer[SCHEMA_NEWCOMERS_APPLIED_PREVIOUSLY][i]
        )
        team_newcomer_applicants.append(
            ApplicantData(general_info, newcomer_info)
        )
    write_applications_to_file(team, GROUP_NEWCOMERS, team_newcomer_applicants)


def generate_application_summaries(a_df: ApplicantDataframes):
    """generate applicantion summary markdown files"""
    for team in a_df.release_teams:
        _returner_applications(team, a_df)
        _newcomer_applications(team, a_df)


if __name__ == "__main__":
    # define flags
    local_excel_file = flag.string(
        "file", "application-release-team-1.24.xlsx", "Applicant data source xlsx file")
    set_verbose_logging = flag.int(
        "verbose", 0, "Activate verbose logging [0/1]")
    flag.parse()

    # set logging configuration
    switcher = {0: logging.WARNING, 1: logging.DEBUG}
    logging.basicConfig(level=switcher.get(
        set_verbose_logging.val(), logging.WARNING))

    # try to open the specified file
    try:
        applicantion_df = load_data(local_excel_f=local_excel_file.val())
    except Exception as e:
        logging.error(e)

    # create plots / charts
    general_plotting(applicantion_df)
    team_plotting(applicantion_df)

    # generate applicantion summary markdown files
    generate_application_summaries(applicantion_df)
