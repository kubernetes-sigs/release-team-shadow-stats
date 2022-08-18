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


# INFO BasicChart:
# BasicChart("Title of the chart", "Opt out column name",
#   "Chart column", "Plotting function", "Clean up methods and config")

CHART_SCHEMA_DEFINITIONS = {
    "1.25": [
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
    "1.26": []
}
