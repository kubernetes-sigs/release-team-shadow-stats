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
	outputFolder := pflag.String("output", "data/", "folder where markdown files will be written")
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

	if err = mdwriter.CreateMarkdownFiles(mdwriter.MdFileConfig{
		Folder:      *outputFolder,
		Df:          df,
		MdFileInfos: permutations,
		Config:      *config,
	}); err != nil {
		panic(err)
	}
}
