import inclusion_exclusion_criteria

screened_by = "Martha"
# screened_by = "Jonathan"

# Keeping this criteria, as otherwise too much code to change
inclusion_criteria_title = ["implying a relation with energy issues?"]

inclusion_criteria_title_and_abstract = [
    "Does the paper define justice indicators? (0=nope, 1=probably/on the side, 2=yes, 3=exeptional)",
    "Does the paper implement justice indicators? (0=nope, 1=probably/on the side, 2=yes, 3=exeptional)",
    "Does the paper assess injustices between different defined groups? (0=nope, 1=probably/on the side, 2=yes, 3=exeptional)",
    "Is the paper describing justice in (1) a numerical approach, (2) a theoretical framework or (3) with other means?",
    "Which topic does the paper mainly address? (1) carbon emissions, (2) carbon pricing or tax, (3) SDG, (4) electrification, (5) the water-energy-nexus or (6) else.",
    "Who might be interested in the paper? (1) Martha (local/consumer), (2) Jonathan (national), (3) Luisa (heat/sufficiency), (4) Alex (theory), (5) any.",
    "Paper must be included! (Veto)",
    "Paper is included based on the veto above, but is only relevant for the backgroud  section.",
]

dict_options_inclusion_criteria_title_and_abstract = {
    inclusion_criteria_title_and_abstract[0]: [0, 1, 2, 3],
    inclusion_criteria_title_and_abstract[1]: [0, 1, 2, 3],
    inclusion_criteria_title_and_abstract[2]: [0, 1, 2, 3],
    inclusion_criteria_title_and_abstract[3]: [1, 2, 3],
    inclusion_criteria_title_and_abstract[4]: [1, 2, 3, 4, 5, 6],
    inclusion_criteria_title_and_abstract[5]: [1, 2, 3, 4, 5],
    inclusion_criteria_title_and_abstract[6]: [True, False],
    inclusion_criteria_title_and_abstract[7]: [True, False],
}

exclusion_criteria = [""]

file = "2022-07-19-Final-Keywords-Publications-merged-Count-votes-only-included.csv"
output_file = file[:-4] + "-2nd-screening"
if screened_by == "Martha":
    output_file += "-m"
elif screened_by == "Jonathan":
    output_file += "-j"
output_file += ".csv"

number_of_inclusion_criteria = 3
target_value_of_inclusion_criteria = 6
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
