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

"""Constants and functions to processing applicant data and define conventions"""

# dataframe
GROUP_RETURNERS = "returners"
GROUP_NEWCOMERS = "newcomers"

# Release team sub team names
TEAM_BUGTRIAGE = "Bug Triage"
TEAM_CISIGNAL = "CI Signal"
TEAM_COMMUNICATIONS = "Communications"
TEAM_RELEASE_NOTES = "Release Notes"
TEAM_DOCS = "Documentation"
TEAM_ENHANCEMENTS = "Enhancements"

RELEASE_TEAM_TEAMS = [TEAM_BUGTRIAGE, TEAM_CISIGNAL,
                      TEAM_COMMUNICATIONS, TEAM_RELEASE_NOTES, TEAM_DOCS, TEAM_ENHANCEMENTS]

# Folders
APPLICANTS_FOLDER = "applicants"
PLOT_FOLDER = "plots"

# Themes
THEME_MARPLOTLIB = 'ggplot'


def get_applicants_file(team_name, group):
    """function to define how to format markdown file names"""
    return f"./{APPLICANTS_FOLDER}/{team_name}-{group}.md"


def get_plot_file(filename):
    """function to define how to format plot file names"""
    return f"./{PLOT_FOLDER}/{filename}.png"


company_keywords = [
    "student",
    "liquid reply",
    "vmware",
    "microsoft",
    "red hat",
    "cisco",
    "ibm",
    "apple",
    "suse",
    "google",
    "independent",
    "deloitte",
    "adeste"
]

company_aliases = {
    "redhat": "red hat",
    "freelancer": "independent",
    "independant": "independent"
}

timezone_aliases = {
    "gmt": "london gmt+0", "paris": "london gmt+0", "london": "london gmt+0",
    "middle europe": "central europe gmt+1", "cet": "central europe gmt+1",
    "+ 1": "central europe gmt+1", "central time": "central europe gmt+1",
    "central european time": "central europe gmt+1", "berlin":
        "central europe gmt+1", "+1": "central europe gmt+1",
    "ist": "india gmt+5", "+5": "india gmt+5", "+ 5": "india gmt+5",
    "india": "india gmt+5", "indian": "india gmt+5", "+ 6": "india gmt+5",
    "pst": "us pacific gmt-8", "pdt": "us pacific gmt-8",
    "pacific": "us pacific gmt-8", "pacific time": "us pacific gmt-8",
    "edt": "us east gmt-5", "eastern time": "us east gmt-5",
    "us east": "us east gmt-5", "est": "us east gmt-5",
    "+4": "iran gmt+4",
    "+2": "east europe gmt+2", "eastern europe": "east europe gmt+2",
    "eastern standard time": "east europe gmt+2",
    "+3": "arabia gmt+3",
    "+9": "japan gmt+9", "jst": "japan gmt+9",
    "+8": "china gmt+8", "shanghai": "china gmt+8",
    "utc": "london gmt+0"
}

pronouns = ["he/they", "he/him", "she/her", "she/they",
            "they/them", "ze", "neopronouns", "other"]

# Schema variables reference column headers of the applicant excel file TODO: dynamic schema
RELEASE_VERSION = "1.24"

# General applicant infos
SCHEMA_EMAIL = "Email Address"
SCHEMA_NAME = "Name"
SCHEMA_PRONOUNS = "To help address everyone correctly, please share your pronouns if you're comfortable doing so. You" \
                  " can more about pronoun sharing here https://www.mypronouns.org/sharing "
SCHEMA_SLACK = "Slack Handle"
SCHEMA_GITHUB = "Github Handle"
SCHEMA_AFFILIATION = "Company Affiliation / Employer"
SCHEMA_PREVIOUSLY_SERVED = "Have you previously served on a Kubernetes Release Team?"

# Returners infos
SCHEMA_RETURNERS_PREVIOUS_ROLES = "Which release team roles have you served in?"
SCHEMA_RETURNERS_PREVIOUS_RELEASE_AND_ROLE = "Please tell us which release team(s) you were previously on and what " \
                                             "role you held (i.e. Lead or Shadow) "
SCHEMA_RETURNERS_INTERESTED_IN_ROLES = f"What release team roles are you interested in for {RELEASE_VERSION}?"
SCHEMA_RETURNERS_CAN_VOLUNTEER_FOR_UP_COMING_CYCLES = "Can you volunteer for 1.25 or 1.26?"
SCHEMA_RETURNERS_TIMEZONE = "What time zone are you normally in?"
SCHEMA_RETURNERS_GOALS = "Goals"
SCHEMA_RETURNERS_CONTRIBUTION_PLANS = "Contribution Plans"
SCHEMA_RETURNERS_INTERESTED_IN_STABLE_ROSTER = "Are you interested in joining a release team stable roster"

# Newcomers
SCHEMA_NEWCOMERS_INTERESTED_IN_ROLES = "Which release roles are you interested in?"
SCHEMA_NEWCOMERS_READ_HANDBOOK = "Have you read the role handbook associated with that role?"
SCHEMA_NEWCOMERS_WHY_INTERESTED = "Why are you interested in that role(s)?"
SCHEMA_NEWCOMERS_HANDBOOK_QUESTIONS = "Do you have other feedback or questions about the handbook?"
SCHEMA_NEWCOMERS_TIMESTIMATE = "How much time do you estimate you can commit to the Release Team a week? "
SCHEMA_NEWCOMERS_ATTEND_RELEASE_TEAM_MEETINGS = "Will you be able to attend Release Team meetings? "
SCHEMA_NEWCOMERS_ATTEND_BURNDOWN_MEETINGS = "Will you be able to attend Burndown meetings?"
SCHEMA_NEWCOMERS_SCHEDULED_CONFLICTS = "Do you have schedule conflicts?"
SCHEMA_NEWCOMERS_VOLUNTEER_UPCOMING_RELEASE = f"{SCHEMA_RETURNERS_CAN_VOLUNTEER_FOR_UP_COMING_CYCLES}.1"
SCHEMA_NEWCOMERS_TIMEZONE = f"{SCHEMA_RETURNERS_TIMEZONE}.1"
SCHEMA_NEWCOMERS_EXPERIENCE_CONTRIBUTING = "What is your experience contributing?"
SCHEMA_NEWCOMERS_SIGNED_CLA = "Have you signed the CLA?"
SCHEMA_NEWCOMERS_K8S_ORG_MEMBER = "Are you a Kubernetes Org Member?"
SCHEMA_NEWCOMERS_PRIOR_RELEASE_TEAMS = "Prior Release Teams"
SCHEMA_NEWCOMERS_RELEVANT_EXPERIENCE = "Relevant Experience"
SCHEMA_NEWCOMERS_GOALS = f"{SCHEMA_RETURNERS_GOALS}.1"
SCHEMA_NEWCOMERS_CONTRIBUTION_PLANS = f"{SCHEMA_RETURNERS_CONTRIBUTION_PLANS}.1"
SCHEMA_NEWCOMERS_COMMENTS = "Comments"
SCHEMA_NEWCOMERS_APPLIED_PREVIOUSLY = "Have you applied to any previous Kubernetes release teams?"
