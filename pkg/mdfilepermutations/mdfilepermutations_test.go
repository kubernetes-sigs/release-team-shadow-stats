package mdfilepermutations

import (
	"kubernetes-sigs/release-team-shadow-stats/pkg/yamlparser"
	"reflect"
	"testing"
)

func TestGetAllPermutations(t *testing.T) {
	tests := []struct {
		name     string
		cfg      []yamlparser.SplitFilesBy
		expected []S
	}{
		{
			name: "Basic Test",
			cfg: []yamlparser.SplitFilesBy{
				{
					Identifiers:     []string{"Identifier1", "Identifier1.1"},
					Alias:           map[string]string{"Option1": "Alias1"},
					PossibleOptions: []string{"Option1", "Option2"},
				},
				{
					Identifiers:     []string{"Identifier2"},
					Alias:           map[string]string{},
					PossibleOptions: []string{"OptionA", "OptionB"},
				},
			},
			expected: []S{
				{
					MdFilename: "Alias1-OptionA",
					Values: []SValue{
						{Val: "Option1", Alias: "Alias1", Keys: []CsvColKey{"Identifier1", "Identifier1.1"}},
						{Val: "OptionA", Alias: "", Keys: []CsvColKey{"Identifier2"}},
					},
				},
				{
					MdFilename: "Alias1-OptionB",
					Values: []SValue{
						{Val: "Option1", Alias: "Alias1", Keys: []CsvColKey{"Identifier1", "Identifier1.1"}},
						{Val: "OptionB", Alias: "", Keys: []CsvColKey{"Identifier2"}},
					},
				},
				{
					MdFilename: "Option2-OptionA",
					Values: []SValue{
						{Val: "Option2", Alias: "", Keys: []CsvColKey{"Identifier1", "Identifier1.1"}},
						{Val: "OptionA", Alias: "", Keys: []CsvColKey{"Identifier2"}},
					},
				},
				{
					MdFilename: "Option2-OptionB",
					Values: []SValue{
						{Val: "Option2", Alias: "", Keys: []CsvColKey{"Identifier1", "Identifier1.1"}},
						{Val: "OptionB", Alias: "", Keys: []CsvColKey{"Identifier2"}},
					},
				},
			},
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			result := GetAllPermutations(tt.cfg)
			if !reflect.DeepEqual(result, tt.expected) {
				t.Errorf("GetAllPermutations() for %s = %v, want %v", tt.name, result, tt.expected)
			}
		})
	}
}
