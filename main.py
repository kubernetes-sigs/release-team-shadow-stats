# Copyright 2022 The Kubernetes Authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import os
import flag
from src.config import CHART_SCHEMA_DEFINITIONS, SUMMARY_CONFIGS
from src.data_parser import read_file, clean_up_duplicate_column_names
from src.summary import write_file
from src.test_data import get_dataframe_random, TESTING_SCHEMA_CHARTS, TESTING_SCHEMA_SUMMARY

OPT_OUT_COLUMN_125 = "We would like to use your answers to produce anonymized reports about shadow applicants. Do you" \
                     " consent to your answers being used in a non-identifying way?"


if __name__ == "__main__":
    print("Process user input...")
    source_data_file = flag.string(
        "file", "shadow-application.csv", "Applicant data source CSV file")
    schema_version = flag.string(
        "schema", "1.25", "Schema that is used to create charts")
    test_mode = flag.int("test", 0, "Generate test files and don't read CSV file")
    flag.parse()

    df, df_opt_in = None, None
    schema_charts = []
    schema_summary = None
    if test_mode.val() != 1:
        print("Check input...")
        if not os.path.isfile(source_data_file.val()):
            print("ERROR: csv file does not exist")
            exit(1)
        if schema_version.val() not in CHART_SCHEMA_DEFINITIONS:
            print(f"ERROR: schema does not exist, currently {CHART_SCHEMA_DEFINITIONS.keys()} are defined")
            exit(1)

        print("Clean up potential duplicate column names...")
        cleaned_data_file = "cleaned-" + source_data_file.val()
        clean_up_duplicate_column_names(source_data_file.val(), cleaned_data_file)

        print("Create dataframe from data file...")
        df, df_opt_in = read_file(cleaned_data_file, OPT_OUT_COLUMN_125)

        print("Look for schema configuration")
        schema_charts = CHART_SCHEMA_DEFINITIONS[schema_version.val()]
        schema_summary = SUMMARY_CONFIGS[schema_version.val()]
    else:
        print("Test mode enabled... generate random test data...")
        df = get_dataframe_random()
        df_opt_in = df
        schema_charts = TESTING_SCHEMA_CHARTS
        schema_summary = TESTING_SCHEMA_SUMMARY

    print("Create charts that are used for the public report...")
    for chart in schema_charts:
        chart.create_plot(df_opt_in)

    print("Create markdown applicant summary...")
    write_file(df, schema_summary)
