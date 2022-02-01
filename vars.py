# Groups of applicants
group_returners = "returners"
group_newcomers = "newcomers"

# Release team names
team_bugtriage = "Bug Triage"
team_cisignal = "CI Signal"
team_communications = "Communications"
team_releasenotes = "Release Notes"
team_documentation = "Documentation"
team_enhacements = "Enhancements"

applicants_folder = "applicants"


def get_applicants_file(team_name, group):
    return f"./{applicants_folder}/{team_name}-{group}.md"


plot_folder = "plots"


def get_plot_file(filename):
    return f"./{plot_folder}/{filename}.png"
