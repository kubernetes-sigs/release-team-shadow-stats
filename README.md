# Release Team Shadow Applicant analysis

*Disclaimer: The project is work in progress*

This project is designed to support at the release team shadow selection process. It should be used in the shadow selection phase and to communicate transparently with the community about the current status of the release team shadow program.    

**Goals**:
* Improve the release team shadow selection process by extracting data from a excel into multiple markdown files (see [examples/applicant](https://github.com/kubernetes-sigs/release-team-shadow-stats/tree/main/examples/applicants))  
* Provide some transparency about the current shadow program by creating non identifying charts that can be shared with the community (see [examples/plots](https://github.com/kubernetes-sigs/release-team-shadow-stats/tree/main/examples/plots))

The files in found under the folder [`example/`](https://github.com/kubernetes-sigs/release-team-shadow-stats/tree/main/examples) are generated with fake data!

## Examples (see [examples/README.md](https://github.com/kubernetes-sigs/release-team-shadow-stats/blob/main/examples/README.md))

Examples for the chats / plots and the applicant summary markdown files can be found under the folder `examples/`. 

Release Team shadow applicants by team
![example: applicants by team](./examples/plots/applicants-by-team.png)
Pronouns Example
![example: pronouns](./examples/plots/pronouns-.png)
...more charts can be found under `examples/plots`

By running `python main.py --test=1` dummy applicant data is getting generated.

## How to work on this project

### Setup your local working environment

1. Create a local virtual python environment `python3 -m venv venv`
2. Activate the local virtual python environment `source venv/bin/activate`.
3. Install dependencies `pip install -r requirements.txt`. 


To generate the plots and applicant summaries run `python main.py --file=your-file.xlsx`.
Make sure to place a matching xlsx file to the root dir of the project.

### Run the application

To update the requirements run `pip freeze > requirements.txt`.

## Community, discussion, contribution, and support
You can reach the maintainers of this project at:

* [Kubernetes Slack](https://slack.k8s.io/) at `#sig-release` and `#release-ci-signal`

## Sponsoring SIG's
* [`sig-release`](https://github.com/kubernetes/sig-release)

## Code of conduct
Participation in the Kubernetes community is governed by the Kubernetes [Code of Conduct](code-of-conduct.md).