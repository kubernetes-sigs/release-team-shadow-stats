# Schema variables reference column headers of the applicant excel file
release_version = "1.24" # TODO: dynamic schema


# General applicant infos
schema_email = "Email Address"
schema_name = "Name"
schema_pronouns = "To help address everyone correctly, please share your pronouns if you're comfortable doing so. You can more about pronoun sharing here https://www.mypronouns.org/sharing"
schema_slack = "Slack Handle"
schema_github = "Github Handle"
schema_affiliation="Company Affiliation / Employer"
schema_previously_served = "Have you previously served on a Kubernetes Release Team?"

# Returners infos
schema_returners_previous_roles = "Which release team roles have you served in?"
schema_returners_previous_release_and_role = "Please tell us which release team(s) you were previously on and what role you held (i.e. Lead or Shadow)"
schema_returners_interested_in_roles = f"What release team roles are you interested in for {release_version}?"
schema_returners_can_volunteer_for_up_coming_cycles = "Can you volunteer for 1.25 or 1.26?"
schema_returners_timezone="What time zone are you normally in?"
schema_returners_goals="Goals"
schema_returners_contribution_plans="Contribution Plans"
schema_returners_interested_in_stable_roster="Are you interested in joining a release team stable roster"

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
schema_newcomers_timezone=f"{schema_returners_timezone}.1"
schema_newcomers_experience_contributing = "What is your experience contributing?"
schema_newcomers_signed_cla = "Have you signed the CLA?"
schema_newcomers_k8s_org_member = "Are you a Kubernetes Org Member?"
schema_newcomers_prior_release_teams = "Prior Release Teams"
schema_newcomers_relevant_experience = "Relevant Experience"
schema_newcomers_goals = f"{schema_returners_goals}.1"
schema_newcomers_contribution_plans = f"{schema_returners_contribution_plans}.1"
schema_newcomers_comments = "Comments"
schema_newcomers_applied_previously = "Have you applied to any previous Kubernetes release teams?"