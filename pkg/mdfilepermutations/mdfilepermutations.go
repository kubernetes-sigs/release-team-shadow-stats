package mdfilepermutations

import (
	"kubernetes-sigs/release-team-shadow-stats/pkg/yamlparser"
	"os"
	"strings"
)

// This file creates a list of all possible permutations of the split files by options

type (
	// The md filename is the name of the markdown file which is the combination of all identifiers (permutations)
	MdFilename string
	// The csv col key is the key in the CSV file (defined in the header)
	CsvColKey string
	// The csv col alias can be used to rename the default CsvColKey
	CsvColAlias string
	// The csv value is the value in the CSV file (everything after the header)
	CsvValue string
)

type S struct {
	MdFilename MdFilename
	Values     []SValue
	File       *os.File
}

type SValue struct {
	Val   CsvValue
	Alias CsvColAlias
	Keys  []CsvColKey
}

// GetAllPermutations generates all permutations of the given SplitFilesBy structs.
func GetAllPermutations(cfg []yamlparser.SplitFilesBy) []S {
	options := make([][]string, len(cfg))
	for i, field := range cfg {
		options[i] = append(options[i], field.PossibleOptions...)
	}

	permutations := cartesianProduct(options)

	var result []S
	for _, perm := range permutations {
		filenameParts := make([]string, len(perm))

		s := S{
			Values: []SValue{},
		}

		for j, val := range perm {
			var alias CsvColAlias

			if a, ok := cfg[j].Alias[val]; ok {
				alias = CsvColAlias(a)
				filenameParts[j] = strings.ReplaceAll(a, " ", "-")
			} else {
				filenameParts[j] = strings.ReplaceAll(val, " ", "-")
			}

			keys := make([]CsvColKey, len(cfg[j].Identifiers))
			for k, identifier := range cfg[j].Identifiers {
				keys[k] = CsvColKey(identifier)
			}

			s.Values = append(s.Values, SValue{
				Val:   CsvValue(val),
				Alias: alias,
				Keys:  keys,
			})
		}

		s.MdFilename = MdFilename(strings.Join(filenameParts, "-"))
		result = append(result, s)
	}

	return result
}

// Helper function to get all combinations of given slices.
func cartesianProduct(input [][]string) [][]string {
	if len(input) == 0 {
		return [][]string{}
	}

	result := [][]string{}
	var recurse func(int, []string)
	recurse = func(i int, acc []string) {
		if i == len(input) {
			result = append(result, append([]string{}, acc...))
			return
		}
		for _, s := range input[i] {
			recurse(i+1, append(acc, s))
		}
	}
	recurse(0, []string{})

	return result
}
