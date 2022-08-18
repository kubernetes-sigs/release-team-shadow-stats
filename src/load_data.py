# # Copyright 2022 The Kubernetes Authors.
# #
# # Licensed under the Apache License, Version 2.0 (the "License");
# # you may not use this file except in compliance with the License.
# # You may obtain a copy of the License at
# #
# #     http://www.apache.org/licenses/LICENSE-2.0
# #
# # Unless required by applicable law or agreed to in writing, software
# # distributed under the License is distributed on an "AS IS" BASIS,
# # WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# # See the License for the specific language governing permissions and
# # limitations under the License.
#
# #
# # This file contains logic to load data from a excel file for further processing
# #
#
# import pandas as pd
# from vars import *
# from applicants import ApplicantData, Applicants, GeneralInfo, NewcomerApplicant, ReturnerApplicant
#
#
# def load_data(local_excel_f) -> Applicants:
#     """Use pandas to load the local excel file and generate a dataframe
#     additionally filter create sub dataframes to reduce filtering simplify at usage
#     """
#     dataframe = pd.read_excel(local_excel_f)
#     returners = dataframe[dataframe[SCHEMA_PREVIOUSLY_SERVED].str.contains(
#         "Yes")]
#     newcomers = dataframe[dataframe[SCHEMA_PREVIOUSLY_SERVED].str.contains(
#         "No")]
#
#     returners_classes = _get_returner_info_from_df(returners)
#     newcomers_classes = _get_newcomer_info_from_df(newcomers)
#     all_applicants = returners_classes + newcomers_classes
#
#     applicants_by_team = {TEAM: {
#         GROUP_NEWCOMERS: list(filter(lambda a: a.a_specific_info.interested_roles.__contains__(TEAM), newcomers_classes)),
#         GROUP_RETURNERS: list(filter(
#             lambda a: a.a_specific_info.interested_roles.__contains__(TEAM), returners_classes))
#     } for TEAM in RELEASE_TEAM_TEAMS}
#
#     return Applicants(all_applicants, returners_classes, newcomers_classes, applicants_by_team)
#
#
# def _get_general_info_from_df(df_series, i) -> GeneralInfo:
#     return GeneralInfo(
#         df_series[SCHEMA_EMAIL][i],
#         df_series[SCHEMA_NAME][i],
#         df_series[SCHEMA_PRONOUNS][i],
#         df_series[SCHEMA_SLACK][i],
#         df_series[SCHEMA_GITHUB][i],
#         df_series[SCHEMA_AFFILIATION][i]
#     )
#
#
# def _get_returner_info_from_df(returners) -> list[ApplicantData]:
#     """Write returner applications to a markdown file"""
#     team_returning_applicants = []
#     indexes = returners.index
#     for i in indexes:
#         general_info = _get_general_info_from_df(returners, i)
#         returner_info = ReturnerApplicant(
#             returners[SCHEMA_RETURNERS_PREVIOUS_ROLES][i],
#             returners[SCHEMA_RETURNERS_PREVIOUS_RELEASE_AND_ROLE][i],
#             returners[SCHEMA_RETURNERS_INTERESTED_IN_ROLES][i],
#             returners[SCHEMA_RETURNERS_TIMEZONE][i],
#             returners[SCHEMA_RETURNERS_CAN_VOLUNTEER_FOR_UP_COMING_CYCLES][i],
#             returners[SCHEMA_RETURNERS_GOALS][i],
#             returners[SCHEMA_RETURNERS_CONTRIBUTION_PLANS][i],
#             returners[SCHEMA_RETURNERS_INTERESTED_IN_STABLE_ROSTER][i]
#         )
#         team_returning_applicants.append(
#             ApplicantData(general_info, returner_info))
#     return team_returning_applicants
#
#
# def _get_newcomer_info_from_df(newcomer) -> list[ApplicantData]:
#     team_newcomer_applicants = []
#     indexes = newcomer.index
#     for i in indexes:
#         general_info = _get_general_info_from_df(newcomer, i)
#         newcomer_info = NewcomerApplicant(
#             interested_roles=newcomer[SCHEMA_NEWCOMERS_INTERESTED_IN_ROLES][i],
#             read_role_handbook=newcomer[SCHEMA_NEWCOMERS_READ_HANDBOOK][i],
#             why_interested=newcomer[SCHEMA_NEWCOMERS_WHY_INTERESTED][i],
#             feedback_handbook=newcomer[SCHEMA_NEWCOMERS_HANDBOOK_QUESTIONS][i],
#             timeestimate_commit_to_releaseteam=newcomer[
#                 SCHEMA_NEWCOMERS_TIMESTIMATE][i],
#             able_to_attend_release_team_meetings=newcomer[
#                 SCHEMA_NEWCOMERS_ATTEND_RELEASE_TEAM_MEETINGS][i],
#             able_to_attend_burndown_meetings=newcomer[
#                 SCHEMA_NEWCOMERS_ATTEND_BURNDOWN_MEETINGS][i],
#             scheduled_conflicts=newcomer[SCHEMA_NEWCOMERS_SCHEDULED_CONFLICTS][i],
#             volunteer_for_upcoming_cycles=newcomer[
#                 SCHEMA_NEWCOMERS_VOLUNTEER_UPCOMING_RELEASE][i],
#             timezone=newcomer[SCHEMA_NEWCOMERS_TIMEZONE][i],
#             experience_contributing=newcomer[SCHEMA_NEWCOMERS_EXPERIENCE_CONTRIBUTING][i],
#             signed_cla=newcomer[SCHEMA_NEWCOMERS_SIGNED_CLA][i],
#             k8s_org_member=newcomer[SCHEMA_NEWCOMERS_K8S_ORG_MEMBER][i],
#             prior_release_teams=newcomer[SCHEMA_NEWCOMERS_PRIOR_RELEASE_TEAMS][i],
#             relevant_experience=newcomer[SCHEMA_NEWCOMERS_RELEVANT_EXPERIENCE][i],
#             goals=newcomer[SCHEMA_NEWCOMERS_GOALS][i],
#             contribution_plans=newcomer[SCHEMA_NEWCOMERS_CONTRIBUTION_PLANS][i],
#             comments=newcomer[SCHEMA_NEWCOMERS_COMMENTS][i],
#             applied_previously=newcomer[SCHEMA_NEWCOMERS_APPLIED_PREVIOUSLY][i]
#         )
#         team_newcomer_applicants.append(
#             ApplicantData(general_info, newcomer_info)
#         )
#     return team_newcomer_applicants
