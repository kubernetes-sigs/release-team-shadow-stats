import pandas as pd
import flag
from applicants import *
from plotting import *
from vars import *


class ApplicantDataframes():
    """ApplicantDataframes holds different dataframes"""
    def __init__(self, dataframe, returners, newcomers, release_teams) -> None:
        self.df = dataframe
        self.returners = returners
        self.newcomers = newcomers
        self.release_teams = release_teams


def load_data(local_excel_f) -> ApplicantDataframes:
    """Use pandas to load the local excel file and generate a dataframe
    additionally filter create sub dataframes to reduce filtering simplify at usage
    """
    dataframe = pd.read_excel(local_excel_f)
    returners = dataframe[dataframe[SCHEMA_PREVIOUSLY_SERVED].str.contains("Yes")]
    newcomers = dataframe[dataframe[SCHEMA_PREVIOUSLY_SERVED].str.contains("No")]

    release_teams = {
        TEAM_BUGTRIAGE: {}, TEAM_CISIGNAL: {}, TEAM_COMMUNICATIONS: {}, TEAM_RELEASE_NOTES: {}, TEAM_DOCS: {}, TEAM_ENHANCEMENTS: {}
    }

    for team in release_teams:
        team_applicants_returners = returners[returners[SCHEMA_RETURNERS_INTERESTED_IN_ROLES].str.contains(
            team)]
        team_applicants_newcomers = newcomers[newcomers[SCHEMA_NEWCOMERS_INTERESTED_IN_ROLES].str.contains(
            team)]
        release_teams[team] = {
            GROUP_RETURNERS: team_applicants_returners,
            GROUP_NEWCOMERS: team_applicants_newcomers
        }
    return ApplicantDataframes(dataframe, returners, newcomers, release_teams)


# Some general plotting
def general_plotting(a_df: ApplicantDataframes):
    """General sig release wide charts"""
    filter_entities(a_df.newcomers[SCHEMA_NEWCOMERS_TIMEZONE].tolist() + a_df.returners[SCHEMA_RETURNERS_TIMEZONE].tolist(), "Timezone",
                    aliases=timezone_aliases,
                    threshold=1, unreached_threshold_print=False)
    print("see timezones: https://24timezones.com/timezone-map")
    filter_entities(a_df.df[SCHEMA_AFFILIATION].tolist(), "Affiliation",
                    keywords=["student", "liquid reply", "vmware", "microsoft", "red hat", "institute",
                              "cisco", "ibm", "apple", "suse", "google", "independant", "deloitte", "adeste"],
                    aliases={"redhat": "red hat", "freelancer": "independant"},
                    threshold=1)
    applicants_by_team(len(a_df.df), a_df.release_teams)
    pronouns_chart(a_df.df[SCHEMA_PRONOUNS])
    reapplying_newcomers(a_df.newcomers[SCHEMA_NEWCOMERS_APPLIED_PREVIOUSLY])
    newcomers_and_returners(a_df.returners, a_df.newcomers)


def team_plotting(a_df: ApplicantDataframes):
    """Team specific plotting"""
    for team in a_df.release_teams:
        newcomers_and_returners(
            a_df.release_teams[team][GROUP_RETURNERS], a_df.release_teams[team][GROUP_NEWCOMERS], team)
        applied_for_multiple_teams([a_df.release_teams[team][GROUP_NEWCOMERS][SCHEMA_NEWCOMERS_INTERESTED_IN_ROLES],
                                    a_df.release_teams[team][GROUP_RETURNERS][SCHEMA_RETURNERS_INTERESTED_IN_ROLES]], team, a_df.release_teams)
        pronouns_chart(a_df.release_teams[team][GROUP_NEWCOMERS][SCHEMA_PRONOUNS].tolist(
        ) + a_df.release_teams[team][GROUP_RETURNERS][SCHEMA_PRONOUNS].tolist(), team)
        filter_entities(a_df.release_teams[team][GROUP_NEWCOMERS][SCHEMA_NEWCOMERS_TIMEZONE].tolist() + a_df.release_teams[team][GROUP_RETURNERS][SCHEMA_RETURNERS_TIMEZONE].tolist(), "Timezone",
                        aliases=timezone_aliases,
                        threshold=1, unreached_threshold_print=False, team=team)


# Create applicant markdown files

def _returner_applications(team, a_df: ApplicantDataframes):
    """Write returner applications to a markdown file"""
    team_returning_applicants = []
    indexes = a_df.release_teams[team][GROUP_RETURNERS].index
    returners = a_df.release_teams[team][GROUP_RETURNERS]
    for i in indexes:
        general_info = GeneralInfo(returners[SCHEMA_EMAIL][i],
                         returners[SCHEMA_NAME][i],
                         returners[SCHEMA_PRONOUNS][i],
                         returners[SCHEMA_SLACK][i],
                         returners[SCHEMA_GITHUB][i],
                         returners[SCHEMA_AFFILIATION][i])
        returner_info = ReturnerInfo(returners[SCHEMA_RETURNERS_PREVIOUS_ROLES][i],
                          returners[SCHEMA_RETURNERS_PREVIOUS_RELEASE_AND_ROLE][i],
                          returners[SCHEMA_RETURNERS_INTERESTED_IN_ROLES][i],
                          returners[SCHEMA_RETURNERS_TIMEZONE][i],
                          returners[SCHEMA_RETURNERS_CAN_VOLUNTEER_FOR_UP_COMING_CYCLES][i],
                          returners[SCHEMA_RETURNERS_GOALS][i],
                          returners[SCHEMA_RETURNERS_CONTRIBUTION_PLANS][i],
                          returners[SCHEMA_RETURNERS_INTERESTED_IN_STABLE_ROSTER][i])
        team_returning_applicants.append(ApplicantData(general_info, returner_info))
    write_applications_to_file(
        team, GROUP_RETURNERS, team_returning_applicants)


def _newcomer_applications(team, a_df: ApplicantDataframes):
    """Write newcomer applications to a markdown file"""
    team_newcomer_applicants = []
    indexes = a_df.release_teams[team][GROUP_NEWCOMERS].index
    newcomer = a_df.release_teams[team][GROUP_NEWCOMERS]
    for i in indexes:
        general_info = GeneralInfo(newcomer[SCHEMA_EMAIL][i],
                         newcomer[SCHEMA_NAME][i],
                         newcomer[SCHEMA_PRONOUNS][i],
                         newcomer[SCHEMA_SLACK][i],
                         newcomer[SCHEMA_GITHUB][i],
                         newcomer[SCHEMA_AFFILIATION][i])
        newcomer_info = NewcomerInfo(interested_roles=newcomer[SCHEMA_NEWCOMERS_INTERESTED_IN_ROLES][i],
                          read_role_handbook=newcomer[SCHEMA_NEWCOMERS_READ_HANDBOOK][i],
                          why_interested=newcomer[SCHEMA_NEWCOMERS_WHY_INTERESTED][i],
                          feedback_handbook=newcomer[SCHEMA_NEWCOMERS_HANDBOOK_QUESTIONS][i],
                          timeestimate_commit_to_releaseteam=newcomer[SCHEMA_NEWCOMERS_TIMESTIMATE][i],
                          able_to_attend_release_team_meetings=newcomer[SCHEMA_NEWCOMERS_ATTEND_RELEASE_TEAM_MEETINGS][i],
                          able_to_attend_burndown_meetings=newcomer[SCHEMA_NEWCOMERS_ATTEND_BURNDOWN_MEETINGS][i],
                          scheduled_conflicts=newcomer[SCHEMA_NEWCOMERS_SCHEDULED_CONFLICTS][i],
                          volunteer_for_upcoming_cycles=newcomer[SCHEMA_NEWCOMERS_VOLUNTEER_UPCOMING_RELEASE][i],
                          timezone=newcomer[SCHEMA_NEWCOMERS_TIMEZONE][i],
                          experience_contributing=newcomer[SCHEMA_NEWCOMERS_EXPERIENCE_CONTRIBUTING][i],
                          signed_cla=newcomer[SCHEMA_NEWCOMERS_SIGNED_CLA][i],
                          k8s_org_member=newcomer[SCHEMA_NEWCOMERS_K8S_ORG_MEMBER][i],
                          prior_release_teams=newcomer[SCHEMA_NEWCOMERS_PRIOR_RELEASE_TEAMS][i],
                          relevant_experience=newcomer[SCHEMA_NEWCOMERS_RELEVANT_EXPERIENCE][i],
                          goals=newcomer[SCHEMA_NEWCOMERS_GOALS][i],
                          contribution_plans=newcomer[SCHEMA_NEWCOMERS_CONTRIBUTION_PLANS][i],
                          comments=newcomer[SCHEMA_NEWCOMERS_COMMENTS][i],
                          applied_previously=newcomer[SCHEMA_NEWCOMERS_APPLIED_PREVIOUSLY][i])
        team_newcomer_applicants.append(ApplicantData(general_info, newcomer_info))
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
    flag.parse()

    # try to open the specified file
    try:
        applicantionDf = load_data(local_excel_f=local_excel_file.val())
    except Exception as e:
        print(e)

    # create plots / charts
    general_plotting(applicantionDf)
    team_plotting(applicantionDf)

    # generate applicantion summary markdown files
    generate_application_summaries(applicantionDf)
