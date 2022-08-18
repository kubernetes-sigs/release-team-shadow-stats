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
