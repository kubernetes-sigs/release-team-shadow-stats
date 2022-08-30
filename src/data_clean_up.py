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


from collections import Counter
import polars


#
# Methods that can be specified to clean up the data

# Used to filter for keyword
# example "I am a Student" with the keyword "student" returns "student" (without "I am a")
CLEAN_KEYWORDS = "CLEAN_KEYWORDS"

# Used to filter out all keywords that match a record
# example "Team1, Team2 - Team3" with the keywords "Team1, Team2" returns ["Team1", "Team2"]
# this cleanup method extends the series if multiple keywords match
CLEAN_SPLIT_INTO_KEYWORDS = "CLEAN_SPLIT_INTO_KEYWORDS"

# aliases should be configured as map
# example: {"red hat": "redhat", "red-hat": "redhat"} ... if there is a match on "red hat it will transform to "redhat"
CLEAN_ALIAS = "CLEAN_ALIAS"

# used to filter out records that are in series total below threshold
# example: threshold=2, series=["a", "b", "c", "b", "c", "b"] -> ["b", "b", "b"]
CLEAN_THRESHOLD = "CLEAN_THRESHOLD"


# example parameter `options: {CLEAN_KEYWORDS: ["company1", "company2"]}`
def clean(series: polars.Series, options) -> polars.Series:
    for cleaning_mode, option in options.items():
        match cleaning_mode:
            case "CLEAN_KEYWORDS":
                series = series.apply(lambda x: _clean_keywords(x, option))
            case "CLEAN_ALIAS":
                series = series.apply(lambda x: _clean_alias(x, option))
            case "CLEAN_THRESHOLD":
                count = Counter(series)
                series = series.filter([count[x] > option for x in series.to_list()])
            case "CLEAN_SPLIT_INTO_KEYWORDS":
                tmp_list = []
                for e in series.to_list():
                    keyword_found = False
                    for option_e in option:
                        if e.__contains__(option_e):
                            keyword_found = True
                            tmp_list.append(option_e)
                    if not keyword_found:
                        tmp_list.append(e)
                series = polars.Series(tmp_list)
    return series


def _clean_keywords(s: str, keywords: any):
    s = s.lower()
    for k in keywords:
        k = k.lower()
        if s.__contains__(k):
            return k
    return s


# aliases should be configured as map
# example: {"red hat": "redhat", "red-hat": "redhat"} ... if there is a match on "red hat it will transform to "redhat"
def _clean_alias(s: str, aliases: any):
    s = s.lower()
    for k, v in aliases.items():
        if s.__contains__(k):
            return v
    return s
