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

import flag
from applicants import *
from plotting import *
from load_data import *
from vars import *


# Some general plotting
def create_general_plotting(a: Applicants):
    """General release team plotting (/charts)"""
    # Timezones
    applicant_timezones = [x.a_specific_info.timezone for x in a.returners] + \
        [x.a_specific_info.timezone for x in a.newcomers]
    filter_entities(
        EntityPlottingConfig(
            entities_list=applicant_timezones,
            description="Timezone",
            aliases=timezone_aliases,
            threshold=1,
            unreached_threshold_print=False
        )
    )
    logging.info("see timezones: https://24timezones.com/timezone-map")
    # Company / Affiliation
    applicant_affiliations = [x.a_general_info.affiliation for x in a.all]
    filter_entities(
        EntityPlottingConfig(
            entities_list=applicant_affiliations,
            description="Affiliation",
            keywords=company_keywords,
            aliases=company_aliases
        )
    )
    # Applicants by Release Team, team
    applicants_by_team(len(a.all), a.applicants_by_team)
    # Pronouns
    pronouns_chart([x.a_general_info.pronoun for x in a.all])
    # Newcomer that applied before but got rejected
    reapplying_newcomers(
        [x.a_specific_info.applied_previously for x in a.newcomers])
    # Ration Newcomers:Returners - returning release team members (returners) and first time release team members (newcomer)
    newcomers_and_returners(a.returners, a.newcomers)


def create_team_plotting(a: Applicants):
    """Release Team specific plotting
    the following charts are getting generated for each release team
    """
    for team in a.applicants_by_team:
        # Team applicants, newcomer:returner ratio
        newcomers_and_returners(
            a.applicants_by_team[team][GROUP_RETURNERS],
            a.applicants_by_team[team][GROUP_NEWCOMERS],
            team
        )
        team_applicants_by_pronouns = [x.a_general_info.pronoun for x in a.applicants_by_team[team][GROUP_NEWCOMERS]] + [
            x.a_general_info.pronoun for x in a.applicants_by_team[team][GROUP_RETURNERS]]
        pronouns_chart(
            team_applicants_by_pronouns,
            team
        )
        team_applicants_by_timezone = [x.a_specific_info.timezone for x in a.applicants_by_team[team][GROUP_NEWCOMERS]] + [
            x.a_specific_info.timezone for x in a.applicants_by_team[team][GROUP_RETURNERS]]
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
def create_application_summaries(a_df: Applicants):
    """Create markdown files with the applicantion information by team & splitted into returners and newcomers
    - ci-signal-returners-applicants.md
    - ci-signal-newcomer-applicants.md
    - ...
    """
    for team in a_df.applicants_by_team:
        write_applications_to_file(
            team, GROUP_NEWCOMERS, a_df.applicants_by_team[team][GROUP_NEWCOMERS])
        write_applications_to_file(
            team, GROUP_RETURNERS, a_df.applicants_by_team[team][GROUP_RETURNERS])


if __name__ == "__main__":
    # Flags
    test = flag.int(
        "test", 0, "Generate test files and don't read Excel file")
    local_excel_file = flag.string(
        "file", "application-release-team-1.24.xlsx", "Applicant data source xlsx file")
    set_verbose_logging = flag.int(
        "verbose", 0, "Activate verbose logging [0/1]")
    flag.parse()

    # Logging configuration
    switcher = {0: logging.WARNING, 1: logging.DEBUG}
    logging.basicConfig(level=switcher.get(
        set_verbose_logging.val(), logging.WARNING))

    data = None
    if test.val() == 0:
        try:
            data = load_data(local_excel_f=local_excel_file.val())
        except Exception as e:
            logging.error(e)
    else:
        # create dummy application data
        data = create_dummy_applicants(50)

    # create plots / charts
    create_general_plotting(data)
    create_team_plotting(data)

    # generate applicantion summary markdown files
    create_application_summaries(data)
