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
from config import RELEASE_124, SCHEMAS
from data_parser import read_file, clean_up_duplicate_column_names

if __name__ == "__main__":
    # Get user input from flags
    version = RELEASE_124

    # Check user input
    # ...

    # Clean duplicate column names
    source_data_file = "./test-125.csv"
    cleaned_data_file = "./test-125-2.csv"
    clean_up_duplicate_column_names(source_data_file, cleaned_data_file)

    # Create dataframe from data file
    df = read_file(cleaned_data_file)

    # Create charts that are used for the public report
    print("create plots...")
    for chart in SCHEMAS[version]:
        chart.create_plot(df)
    print("finished creating plots...")

    # Create markdown applicant summary
    # ...
