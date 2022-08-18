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
import polars

CLEAN_KEYWORDS = "CLEAN_KEYWORDS"
CLEAN_ALIAS = "CLEAN_ALIAS"


# example parameter `options: {CLEAN_KEYWORDS: ["company1", "company2"]}`
def clean(series: polars.Series, options) -> polars.Series:
    for k, v in options.items():
        match k:
            case "CLEAN_KEYWORDS":
                series = series.apply(lambda x: _clean_keywords(x, v))
            case "CLEAN_ALIAS":
                series = series.apply(lambda x: _clean_alias(x, v))
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
