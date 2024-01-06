/*
Copyright 2024 The Kubernetes Authors.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
*/

package main

import (
	"fmt"
	"kubernetes-sigs/release-team-shadow-stats/pkg/csvparser"
	"kubernetes-sigs/release-team-shadow-stats/pkg/mdfilepermutations"
	"kubernetes-sigs/release-team-shadow-stats/pkg/mdwriter"
	"kubernetes-sigs/release-team-shadow-stats/pkg/yamlparser"

	"github.com/spf13/pflag"
)

func main() {
	csvFilePath := pflag.String("csv", "data.csv", "path to the CSV file")
	yamlFilePath := pflag.String("yaml", "config.yaml", "path to the YAML file")
	outputFolder := pflag.String("output", "data", "folder where markdown files will be written")
	pflag.Parse()

	config, err := yamlparser.ReadYAMLFile(*yamlFilePath)
	if err != nil {
		panic(err)
	}

	permutations := mdfilepermutations.GetAllPermutations(config.SplitFilesBy)
	fmt.Println("Total files:", len(permutations))

	df, err := csvparser.ReadCSVFile(*csvFilePath)
	if err != nil {
		panic(err)
	}
	fmt.Printf("CSV Rows: %d", df.NRows())

	if err = mdwriter.WriteMarkdownFiles(&mdwriter.MdFileConfig{
		Folder:      *outputFolder,
		Df:          df,
		MdFileInfos: permutations,
		Config:      *config,
	}); err != nil {
		panic(err)
	}
}
