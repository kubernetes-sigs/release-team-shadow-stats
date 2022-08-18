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
from data_clean_up import CLEAN_KEYWORDS, CLEAN_ALIAS
from defaults import timezone_aliases, company_keywords
from charts import BasicChart, plotting_count_entities_up

RELEASE_124 = "1.24"

SCHEMAS = {
    RELEASE_124: [
        BasicChart(["Company Affiliation / Employer"], plotting_count_entities_up,
                   {CLEAN_KEYWORDS: company_keywords}),
        BasicChart(["What time zone are you normally in?", "What time zone are you normally in?.1"],
                   plotting_count_entities_up, {CLEAN_ALIAS: timezone_aliases})
    ]
}
