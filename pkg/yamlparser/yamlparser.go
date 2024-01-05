package yamlparser

import (
	"io"
	"os"

	"gopkg.in/yaml.v2"
)

type F struct {
	Fields       Fields         `yaml:"Fields"`
	SplitFilesBy []SplitFilesBy `yaml:"SplitFilesBy"`
}

// Fields contians information which identifiers to write in the markdown file to which position 1. Title 2. Details 3. Text
type Fields struct {
	Title   []string `yaml:"Title"`
	Details []string `yaml:"Details"`
	Text    []string `yaml:"Text"`
}

type SplitFilesBy struct {
	// Identifier is the key in the CSV file (defined in the header)
	Identifiers []string `yaml:"Identifiers"`
	// Alias can be used to map the option to a different name
	Alias map[string]string `yaml:"Alias"`
	// PossibleOptions is a list of all possible options / values for the identifier (everything after the header in the CSV file)
	PossibleOptions []string `yaml:"PossibleOptions"`
}

func ReadYAMLFile(filepath string) (*F, error) {
	file, err := os.Open(filepath)
	if err != nil {
		return nil, err
	}
	defer file.Close()

	bytes, err := io.ReadAll(file)
	if err != nil {
		return nil, err
	}

	var config F
	err = yaml.Unmarshal(bytes, &config)
	if err != nil {
		return nil, err
	}
	return &config, nil
}
