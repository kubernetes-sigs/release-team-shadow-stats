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
import matplotlib.pyplot as plt
import polars
from src.data_clean_up import clean
from src.defaults import THEME_MARPLOTLIB, get_plot_file


def _make_auto_percent(values):
    """generic method to display percentage and amount on charts"""

    def my_autopct(pct):
        total = sum(values)
        val = int(round(pct * total / 100.0))
        return f"{pct:.2f}%  ({val:d})"

    return my_autopct


# Type of charts that can be created
def plotting_count_entities_up(series: polars.Series, name: str, config: any):
    column = clean(series.drop_nulls(), config)
    column_counter = Counter(column)
    _, ax = plt.subplots()
    ax.pie(column_counter.values(), labels=break_label_lines(column_counter.keys(), 4),
           autopct=_make_auto_percent(column_counter.values()))
    ax.axis('equal')
    plt.style.use(THEME_MARPLOTLIB)
    plt.title(name)
    plt.savefig(get_plot_file(name.lower().replace(" ", "-")))


def break_label_lines(list_of_labels, max_words_per_line: int):
    updated_list = []
    for label in list_of_labels:
        i = 0
        w = ""
        splitted_label_text = label.split()
        for e in splitted_label_text:
            i += 1
            if i > max_words_per_line:
                w += f"\n"
                i = 1
            w += f"{e} "
        updated_list.append(w.strip())
    return updated_list

@dataclass(order=True)
class BasicChart:
    # Title of the diagram
    plot_name: str
    # name of the columns to process the data from
    dataframe_columns: list[str]
    # this needs to be a function that creates a chart, see plotting_xxx methods above
    plotter: any
    # this should be a map to configure how to clean up the data before creating the chart, see data_clean_up.py
    data_clean_up_config: any

    def create_plot(self, df: polars.DataFrame):
        s = polars.Series([]).cast(str)
        for e in self.dataframe_columns:
            s.append(df.get_column(e))
        self.plotter(s, self.plot_name, self.data_clean_up_config)
