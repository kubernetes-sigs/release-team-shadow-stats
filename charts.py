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
from collections import Counter
import polars

from data_clean_up import clean


# Type of charts that can be created
def plotting_count_entities_up(series: polars.Series, config: any):
    column = clean(series, config)
    print(Counter(column))
    # create plot and safe it to the plot folder


@dataclass(order=True)
class BasicChart:
    # name of the columns to process the data from
    dataframe_columns: list[str]
    # this needs to be a function that creates a chart, see plotting_xxx methods above
    plotter: any
    # this should be a map to configure how to clean up the data before creating the chart, see data_clean_up.py
    data_clean_up_config: any

    def create_plot(self, df: polars.DataFrame):
        s = polars.Series([]).cast(str)
        for e in self.dataframe_columns:
            print(df.get_column(e))
            s.append(df.get_column(e))
        self.plotter(s, self.data_clean_up_config)
