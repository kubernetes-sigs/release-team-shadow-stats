package mdwriter

import (
	"fmt"
	"kubernetes-sigs/release-team-shadow-stats/pkg/mdfilepermutations"
	"kubernetes-sigs/release-team-shadow-stats/pkg/yamlparser"
	"os"
	"path/filepath"
	"strings"

	dataframe "github.com/rocketlaunchr/dataframe-go"
)

type MdFileConfig struct {
	Folder      string
	Df          *dataframe.DataFrame
	MdFileInfos []mdfilepermutations.S
	Config      yamlparser.F
}

type MdFileContent map[mdfilepermutations.MdFilename]MdFileDetails

type MdFileDetails struct {
	F    mdfilepermutations.S
	Rows []map[string]interface{}
}

func CreateMarkdownFiles(mdfileconfig MdFileConfig) error {
	iterator := mdfileconfig.Df.ValuesIterator(dataframe.ValuesOptions{InitialRow: 0, Step: 1, DontReadLock: true})
	mdfileconfig.Df.Lock()

	mdFileContent := MdFileContent{}
	for _, p := range mdfileconfig.MdFileInfos {
		mdFileContent[p.MdFilename] = MdFileDetails{
			F:    p,
			Rows: []map[string]interface{}{},
		}
	}

	for {
		row, rawVals, _ := iterator()
		if row == nil {
			break
		}

		vals := make(map[string]interface{})
		for k, v := range rawVals {
			if strKey, ok := k.(string); ok {
				vals[strKey] = v
			}
		}

		for {
			row, rawVals, _ := iterator()
			if row == nil {
				break
			}

			vals := make(map[string]interface{})
			for k, v := range rawVals {
				if strKey, ok := k.(string); ok {
					vals[strKey] = v
				}
			}

			for filename, fileDetails := range mdFileContent {
				matchFound := true
				for _, val := range fileDetails.F.Values {
					keysMatch := false
					for _, key := range val.Keys {
						rowValue, ok := vals[string(key)].(string)
						if !ok {
							fmt.Printf("Value for key %s is not a string\n", key)
							continue
						}
						fmt.Printf("Checking key: %s, Permutation value: %v, Row value: %v\n", key, val.Val, rowValue)

						if strings.Contains(rowValue, string(val.Val)) {
							keysMatch = true
							break
						}
					}
					matchFound = matchFound && keysMatch
					if !matchFound {
						break
					}
				}
				if matchFound {
					mdFileDetails := mdFileContent[filename]
					mdFileDetails.Rows = append(mdFileDetails.Rows, vals)
					mdFileContent[filename] = mdFileDetails

					fmt.Printf("Row added to: %s\n", filename)
				}
			}
		}
	}

	mdfileconfig.Df.Unlock()

	for filename, mdFileDetails := range mdFileContent {
		formatEntry, err := formatEntry(string(filename), mdFileDetails.Rows, mdfileconfig.Config)
		if err != nil {
			panic(err)

		}
		err = writeToFile(fmt.Sprintf("%s/%s.md", mdfileconfig.Folder, filename), formatEntry)
		if err != nil {
			panic(err)
		}
	}

	return nil
}

func formatEntry(filename string, rows []map[string]interface{}, configFields yamlparser.F) (*strings.Builder, error) {
	var mdEntries strings.Builder

	mdEntries.WriteString("# " + filename + "\n\n")

	for _, row := range rows {
		// Process Title fields
		firstTitle := true
		for _, titleField := range configFields.Fields.Title {
			if value, ok := row[titleField]; ok && value != "" {
				if !firstTitle {
					mdEntries.WriteString(" -")
				} else {
					mdEntries.WriteString("## ")
				}
				mdEntries.WriteString(fmt.Sprintf("%s", value))
				firstTitle = false
			}
		}

		// Process Details fields
		for _, detailField := range configFields.Fields.Details {
			if value, ok := row[detailField]; ok && value != "" {
				mdEntries.WriteString(fmt.Sprintf("* **%s**: %s\n", detailField, value))
			}
		}
		mdEntries.WriteString("\n\n")

		// Process Text fields
		for _, textField := range configFields.Fields.Text {
			if value, ok := row[textField]; ok && value != "" {
				mdEntries.WriteString(fmt.Sprintf("### %s\n\n%s\n", textField, value))
			}
		}
		mdEntries.WriteString("\n---\n")
	}

	return &mdEntries, nil
}

func writeToFile(filename string, mdEntries *strings.Builder) error {
	dir := filepath.Dir(filename)

	err := os.MkdirAll(dir, os.ModePerm)
	if err != nil {
		return fmt.Errorf("failed to create directory %s: %w", dir, err)
	}

	file, err := os.Create(filename)
	if err != nil {
		return fmt.Errorf("failed to create file %s: %w", filename, err)
	}
	defer file.Close()

	_, err = file.WriteString(mdEntries.String())
	if err != nil {
		return fmt.Errorf("failed to write to file %s: %w", filename, err)
	}
	return nil
}
