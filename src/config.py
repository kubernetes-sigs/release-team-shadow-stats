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


from src.data_clean_up import CLEAN_KEYWORDS, CLEAN_ALIAS, CLEAN_THRESHOLD, CLEAN_SPLIT_INTO_KEYWORDS
from src.defaults import timezone_aliases, company_keywords, RELEASE_TEAM_TEAMS
from src.charts import BasicChart, plotting_count_entities_up
from src.summary import SummaryConfig

# INFO BasicChart:
# BasicChart("Title of the chart", "Opt out column name",
#   "Chart column", "Plotting function", "Clean up methods and config")

K8s_125 = "1.25"
K8s_126 = "1.26"

CHART_SCHEMA_DEFINITIONS = {
    K8s_125: [
        BasicChart("affiliation", ["Company Affiliation / Employer"],
                   plotting_count_entities_up,
                   {CLEAN_KEYWORDS: company_keywords, CLEAN_THRESHOLD: 2}),
        BasicChart("Timezone",
                   ["What time zone are you normally in?", "What time zone are you normally in?.1"],
                   plotting_count_entities_up, {CLEAN_ALIAS: timezone_aliases, CLEAN_THRESHOLD: 2}),
        BasicChart("Interested in Teams", ["Which Release Team roles are you interested in?",
                                           "Which Release Team roles are you interested for 1.25?"],
                   plotting_count_entities_up, {CLEAN_SPLIT_INTO_KEYWORDS: RELEASE_TEAM_TEAMS}),
        BasicChart("Previously served on the Kubernetes Release Team",
                   ["Have you previously served on a Kubernetes Release Team?"],
                   plotting_count_entities_up, {}),
        BasicChart("How often applied to the release team",
                   ["How many times have you applied to join the Release Team?"],
                   plotting_count_entities_up, {}),
        BasicChart("Release Team Roles Previously Served in",
                   ["Which Release Team roles have you served in?"],
                   plotting_count_entities_up, {CLEAN_SPLIT_INTO_KEYWORDS: RELEASE_TEAM_TEAMS, CLEAN_THRESHOLD: 2}),
        BasicChart("Able to attend Release Team meetings",
                   ["Will you be able to attend Release Team meetings? "],
                   plotting_count_entities_up, {CLEAN_THRESHOLD: 2}),
        BasicChart("Able to attend Burndown meetings",
                   ["Will you be able to attend Burndown meetings?"],
                   plotting_count_entities_up, {CLEAN_THRESHOLD: 2})
    ],
    K8s_126: []
}

# Info SummaryConfig:
# 1. returner_column_name: (str) which column is used to check if the applicant is a returner or newcomer?
#       This should be a "Yes" (I am a returner) / "No" (I am a newcomer) field
# 2. team_column_name: (list[str]) column used to specify which teams the applicant is interested in
# 3. deactivated_columns: (list[str]) which columns not to add to the summary file
# 4. column_rename: (dict[str, str]) which columns to rename to shorten the document and improve readability
# 5. teams: (list[str]) list of the teams that can be applied to
# 6. file_prefix: (str) prefix to write markdown files to

SUMMARY_CONFIGS = {
    K8s_125: SummaryConfig(
        # returner_column_name
        "Have you previously served on a Kubernetes Release Team?",
        # team_column_name
        ["Which Release Team roles are you interested in?",
         "Which Release Team roles are you interested for 1.25?"],
        # deactivated_columns
        ["Timestamp", "We would like to use your answers to produce anonymized reports about "
                      "shadow applicants. Do you consent to your answers being used in a "
                      "non-identifying way?"],
        # column_rename
        {"Goals.1": "Goals",
         "To help address everyone correctly, please share your pronouns if you're comfortable doing so. You can read "
         "more about pronoun sharing here https://www.mypronouns.org/sharing": "Pronouns",
         "Contribution Plans.1": "Contribution Plans",
         "Can you volunteer for 1.26 or 1.27?.1": "Can you volunteer for 1.26 or 1.27?",
         "What time zone are you normally in?": "Timezone",
         "What time zone are you normally in?.1": "Timezone",
         "How many times have you applied to join the Release Team?:": "Times applied before",
         "Have you read the role handbook associated with the role(s)?": "Read Handbook",
         "Have you previously served on a Kubernetes Release Team?": "Previously served on the RT",
         "How much time do you estimate you can commit to the Release Team a week? ": "Estimated Weekly Time commitment",
         "Why are you interested in that role(s)?": "Why interested?",
         "Will you be able to attend Release Team meetings? ": "Able to attend RT Meetings",
         "Will you be able to attend Burndown meetings?": "Able to attend Burndown Meetings",
         "Are you interested in joining a Release Team stable roster": "Interested in the RT stable roster",
         "How many times have you applied to join the Release Team?": "Times applied to join the RT",
         "Which Release Team roles are you interested for 1.25?": "Interested in Teams",
         "Which Release Team roles are you interested in?": "Interested in Teams"},
        # teams
        RELEASE_TEAM_TEAMS,
        # file_prefix
        "./applicants/"),
    K8s_126: None
}
