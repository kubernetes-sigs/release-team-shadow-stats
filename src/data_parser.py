# Copyright 2022 The Kubernetes Authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0xsx
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import polars as ps


# This function is used to read csv files, decode the files and return a polars dataframe
def read_file(file, opt_out_column, opt_in_key="Yes") -> ps.DataFrame:
    df = ps.read_csv(file)
    if opt_out_column != "":
        # Just go ahead with the data if the applicant has given consent to the data processing
        return df.filter(ps.col(opt_out_column) == opt_in_key)
    return df


# clean_up_duplicate_column_names used to set unique column names which are required for further processing
def clean_up_duplicate_column_names(file, new_file, duplicate_column_identifier=".1"):
    duplicated_column_count = 0
    with open(new_file, "w") as target_file:
        with open(file, "r") as source_file:
            first_line = True
            for row in source_file:
                # just check the first line of the file to update the column names
                if first_line:
                    first_line = False
                    previous_char = " "
                    columns = []
                    current_column = ""
                    for i in range(len(row)):
                        if row[i] == "," and row[i + 1] != " " and previous_char != " ":
                            # it can be the case that there are three or more columns with the same name,
                            # in this case the next two lines would need to get updated
                            if current_column in columns:
                                print("- info, duplicate Column name detected: ", current_column)
                                duplicated_column_count += 1
                                current_column += duplicate_column_identifier
                            columns.append(current_column)
                            current_column = ""
                        else:
                            current_column += row[i]
                        previous_char = row[i]
                    target_file.write(','.join(columns) + "\n")
                    continue
                # copy and paste lines after the header line to the new file without modification
                target_file.write(row)
            source_file.close()
        target_file.close()
    print(f"= {duplicated_column_count} column names cleaned up")
