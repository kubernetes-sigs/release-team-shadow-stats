# Groups of applicants
group_returners = "returners"
group_newcomers = "newcomers"

# Release team names
team_bugtriage = "Bug Triage"
team_cisignal = "CI Signal"
team_communications = "Communications"
team_releasenotes = "Release Notes"
team_documentation = "Documentation"
team_enhancements = "Enhancements"

applicants_folder = "applicants"


def get_applicants_file(team_name, group):
    return f"./{applicants_folder}/{team_name}-{group}.md"


plot_folder = "plots"

theme_matplotlib = 'ggplot'


def get_plot_file(filename):
    return f"./{plot_folder}/{filename}.png"


timezone_aliases = {
    "gmt": "london gmt+0", "paris": "london gmt+0", "london": "london gmt+0",
    "middle europe": "central europe gmt+1", "cet": "central europe gmt+1", "+ 1": "central europe gmt+1", "central time": "central europe gmt+1", "central european time": "central europe gmt+1", "berlin": "central europe gmt+1", "+1": "central europe gmt+1",
    "ist": "india gmt+5", "+5": "india gmt+5", "+ 5": "india gmt+5", "india": "india gmt+5", "indian": "india gmt+5", "+ 6": "india gmt+5",
    "pst": "us pacific gmt-8", "pdt": "us pacific gmt-8", "pacific": "us pacific gmt-8", "pacific time": "us pacific gmt-8",
    "edt": "us east gmt-5", "eastern time": "us east gmt-5", "us east": "us east gmt-5", "est": "us east gmt-5",
    "+4": "iran gmt+4",
    "+2": "east europe gmt+2", "eastern europe": "east europe gmt+2", "eastern standard time": "east europe gmt+2",
    "+3": "arabia gmt+3",
    "+9": "japan gmt+9", "jst": "japan gmt+9",
    "+8": "china gmt+8", "shanghai": "china gmt+8",
    "utc": "london gmt+0"
}


# Schema variables reference column headers of the applicant excel file
release_version = "1.24"  # TODO: dynamic schema

# General applicant infos
schema_email = "Email Address"
schema_name = "Name"
schema_pronouns = "To help address everyone correctly, please share your pronouns if you're comfortable doing so. You can more about pronoun sharing here https://www.mypronouns.org/sharing"
schema_slack = "Slack Handle"
schema_github = "Github Handle"
schema_affiliation = "Company Affiliation / Employer"
schema_previously_served = "Have you previously served on a Kubernetes Release Team?"

# Returners infos
schema_returners_previous_roles = "Which release team roles have you served in?"
schema_returners_previous_release_and_role = "Please tell us which release team(s) you were previously on and what role you held (i.e. Lead or Shadow)"
schema_returners_interested_in_roles = f"What release team roles are you interested in for {release_version}?"
schema_returners_can_volunteer_for_up_coming_cycles = "Can you volunteer for 1.25 or 1.26?"
schema_returners_timezone = "What time zone are you normally in?"
schema_returners_goals = "Goals"
schema_returners_contribution_plans = "Contribution Plans"
schema_returners_interested_in_stable_roster = "Are you interested in joining a release team stable roster"

# Newcomers
schema_newcomers_interested_in_roles = "Which release roles are you interested in?"
schema_newcomers_read_handbook = "Have you read the role handbook associated with that role?"
schema_newcomers_why_interested = "Why are you interested in that role(s)?"
schema_newcomers_handbook_questions = "Do you have other feedback or questions about the handbook?"
schema_newcomers_timestimate = "How much time do you estimate you can commit to the Release Team a week? "
schema_newcomers_attend_release_team_meetings = "Will you be able to attend Release Team meetings? "
schema_newcomers_attend_burndown_meetings = "Will you be able to attend Burndown meetings?"
schema_newcomers_scheduled_conflicts = "Do you have schedule conflicts?"
schema_newcomers_volunteer_upcoming_releases = f"{schema_returners_can_volunteer_for_up_coming_cycles}.1"
schema_newcomers_timezone = f"{schema_returners_timezone}.1"
schema_newcomers_experience_contributing = "What is your experience contributing?"
schema_newcomers_signed_cla = "Have you signed the CLA?"
schema_newcomers_k8s_org_member = "Are you a Kubernetes Org Member?"
schema_newcomers_prior_release_teams = "Prior Release Teams"
schema_newcomers_relevant_experience = "Relevant Experience"
schema_newcomers_goals = f"{schema_returners_goals}.1"
schema_newcomers_contribution_plans = f"{schema_returners_contribution_plans}.1"
schema_newcomers_comments = "Comments"
schema_newcomers_applied_previously = "Have you applied to any previous Kubernetes release teams?"
