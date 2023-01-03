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


from dataclasses import dataclass
import polars

# The variables below are used to match the configuration in a map
SUMMARY_IS_RETURNER_COLUMN = "SUMMARY_IS_RETURNER_COLUMN"
SUMMARY_TEAM_COLUMN = "SUMMARY_TEAM_COLUMN"
SUMMARY_DEACTIVATED_COLUMNS = "SUMMARY_DEACTIVATED_COLUMNS"


@dataclass(order=True)
class SummaryConfig:
    returner_column_name: str
    team_column_name: list[str]
    deactivated_columns: list[str]
    column_rename: dict[str, str]
    teams: list[str]
    file_prefix: str


def write_file(df: polars.DataFrame, config: SummaryConfig):
    returners = df.filter(polars.col(config.returner_column_name) == "Yes")
    newcomers = df.filter(polars.col(config.returner_column_name) == "No")
    for group_name, e in {"Returners": returners, "Newcomers": newcomers}.items():
        print(f"Writing group {group_name}")
        for team in config.teams:
            print(f"Writing team {team}")
            f = open(f"{config.file_prefix}{group_name.lower()}-{team.lower().replace(' ', '-')}.md", "w+")
            f.write(f"# {group_name} {team}")
            i = 1
            for team_column in config.team_column_name:
                for _, row in e.filter(polars.col(team_column).str.contains(team)).to_pandas().iterrows():
                    f.write(f"\n\n## {group_name[0]}{i}")
                    for colum in e.columns:
                        if colum not in config.deactivated_columns and row[colum] is not None:
                            if colum in config.column_rename:
                                f.write(f"\n- **{config.column_rename[colum].strip()}**: {row[colum]}")
                            else:
                                f.write(f"\n- **{colum.strip()}**: {row[colum]}")
                    i += 1
            f.close()


if __name__ == "__main__":
    d = polars.DataFrame({
        'Company1': ['AA1', 'AA2', 'AA3', 'AA4', 'AA5', 'AA6', 'AA7', 'AA8'],
        'Interested Roles': ['A', 'A', '', '', 'C', 'A, C', '', ''],
        'Interested Roles2': ['', '', 'B, C', 'B', '', '', '', 'B'],
        'Experienced': ['Yes', 'No', 'Yes', 'No', 'No', 'No', 'No', 'Yes'],
        'Experienced2': ['Yes', 'No', 'Yes', 'No', 'No', 'No', 'No', 'Yes'],
        'Experienced3': ['Yes', 'No', 'Yes', 'No', 'No', 'No', 'No', 'Yes'],
    })
    write_file(d, SummaryConfig("Experienced", ["Interested Roles", "Interested Roles2"],
                                ["Experienced2", "Experienced3"], {"Company1": "Company"}, ["A", "B", "C"]))
