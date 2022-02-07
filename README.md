# Release Team Shadow Applicant analysis

This project is being developed in the scope of Kubernetes [sig-release](https://github.com/kubernetes/sig-release/blob/master/release-team/README.md). The project intent is to initiate a discussion aimed at improving the Release Team Shadow program. This project could also be the subject of a donation to one of the Kubernetes repos/orgs.

**!! This project is subject to change and under discussion !!**

**!! IMPORTANT NOTE !!**: Since this project processes data of applicants, everything should be treated extra carefully. It must be insured that data is not leaked somewhere! (Example: No applicant data should be checking out to GitHub!).

## Summary
This project is designed to support at the release team shadow selection process. It should be used in the shadow selection phase and to communicate transparently with the community about the current status of the release team shadow program.    

**Goals**:
* Improve the release team shadow selection process
* Provide some transparency about the current shadow program

## Current Situation
Currently, there is nothing really in place. 
* Since the applicant data is confidential. The information is not shared. No one outside of sig-release has any idea of the status of the shadow application program.
* The release team has some guidelines, but no tools to assist in the selection of shadow applicants. This process is quite cumbersome as everything is based on Excel spreadsheets and it is difficult to review all applicants.

## Examples
**Plots**:
Plots are created for two different types of applicant pools. 
* Pool 1: all applicants
* Pool 2: applicants by sub-team (a pool for enhancements ). This means that the listed plots are created once for all applicants and then for each sub-team.

* Applicants by release-team sub-team (enhacements, docs, release-notes, comm's, ci-signal, bug-triage)
* Timezones
* Affiliation / company
* Pronouns
* Reapplying newcomers
* Newcomers / returners ratio

The pie charts are generated using the python library [matplotlib](https://matplotlib.org/stable/index.html).

**Applicant summary**:

Template for returners:
```md
## R[ID] [name] for [release sub-team]
**Pronoun**: [...], **Slack** [...], **GitHub** [...], **Affiliation**: [...]

* **Timezone**: [...]
* **Previous Roles**: [...]
* **Previous Release**: [...]

**Goals**:
[...]

**Contribution plans**:
[...]

* **Interest in stable rooster**: [Yes/No]
* **Can volunteer for up coming cycles**: [Yes/No]
```
Template for newcomers:

```md
## N[ID] [name] for [release sub-team]
**Pronoun**: [...], **Slack** [...], **GitHub** [...], **Affiliation**: [...]

* **Timezone**: [...]
* **Read handbook**: [Yes No]
* **Scheduled conflicts**: [...]

**Why interested**: [...]

**Goals**: [...] 

**Contribution plans**: [...]

**Comments**: [...]

**Relevant experience**: [...]

**Handbook feedback**: [...]

**Experience contributing**: [...]

**Prior release teams**: [...]

* **Timestimate to spare per week**: [...]
* **Able to attend release team meetings**: [...]
* **Able to attend burndown meetings**: [...]
* **Volunteer for upcoming cycles**: [Yes/No]
* **Applied previously**: [...]

* **K8s org member**: [Yes/No]
* **Signed CLA**: [Yes/No]

```

## How to work on this project

Create local virtual environment `python3 -m venv tutorial-env` and activate the virtual environment with `source venv/bin/activate`.
Install all dependencies with `pip install -r requirements.txt`. To update the requirements run `pip freeze > requirements.txt`. 
To generate the plots and applicant summaries run `python main.py`.
Make sure to place a matching xlsx file to the root dir of the project.

