import inclusion_exclusion_criteria

inclusion_criteria_title = ["implying a relation with energy issues?"]

inclusion_criteria_title_and_abstract = [
    "dealing with energy supply?",
    "highlighting the relevance of justice in planning?",
    "investigating the impact of policies on consumer justice?",
    "offer a structurized approach to justice via eg a model or framework?",
    "clearly stating at least one justice indicator? (including fuzzy logic)",
    "hinting at at least one relevant justice indicator? (only True if no explicit mention)",
    "otherwise relevant for the paper? (only True if otherwise not included)",
    "otherwise relevant for my PhD?",
    "otherwise relevant for people I know?",
]

dict_options_inclusion_criteria_title_and_abstract = {
    inclusion_criteria_title_and_abstract[0]: [True, False],
    inclusion_criteria_title_and_abstract[1]: [True, False],
    inclusion_criteria_title_and_abstract[2]: [True, False],
    inclusion_criteria_title_and_abstract[3]: [True, False],
    inclusion_criteria_title_and_abstract[4]: [True, False],
    inclusion_criteria_title_and_abstract[5]: [True, False],
    inclusion_criteria_title_and_abstract[6]: [True, False],
}

exclusion_criteria = [""]

file = "2022-07-19-Final-Keywords-Publications-merged-Count.csv"
output_file = file[:-4] + "-votes.csv"

target_value_of_inclusion_criteria = 5
number_of_inclusion_criteria = 5
list_index_positive_vote = 6

inclusion_exclusion_criteria.evaluate_title_and_abstract(
    file=file,
    output_file=output_file,
    inclusion_criteria_title=inclusion_criteria_title,
    inclusion_criteria_title_and_abstract=inclusion_criteria_title_and_abstract,
    dict_options_inclusion_criteria_title_and_abstract=dict_options_inclusion_criteria_title_and_abstract,
    target_value_of_inclusion_criteria=target_value_of_inclusion_criteria,
    number_of_inclusion_criteria=number_of_inclusion_criteria,
    list_index_positive_vote=list_index_positive_vote,
)
