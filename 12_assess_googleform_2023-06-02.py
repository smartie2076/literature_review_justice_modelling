import re

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import collections

CREATE_PLOTS = True
PRINT_RESULT_SNIPPETS = False
np.set_printoptions(linewidth=100000)  # Export processed data without linebreaks in csv

path_base = "2023-06-02-GoogleFormResults"

FILENAME = (
    f"{path_base}/2023-06-02-Survery-Literature-Review-Justice-in-Modelling-Final"
)
CSV = ".csv"
PNG = ".png"

PARAMETER = "parameter"  # parameters/answer options
DOI = "doi"

RESULT_FOLDER = f"{path_base}-Evaluation"

# Columns
column_file = f"{path_base}/00_googleform_code_2023-03-Survery-Literature-Review-Justice-in-Modelling-Final"

print(column_file)

columns = pd.read_csv(column_file + CSV, header=None).squeeze("columns")
results = pd.read_csv(FILENAME + CSV)


def get_all_answers_with_doi(results, column_number, sep=","):
    list_of_answers = []
    list_of_doi = []

    for paper in results.index:
        if (
            pd.isna(results[columns[column_number]][paper]) is False
            and len(results[columns[column_number]][paper]) > 1
        ):
            answer_string = results[columns[column_number]][paper] + f"{sep} "
            answer_string.replace(f"{sep} ", sep)
            phrases_seperated_by_comma = [
                ele for ele in answer_string.split(sep) if ele != ""
            ]
            phrases_seperated_by_comma = list(
                filter(lambda x: x != " ", phrases_seperated_by_comma)
            )
            list_of_answers += phrases_seperated_by_comma
            list_of_doi += [
                results[columns[1]][paper] for ele in phrases_seperated_by_comma
            ]
    list_of_answers = [x.lower() for x in list_of_answers]
    df_answers_doi = pd.DataFrame({PARAMETER: list_of_answers, DOI: list_of_doi})
    return df_answers_doi


def get_list_of_factors_not_implemented(
    results,
    column_number_suggested,
    column_number_implemented,
    list_implemented_answers_and_doi=None,
):
    df_suggested_answes_and_doi = get_all_answers_with_doi(
        results=results, column_number=column_number_suggested
    )
    if list_implemented_answers_and_doi is None:
        df_implemented_answers_and_doi = get_all_answers_with_doi(
            results=results, column_number=column_number_implemented
        )
        list_implemented_answers_and_doi = df_implemented_answers_and_doi[
            PARAMETER
        ].values
    df_not_implemented_parameters = pd.DataFrame(
        {
            PARAMETER: [
                i
                for i in df_suggested_answes_and_doi[PARAMETER]
                if i not in list_implemented_answers_and_doi
            ],
            DOI: [
                df_suggested_answes_and_doi[DOI][i]
                for i in df_suggested_answes_and_doi.index
                if df_suggested_answes_and_doi[PARAMETER][i]
                not in list_implemented_answers_and_doi
            ],
        }
    )
    return df_not_implemented_parameters  # margin


COUNT = "count"


def assess_number_of_mentions(df_answers_with_doi, name, number_of_mentions=1):
    count_of_answers = collections.Counter(
        df_answers_with_doi[PARAMETER].values
    ).most_common(1000)
    count_of_answers = pd.DataFrame.from_records(
        count_of_answers, columns=[PARAMETER, COUNT]
    )
    if (
        CREATE_PLOTS is True
        and len(count_of_answers[count_of_answers[COUNT] > 1]) > number_of_mentions
    ):
        count_of_answers[count_of_answers[COUNT] > number_of_mentions].plot.barh(
            x=PARAMETER, y=COUNT
        )
        plt.savefig(RESULT_FOLDER + "/" + name + PNG, bbox_inches="tight")
        plt.close()

    # Retrieve all DOIs where word occurs
    count_of_answers[DOI] = [
        np.array2string(
            df_answers_with_doi[df_answers_with_doi[PARAMETER] == word][DOI].values,
            separator=", ",
        )[1:-1]
        for word in count_of_answers[PARAMETER]
    ]

    count_of_answers.to_csv(RESULT_FOLDER + "/" + name + CSV)
    print(
        f"The assessed papers are provide {len(count_of_answers.index)} different answers."
    )
    if PRINT_RESULT_SNIPPETS is True:
        if len(count_of_answers[count_of_answers["count"] > 1]) > 0:
            print(
                f"Answers occurring more then once are: {count_of_answers[count_of_answers['count']>1]}"
            )
        else:
            print(f"Answers mentioned once are: {count_of_answers}")
    return count_of_answers


def cross_answers(
    results, df_count_of_answers_with_doi, original_column, cross_column, name
):
    # Get list of all possible answers (single-choice)
    answer_options = [*set(results[columns[cross_column]].values)]
    # For all answer options
    for option in answer_options:
        # Get all papers that have the same answer
        all_papers_with_answer_option = results[
            results[columns[cross_column]] == option
        ]
        # Get count of papers that have the same answer and fullfill original condition
        # for example all papers dealing with energy justice in Germany
        number_of_papers_with_answer_combination = [
            sum(
                all_papers_with_answer_option[columns[original_column]]
                .str.contains(re.escape(word), case=False)
                .dropna()
            )
            for word in df_count_of_answers_with_doi[PARAMETER]
        ]
        # Add column of evaluated answer option with number of papers with both conditions
        df_count_of_answers_with_doi[option] = number_of_papers_with_answer_combination
    # Save to file
    df_count_of_answers_with_doi.to_csv(RESULT_FOLDER + "/" + name + CSV)
    return df_count_of_answers_with_doi


def connect_indicators_with_multiple_choice(results, assessed_column, name):
    group_list = {
        "Distributional-Justice": 59,
        "Procedual-Justice": 60,
        "Recognition-Justice": 61,
        "Restorative-Justice": 62,
        "Cosmopolitan-Justice": 63,
        "Intergenerational-Justice": 64,
    }
    df_answers_doi = get_all_answers_with_doi(
        results, column_number=assessed_column, sep=";"
    )
    assess_number_of_mentions(df_answers_doi, f"{name}")

    df_results_copy = pd.DataFrame(columns=results.columns)
    for paper in df_answers_doi.index:
        row = results[results[columns[1]] == df_answers_doi.loc[paper][DOI]]
        df_results_copy = pd.concat([df_results_copy, row], ignore_index=True)

    for key in group_list.keys():
        df_answers_doi[key] = df_results_copy[columns[group_list[key]]]

    df_answers_doi.to_csv(f"{RESULT_FOLDER}/{name}.csv")
    print(f"Saved as {RESULT_FOLDER}/{name}.csv")


# Print total number of papers
print(f"Number of evaluated papers: {len(results.index)}")
print(
    f"Number of papers that apply numeric model: {len(results[results[columns[48]] == 'Yes'].index)}"
)

# Create a seperate pd.Dataframe only with the Spatial Papers
spatial_papers = (
    pd.concat(
        [
            results[results[columns[3]].str.contains("atial")],
            results[results[columns[14]].str.contains("ATIAL")],
        ],
        ignore_index=True,
    )
    .drop_duplicates()
    .reset_index(drop=True)
)
spatial_papers.to_csv(RESULT_FOLDER + "/" + "only-spatial-papers.csv")
print(f"Number of spatial papers: {len(spatial_papers.index)}")
print(
    f"Number of spatial papers that apply numeric model: {len(spatial_papers[spatial_papers[columns[48]] == 'Yes'].index)}"
)
print(f"\n")

# Assess author-defined keywords
assessed_column = 2
print(f"Assessing column '{columns[assessed_column]}'")
df_answers_doi = get_all_answers_with_doi(results, column_number=assessed_column)
assess_number_of_mentions(
    df_answers_doi, name=f"{columns[assessed_column][:1]}-Author-defined-keywords"
)
print("\n")

# Assess sectoral focus and used indicators
assessed_column = 6
name = f"{columns[assessed_column][:1]}-Modelled-Sectors"
print(f"Assessing column '{columns[assessed_column]}'")
# Only assess for papers that apply models
connect_indicators_with_multiple_choice(
    results[results[columns[48]] == "Yes"], assessed_column, name
)
print("\n")

# Assess countries/cities:
assessed_column = 8
name = f"{columns[assessed_column][:1]}-Locations"
print(f"Assessing column '{columns[assessed_column]}'")
df_answers_doi = get_all_answers_with_doi(results, column_number=assessed_column)
df_count_of_answers_with_doi = assess_number_of_mentions(df_answers_doi, name=name)
cross_answers(
    results,
    df_count_of_answers_with_doi,
    original_column=assessed_column,
    cross_column=20,
    name=name,
)
print("\n")

# Assess scale and used indicators
assessed_column = 10
name = f"{columns[assessed_column][:1]}-Modelled-Scales"
print(f"Assessing column '{columns[assessed_column]}'")
# Only assess for papers that apply models
connect_indicators_with_multiple_choice(
    results[results[columns[48]] == "Yes"], assessed_column, name
)
print("\n")

# Assess scale and used indicators
assessed_column = 12
name = f"{columns[assessed_column][:1]}-Modelled-Time-Scales"
print(f"Assessing column '{columns[assessed_column]}'")
# Only assess for papers that apply models
connect_indicators_with_multiple_choice(
    results[results[columns[48]] == "Yes"], assessed_column, name
)
print("\n")


# Assess energy research fields and used indicators
assessed_column = 14
name = f"{columns[assessed_column][:1]}-Modelled-Energy-Research-Fields"
print(f"Assessing column '{columns[assessed_column]}'")
# Only assess for papers that apply models
connect_indicators_with_multiple_choice(
    results[results[columns[48]] == "Yes"], assessed_column, name
)
print("\n")

# Assess scale and used indicators
assessed_column = 20
name = f"{columns[assessed_column][:2]}-Modelled-Justice-Concepts"
print(f"Assessing column '{columns[assessed_column]}'")
# Only assess for papers that apply models
connect_indicators_with_multiple_choice(
    results[results[columns[48]] == "Yes"], assessed_column, name
)
print("\n")

# Assess mentioned input factors:
assessed_column = 44
print(f"Assessing column '{columns[assessed_column]}'")
df_answers_doi = get_all_answers_with_doi(results, column_number=assessed_column)
assess_number_of_mentions(
    df_answers_doi, name=f"{columns[assessed_column][:2]}-Input-Factors-Suggested"
)
print("\n")

# Assess mentioned output indicators:
assessed_column = 46
print(f"Assessing column '{columns[assessed_column]}'")
df_answers_doi = get_all_answers_with_doi(results, column_number=assessed_column)
assess_number_of_mentions(
    df_answers_doi, name=f"{columns[assessed_column][:2]}-Output-Indicators-Suggested"
)
print("\n")

# Assess analysed households types and used indicators
assessed_column = 52
name = f"{columns[assessed_column][:2]}-Modelled-Households"
print(f"Assessing column '{columns[assessed_column]}'")
# Only assess for papers that apply models
connect_indicators_with_multiple_choice(
    results[results[columns[48]] == "Yes"], assessed_column, name
)
print("\n")

# Assess used input factors:
assessed_column = 54
print(f"Assessing column '{columns[assessed_column]}'")
# Only get answers where a model is directly applied
df_answers_doi = get_all_answers_with_doi(
    results[results[columns[48]] == "Yes"], column_number=assessed_column
)
assess_number_of_mentions(
    df_answers_doi, name=f"{columns[assessed_column][:2]}-Input-Factors-Implemented"
)
print("\n")

# Assess used input factors only for spatial papers
assessed_column = 54
print(f"Assessing column '{columns[assessed_column]}' (spatial)")
# Only get answers where a model is directly applied
df_answers_doi = get_all_answers_with_doi(
    spatial_papers[spatial_papers[columns[48]] == "Yes"], column_number=assessed_column
)
assess_number_of_mentions(
    df_answers_doi,
    name=f"{columns[assessed_column][:2]}-Input-Factors-Implemented-Spatial",
)
print("\n")

# Assess margin between suggested and used input factors:
# I think this should be based on results[results[columns[48]==Yes]]. Papers with relevant content should be evaulated seperatrely.
print(f"Assessing input factors not implemented in models")
df_answers_doi = get_list_of_factors_not_implemented(
    results, column_number_suggested=44, column_number_implemented=54
)
assess_number_of_mentions(
    df_answers_doi, name=f"{columns[44][:2]}-Input-Factors-Not-Implemented"
)
print("\n")


def result_selection_string(result_selection):
    if len(result_selection) > 0:
        result_selection_suffix = f"-{result_selection}"
        result_selection_brackets = f" ({result_selection})"
    else:
        result_selection_suffix = ""
        result_selection_brackets = ""
    return result_selection_brackets, result_selection_suffix


def assessing_all_implemented_output_indicators(results, result_key=""):
    result_selection_brackets, result_selection_suffix = result_selection_string(
        result_key
    )
    # Assess used output factors, for which a justice dimension is not yet defined:
    assessed_column = 56
    print(f"Assessing column '{columns[assessed_column]}'{result_selection_brackets}")

    # Only get answers where a model is directly applied
    df_answers_doi = get_all_answers_with_doi(
        results[results[columns[48]] == "Yes"], column_number=assessed_column
    )
    assess_number_of_mentions(
        df_answers_doi,
        name=f"{columns[assessed_column][:2]}-Output-Factors-Implemented-Not-Attributed-To-J-Dimension{result_selection_suffix}",
    )
    print("\n")

    all_implemented_output_indicators = df_answers_doi[PARAMETER].values.tolist()

    # Assess used output indicators:
    list = {
        "Distributional-Justice": 59,
        "Procedual-Justice": 60,
        "Recognition-Justice": 61,
        "Restorative-Justice": 62,
        "Cosmopolitan-Justice": 63,
        "Intergenerational-Justice": 64,
    }

    for key in list.keys():
        assessed_column = list[key]
        print(
            f"Assessing column '{columns[assessed_column]}'{result_selection_brackets}"
        )
        # Only get answers where a model is directly applied
        df_answers_doi = get_all_answers_with_doi(
            results[results[columns[48]] == "Yes"], column_number=assessed_column
        )
        assess_number_of_mentions(
            df_answers_doi,
            name=f"{columns[assessed_column][:2]}-Output-Indicators-Implemented{result_selection_suffix}-{key}",
        )
        print("\n")
        all_implemented_output_indicators += df_answers_doi[PARAMETER].values.tolist()

    create_summary_csv(
        group_dict=list,
        name_root="-Output-Indicators-Implemented",
        result_selection_suffix=result_selection_suffix,
    )

    # Assess margin between suggested and used output indicators:
    # I think this should be based on results[results[columns[48]==Yes]]. Papers with relevant content should be evaulated seperatrely.
    print(
        f"Assessing output indicators not implemented in models{result_selection_brackets}"
    )
    df_answers_doi = get_list_of_factors_not_implemented(
        results,
        column_number_suggested=46,
        column_number_implemented=None,
        list_implemented_answers_and_doi=all_implemented_output_indicators,
    )
    assess_number_of_mentions(
        df_answers_doi,
        name=f"{columns[46][:2]}-Output-Indicators-Not-Implemented{result_selection_suffix}",
    )
    print("\n")


def create_summary_csv(group_dict, name_root, result_selection_suffix):
    dict_summary = {}
    rel_col = [PARAMETER, COUNT, DOI]
    max_len = 0
    for key in group_dict.keys():
        df_file = pd.read_csv(
            f"{RESULT_FOLDER}/{columns[group_dict[key]][:2]}{name_root}{result_selection_suffix}-{key}"
            + ".csv",
            usecols=rel_col,
        )
        for col in rel_col:
            dict_summary.update({(key, col): df_file[col].values.tolist()})
            if len(dict_summary[(key, col)]) > max_len:
                max_len = len(dict_summary[(key, col)])

    for key_len in dict_summary:
        while len(dict_summary[key_len]) <= max_len:
            dict_summary.update({key_len: dict_summary[key_len] + [None]})

    df_summary = pd.DataFrame(dict_summary)
    df_summary.to_csv(
        f"{RESULT_FOLDER}/{columns[group_dict[key]][:2]}{name_root}{result_selection_suffix}"
        + ".csv"
    )
    return


assessing_all_implemented_output_indicators(results)
assessing_all_implemented_output_indicators(spatial_papers, result_key="spatial")
import pprint

INDICATOR = "Indicator"


def create_table_for_indicators(results, columns):
    print("Creating table listing all output indicators as individual rows:")
    # Define rows in which GF question for justice dimension of indicators is defined in 00_googleform_code_2023-03-Survery-Literature-Review-Justice-in-Modelling-Final
    list_of_output_indicator_groups = {
        "Distributional-Justice": 59,
        "Procedual-Justice": 60,
        "Recognition-Justice": 61,
        "Restorative-Justice": 62,
        "Cosmopolitan-Justice": 63,
        "Intergenerational-Justice": 64,
    }
    # Define relevant information that is to be connected to individual indicators
    relevant_answers = [1, 2, 6, 8, 10, 12, 14, 20, 48, 52, 66, 76]
    relevant_columns = [columns[i] for i in relevant_answers]
    # Add columns for indicator name and the justice dimensions it adresses
    ATTRIBUTED_J_DIMENSION = "Which justice dimension is addressed?"
    relevant_columns = [INDICATOR] + relevant_columns + [ATTRIBUTED_J_DIMENSION]

    df_indicators = pd.DataFrame(columns=relevant_columns)
    # Go though all papers
    for paper in results.index:
        # Define a dict that stores all indicators of a paper (allows for easy changeing of answers)
        all_paper_indicators_dict = {}
        # Retrieve information that is specific to the paper, not the indicator
        paper_dict = {}
        for col in relevant_columns[1:-1]:
            paper_dict.update({col: results[col][paper]})
        # Go through all justice dimensions, ie. the different GF question-answer pairs
        for key in list_of_output_indicator_groups.keys():
            assessed_column = list_of_output_indicator_groups[key]
            # Only get answers where a model is directly applied
            list_of_answers = []
            # Check if any indicators are defined
            if (
                pd.isna(results[columns[assessed_column]][paper]) is False
                and len(results[columns[assessed_column]][paper]) > 1
            ):
                # derive seperate indicators from the list of indicators. All "," are interpreted to distinguish answers
                answer_string = results[columns[assessed_column]][paper] + ", "
                phrases_seperated_by_comma = [
                    ele for ele in answer_string.split(", ") if ele != ""
                ]
                list_of_answers += phrases_seperated_by_comma
                # Make lowercase to ease reading
                list_of_answers = [x.lower() for x in list_of_answers]
                # Create a dict that collects all information connected to the indicators of a specific paper
                indicator_dict = paper_dict.copy()
                indicator_dict.update({ATTRIBUTED_J_DIMENSION: key})
                for indicator in list_of_answers:
                    # check if indicator was also mentioned to address a different justice dimension
                    if indicator not in all_paper_indicators_dict.keys():
                        # Fist mention of the indicator in the analysed paper
                        indicator_dict.update({INDICATOR: indicator})
                        all_paper_indicators_dict.update(
                            {indicator: indicator_dict.copy()}
                        )
                    else:
                        # Indicator was already mentioned to address another justice dimension
                        # Update the justice dimension field with the new dimension
                        # This avoids indicator duplicates for a single paper
                        all_paper_indicators_dict[indicator].update(
                            {
                                ATTRIBUTED_J_DIMENSION: all_paper_indicators_dict[
                                    indicator
                                ][ATTRIBUTED_J_DIMENSION]
                                + ", "
                                + key
                            }
                        )
        # Create df from the dict and align with structure of df_indicators
        new_rows = pd.DataFrame(all_paper_indicators_dict).transpose()
        df_indicators = pd.concat([df_indicators, new_rows], ignore_index=True)
    # Store df_indicators to file. All gathered information on indicators can now be found in a database.
    df_indicators.to_csv(
        RESULT_FOLDER + "/0_Database_Output_Indicators_Implemented.csv"
    )


create_table_for_indicators(
    results, columns
)  # Should be either results[results[columns[48]] != "No"] or results[results[columns[48]] = "Yes"]


def get_methods_used_in_modelling_steps(result_selection, result_key=""):
    result_selection_brackets, result_selection_suffix = result_selection_string(
        result_key
    )

    list = {
        "storybuilding-narrative": 67,
        "scenario-building": 68,
        "parameterization": 69,
        "simulation-optimization": 70,
        "result-processing": 71,
        "discussion": 72,
    }

    for key in list.keys():
        assessed_column = list[key]
        print(f"Assessing column '{columns[list[key]]}'{result_selection_brackets}")
        # Only get answers where a model is directly applied
        df_answers_doi = get_all_answers_with_doi(
            result_selection[result_selection[columns[48]] == "Yes"],
            column_number=assessed_column,
        )
        file_name = (
            f"{columns[list[key]][:2]}-Used-Methods{result_selection_suffix}-{key}"
        )
        assess_number_of_mentions(df_answers_doi, name=file_name)

    create_summary_csv(
        group_dict=list,
        name_root="-Used-Methods",
        result_selection_suffix=result_selection_suffix,
    )
    print("\n")


# Assess mentioned methods that are not connected to the different modelling steps:
assessed_column = 50
print(f"Assessing column '{columns[assessed_column]}'")
df_answers_doi = get_all_answers_with_doi(
    results[results[columns[48]] == "Yes"], column_number=assessed_column
)
assess_number_of_mentions(
    df_answers_doi, name=f"{columns[assessed_column][:2]}-Used-Methods-Not-Defined-Step"
)
print("\n")

# Assess used methods indicators for all evaluated papers that use a numeric model
get_methods_used_in_modelling_steps(result_selection=results)
get_methods_used_in_modelling_steps(
    result_selection=spatial_papers, result_key="Spatial"
)
