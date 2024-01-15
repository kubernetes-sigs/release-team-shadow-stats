# Release Team Shadow Applicant analysis

This project is designed to support at the release team shadow selection process. It generates a list of the release team shadow application data which is gathered each cycle.
The **release team emeritus advisor** uses this tool to generate and distribute the shadow application data **privately**.

## How to work on this project

1. Install [Go](https://go.dev/learn/)
2. Write the configuration file to match the release team shadow application data. Make sure to rename any columns that use an identifier twice. E.g. if the column `Goals` exists twice, rename the second one to `Goals.1`. An example yaml file can be found in `config.yaml`.
3. To run the application, execute `go run main.go` the following flags can be set.
   1.  `csv`, path to the CSV file with default `data.csv``
   2.  `yaml`, path to the YAML file with default `config.yaml`
   3.  `output`, folder where markdown files will be written with default `data/`

After the execution you should see files added to the `data` folder if not specified otherwise.

## Community, discussion, contribution, and support
You can reach the maintainers of this project at:

* [Kubernetes Slack](https://slack.k8s.io/) at `#sig-release`

## Sponsoring SIG's
* [`sig-release`](https://github.com/kubernetes/sig-release)

## Code of conduct
Participation in the Kubernetes community is governed by the Kubernetes [Code of Conduct](code-of-conduct.md).