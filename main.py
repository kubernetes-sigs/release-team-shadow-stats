from applicants import *
from plotting import *
from vars import *
import pandas as pd
import flag


class ApplicantDataframes():
    def __init__(self, df, returners, newcomers, release_teams) -> None:
        self.df = df
        self.returners = returners
        self.newcomers = newcomers
        self.release_teams = release_teams


def load_data(local_excel_f) -> ApplicantDataframes:
    # Use pandas to load the local excel file and generate a dataframe
    df = pd.read_excel(local_excel_f)

    # Filter applicants by returning release team members and new applicants
    returners = df[df[schema_previously_served].str.contains("Yes")]
    newcomers = df[df[schema_previously_served].str.contains("No")]

    release_teams = {
        team_bugtriage: {}, team_cisignal: {}, team_communications: {}, team_releasenotes: {}, team_documentation: {}, team_enhancements: {}
    }

    for team in release_teams:
        teamApplicantsReturners = returners[returners[schema_returners_interested_in_roles].str.contains(
            team)]
        teamApplicantsNewcomers = newcomers[newcomers[schema_newcomers_interested_in_roles].str.contains(
            team)]
        release_teams[team] = {
            group_returners: teamApplicantsReturners,
            group_newcomers: teamApplicantsNewcomers
        }
    return ApplicantDataframes(df, returners, newcomers, release_teams)


# Some general plotting
def general_plotting(a: ApplicantDataframes):
    # General sig release wide charts
    filter_entities(a.newcomers[schema_newcomers_timezone].tolist() + a.returners[schema_returners_timezone].tolist(), "Timezone",
                    aliases=timezone_aliases,
                    threshold=1, unreached_threshold_print=False)
    print(f"see timezones: https://24timezones.com/timezone-map")
    filter_entities(a.df[schema_affiliation].tolist(), "Affiliation",
                    keywords=["student", "liquid reply", "vmware", "microsoft", "red hat", "institute",
                              "cisco", "ibm", "apple", "suse", "google", "independant", "deloitte", "adesso"],
                    aliases={"redhat": "red hat", "freelancer": "independant"},
                    threshold=1)
    applicants_by_team(len(a.df), a.release_teams)
    pronouns_chart(a.df[schema_pronouns])
    reapplying_newcomers(a.newcomers[schema_newcomers_applied_previously])
    newcomers_and_returners(a.returners, a.newcomers)


# Team specific plotting
def team_plotting(a: ApplicantDataframes):
    for team in a.release_teams:
        print(f"\n\n{team}")
        newcomers_and_returners(
            a.release_teams[team][group_returners], a.release_teams[team][group_newcomers], team)
        applied_for_multiple_teams([a.release_teams[team][group_newcomers][schema_newcomers_interested_in_roles],
                                    a.release_teams[team][group_returners][schema_returners_interested_in_roles]], team, a.release_teams)
        pronouns_chart(a.release_teams[team][group_newcomers][schema_pronouns].tolist(
        ) + a.release_teams[team][group_returners][schema_pronouns].tolist(), team)
        filter_entities(a.release_teams[team][group_newcomers][schema_newcomers_timezone].tolist() + a.release_teams[team][group_returners][schema_returners_timezone].tolist(), "Timezone",
                        aliases=timezone_aliases,
                        threshold=1, unreached_threshold_print=False, team=team)


# Create applicant markdown files

# method used to write returner applications to a markdown file
def _returner_applications(team, a: ApplicantDataframes):
    team_returning_applicants = []
    indexes = a.release_teams[team][group_returners].index
    returners = a.release_teams[team][group_returners]
    for i in indexes:
        ag = GeneralInfo(returners[schema_email][i],
                         returners[schema_name][i],
                         returners[schema_pronouns][i],
                         returners[schema_slack][i],
                         returners[schema_github][i],
                         returners[schema_affiliation][i])
        ai = ReturnerInfo(returners[schema_returners_previous_roles][i],
                          returners[schema_returners_previous_release_and_role][i],
                          returners[schema_returners_interested_in_roles][i],
                          returners[schema_returners_timezone][i],
                          returners[schema_returners_can_volunteer_for_up_coming_cycles][i],
                          returners[schema_returners_goals][i],
                          returners[schema_returners_contribution_plans][i],
                          returners[schema_returners_interested_in_stable_roster][i])
        team_returning_applicants.append(ApplicantData(ag, ai))
    write_applications_to_file(
        team, group_returners, team_returning_applicants)


# method used to write newcomer applications to a markdown file
def _newcomer_applications(team, a: ApplicantDataframes):
    team_newcomer_applicants = []
    indexes = a.release_teams[team][group_newcomers].index
    nc = a.release_teams[team][group_newcomers]
    for i in indexes:
        ag = GeneralInfo(nc[schema_email][i],
                         nc[schema_name][i],
                         nc[schema_pronouns][i],
                         nc[schema_slack][i],
                         nc[schema_github][i],
                         nc[schema_affiliation][i])
        ai = NewcomerInfo(interested_roles=nc[schema_newcomers_interested_in_roles][i],
                          read_role_handbook=nc[schema_newcomers_read_handbook][i],
                          why_interested=nc[schema_newcomers_why_interested][i],
                          feedback_handbook=nc[schema_newcomers_handbook_questions][i],
                          timeestimate_commit_to_releaseteam=nc[schema_newcomers_timestimate][i],
                          able_to_attend_release_team_meetings=nc[schema_newcomers_attend_release_team_meetings][i],
                          able_to_attend_burndown_meetings=nc[schema_newcomers_attend_burndown_meetings][i],
                          scheduled_conflicts=nc[schema_newcomers_scheduled_conflicts][i],
                          volunteer_for_upcoming_cycles=nc[schema_newcomers_volunteer_upcoming_releases][i],
                          timezone=nc[schema_newcomers_timezone][i],
                          experience_contributing=nc[schema_newcomers_experience_contributing][i],
                          signed_cla=nc[schema_newcomers_signed_cla][i],
                          k8s_org_member=nc[schema_newcomers_k8s_org_member][i],
                          prior_release_teams=nc[schema_newcomers_prior_release_teams][i],
                          relevant_experience=nc[schema_newcomers_relevant_experience][i],
                          goals=nc[schema_newcomers_goals][i],
                          contribution_plans=nc[schema_newcomers_contribution_plans][i],
                          comments=nc[schema_newcomers_comments][i],
                          applied_previously=nc[schema_newcomers_applied_previously][i])
        team_newcomer_applicants.append(ApplicantData(ag, ai))
    write_applications_to_file(team, group_newcomers, team_newcomer_applicants)


# generate applicantion summary markdown files
def generate_application_summaries(a: ApplicantDataframes):
    for team in a.release_teams:
        _returner_applications(team, a)
        _newcomer_applications(team, a)


if __name__ == "__main__":
    # define flags
    local_excel_file = flag.string("file", "application-release-team-1.24.xlsx", "Applicant data source xlsx file")
    flag.parse()

    # try to open the specified file
    try:
        applicantionDf = load_data(local_excel_f=local_excel_file.val())
    except Exception as e: print(e)

    # create plots / charts
    general_plotting(applicantionDf)
    team_plotting(applicantionDf)

    # generate applicantion summary markdown files
    generate_application_summaries(applicantionDf)
