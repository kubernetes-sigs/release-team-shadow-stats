package mdwriter

import (
	"fmt"
	"kubernetes-sigs/release-team-shadow-stats/pkg/mdfilepermutations"
	"kubernetes-sigs/release-team-shadow-stats/pkg/yamlparser"
	"os"
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

func WriteMarkdownFiles(mdfileconfig MdFileConfig) error {
	// open files buffers for each file
	err := openFileBuffers(mdfileconfig)
	if err != nil {
		return err
	}
	defer func() {
		for _, fileInfo := range mdfileconfig.MdFileInfos {
			fileInfo.File.Close()
		}
	}()

	// iterate over all rows in the dataframe
	iterator := mdfileconfig.Df.ValuesIterator(dataframe.ValuesOptions{InitialRow: 0, Step: 1, DontReadLock: true})
	mdfileconfig.Df.Lock()

	for {
		row, rawVals, _ := iterator()
		if row == nil {
			break // end of dataframe
		}

		// Convert raw values map[interface{}]interface{} to map[string]interface{}
		vals := make(map[string]interface{})
		for k, v := range rawVals {
			if strKey, ok := k.(string); ok {
				vals[strKey] = v
			}
		}

		// Temporary list to record to which files to write the row.
		//  This can be to multiple files
		writeToFiles := []*os.File{}

		for _, fileInfo := range mdfileconfig.MdFileInfos {
			matchFound := true
			for _, val := range fileInfo.Values {
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
				writeToFiles = append(writeToFiles, fileInfo.File)
			}
		}

		// write the row to the files
		for _, file := range writeToFiles {
			formattedEntry, err := formatEntry(vals, mdfileconfig.Config)
			if err != nil {
				return err
			}
			_, err = file.WriteString(fmt.Sprintf("%s\n", formattedEntry.String()))
			if err != nil {
				return err
			}
			fmt.Printf("Row added to: %s\n", file.Name())
		}
	}

	mdfileconfig.Df.Unlock()
	return nil
}

func openFileBuffers(mdfileconfig MdFileConfig) error {
	err := os.MkdirAll(mdfileconfig.Folder, os.ModePerm)
	if err != nil {
		return fmt.Errorf("failed to create directory %s: %w", mdfileconfig.Folder, err)
	}

	for i, info := range mdfileconfig.MdFileInfos {
		filename := fmt.Sprintf("%s/%s.md", mdfileconfig.Folder, info.MdFilename)
		f, err := os.Create(filename)
		if err != nil {
			return fmt.Errorf("failed to open file %s: %w", filename, err)
		}

		_, err = f.WriteString(fmt.Sprintf("# %s\n\n", info.MdFilename))
		if err != nil {
			return fmt.Errorf("failed to write the file header to file %s: %w", filename, err)
		}
		mdfileconfig.MdFileInfos[i].File = f
	}
	return nil
}

func formatEntry(row map[string]interface{}, configFields yamlparser.F) (*strings.Builder, error) {
	var mdEntries strings.Builder

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
	mdEntries.WriteString("\n\n")

	// Process Details fields
	for _, detailField := range configFields.Fields.Details {
		if value, ok := row[detailField]; ok && value != "" {
			mdEntries.WriteString(fmt.Sprintf("* **%s**: %s\n", detailField, value))
		}
	}

	// Process Text fields
	for _, textField := range configFields.Fields.Text {
		if value, ok := row[textField]; ok && value != "" {
			mdEntries.WriteString(fmt.Sprintf("\n### %s\n\n%s\n", textField, value))
		}
	}
	mdEntries.WriteString("\n---\n")

	return &mdEntries, nil
}
