package csvparser

import (
	"context"
	"fmt"
	"os"

	dataframe "github.com/rocketlaunchr/dataframe-go"
	"github.com/rocketlaunchr/dataframe-go/imports"
)

func ReadCSVFile(filepath string) (*dataframe.DataFrame, error) {
	file, err := os.Open(filepath)
	if err != nil {
		fmt.Println("Error opening file:", err)
		return nil, err
	}
	defer file.Close()

	df, err := imports.LoadFromCSV(context.Background(), file)
	if err != nil {
		fmt.Println("Error reading from CSV:", err)
		return nil, err
	}

	return df, nil
}
