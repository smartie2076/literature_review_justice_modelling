import re

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import collections

CREATE_PLOTS = True

FILENAME = "./2023-GoogleFormResults/2023-01-31-Results-2022-11-23-Survery-Literature-Review-Justice-in-Modelling-Final"
CSV = ".csv"
PNG = ".png"

PARAMETER = "parameter" #parameters/answer options
DOI = "doi"

RESULT_FOLDER = "2023-GoogleFormResults-Evaluation"

# Columns
column_file = "./2023-GoogleFormResults/00_googleform_code_2022-11-23-Survery-Literature-Review-Justice-in-Modelling-Final"

print(column_file)

columns = pd.read_csv(column_file+CSV, header=None).squeeze("columns")
results = pd.read_csv(FILENAME + CSV)

def get_all_answers_with_doi (results, column_number):
    list_of_answers = []
    list_of_doi = []
    for paper in results.index:
        if pd.isna(results[columns[column_number]][paper]) is False and len(results[columns[column_number]][paper]) > 1:
            answer_string = results[columns[column_number]][paper] + ", "
            phrases_seperated_by_comma = [ele for ele in answer_string.split(", ") if ele != ""]
            list_of_answers += phrases_seperated_by_comma
            list_of_doi += [results[columns[1]][paper] for ele in phrases_seperated_by_comma]
    list_of_answers = [x.lower() for x in list_of_answers]
    df_answers_doi = pd.DataFrame({PARAMETER: list_of_answers, DOI: list_of_doi})
    return df_answers_doi

def get_list_of_fators_not_implemented (results, column_number_suggested, column_number_implemented):
    df_suggested_answes_and_doi = get_all_answers_with_doi(results=results, column_number=column_number_suggested)
    df_implemented_answers_and_doi = get_all_answers_with_doi(results=results, column_number=column_number_implemented)
    df_not_implemented_parameters = pd.DataFrame({
        PARAMETER: [i for i in df_suggested_answes_and_doi[PARAMETER] if i not in
                      df_implemented_answers_and_doi[PARAMETER].values],
        DOI: [df_suggested_answes_and_doi[DOI][i] for i in df_suggested_answes_and_doi.index if df_suggested_answes_and_doi[PARAMETER][i] not in df_implemented_answers_and_doi[PARAMETER].values]
    })

    return df_not_implemented_parameters # margin

import numpy as np
def assess_number_of_mentions(df_answers_with_doi, name, number_of_mentions=1):
    count_of_answers = collections.Counter(df_answers_with_doi[PARAMETER].values).most_common(1000)
    count_of_answers = pd.DataFrame.from_records(count_of_answers, columns=[PARAMETER, "count"])
    if CREATE_PLOTS is True and len(count_of_answers[count_of_answers["count"]>1])>number_of_mentions:
        count_of_answers[count_of_answers["count"]>number_of_mentions].plot.barh(x=PARAMETER, y="count")
        plt.savefig(RESULT_FOLDER+"/"+name+PNG)

    # Retrieve all DOIs where word occurs
    count_of_answers[DOI] = [
        np.array2string(
            df_answers_with_doi[df_answers_with_doi[PARAMETER]==word][DOI].values,
            separator=", ")[1:-1]
        for word in count_of_answers[PARAMETER]]

    count_of_answers.to_csv(RESULT_FOLDER+"/"+name+CSV)
    print(f"The assessed papers are provide {len(count_of_answers.index)} different answers.")
    print(f"Answers occurring more then once are: {count_of_answers[count_of_answers['count']>1]}")
    return count_of_answers


def cross_answers (results, df_count_of_answers_with_doi, original_column, cross_column, name):
    # Get list of all possible answers (single-choice)
    answer_options = [*set(results[columns[cross_column]].values)]
    # For all answer options
    for option in answer_options:
        # Get all papers that have the same answer
        all_papers_with_answer_option = results[results[columns[cross_column]] == option]
        # Get count of papers that have the same answer and fullfill original condition
        # for example all papers dealing with energy justice in Germany
        number_of_papers_with_answer_combination = [
            sum(all_papers_with_answer_option[columns[original_column]].str.contains(re.escape(word), case=False).dropna()) for word
            in df_count_of_answers_with_doi[PARAMETER]]
        # Add column of evaluated answer option with number of papers with both conditions
        df_count_of_answers_with_doi[option] = number_of_papers_with_answer_combination
    # Save to file
    df_count_of_answers_with_doi.to_csv(RESULT_FOLDER+"/"+name+CSV)
    return df_count_of_answers_with_doi

# Assess author-defined keywords
assessed_column = 2
print (f"Assessing column '{columns[assessed_column]}'")
df_answers_doi = get_all_answers_with_doi(results, column_number=assessed_column)
assess_number_of_mentions(df_answers_doi, name=f"{columns[assessed_column][:1]}-Author-defined-keywords")
print("\n")

# Assess countries/cities:
assessed_column = 8
name = f"{columns[assessed_column][:1]}-Locations"
print (f"Assessing column '{columns[assessed_column]}'")
df_answers_doi = get_all_answers_with_doi(results, column_number=assessed_column)
df_count_of_answers_with_doi = assess_number_of_mentions(df_answers_doi, name=name)
cross_answers(results, df_count_of_answers_with_doi, original_column=assessed_column, cross_column=20, name=name)
print("\n")

# Assess mentioned input factors:
assessed_column = 44
print (f"Assessing column '{columns[assessed_column]}'")
df_answers_doi = get_all_answers_with_doi(results, column_number=assessed_column)
assess_number_of_mentions(df_answers_doi, name=f"{columns[assessed_column][:2]}-Input-Factors-Suggested")
print("\n")

# Assess mentioned output indicators:
assessed_column = 46
print (f"Assessing column '{columns[assessed_column]}'")
df_answers_doi = get_all_answers_with_doi(results, column_number=assessed_column)
assess_number_of_mentions(df_answers_doi, name=f"{columns[assessed_column][:2]}-Output-Indicators-Suggested")
print("\n")

# Assess used input factors:
assessed_column = 54
print (f"Assessing column '{columns[assessed_column]}'")
# Only get answers where a model is directly applied
df_answers_doi = get_all_answers_with_doi(results[results[columns[48]] == "Yes"], column_number=assessed_column)
assess_number_of_mentions(df_answers_doi, name=f"{columns[assessed_column][:2]}-Input-Factors-Implemented")
print("\n")

# Assess used output indicators:
assessed_column = 56
print (f"Assessing column '{columns[assessed_column]}'")
# Only get answers where a model is directly applied
df_answers_doi = get_all_answers_with_doi(results[results[columns[48]] == "Yes"], column_number=assessed_column)
assess_number_of_mentions(df_answers_doi, name=f"{columns[assessed_column][:2]}-Output-Indicators-Implemented")
print("\n")

# Assess margin between suggested and used input factors:
# I think this should be based on results[results[columns[48]==Yes]]. Papers with relevant content should be evaulated seperatrely.
print (f"Assessing input factors not implemented in models")
df_answers_doi = get_list_of_fators_not_implemented(results, column_number_suggested=44, column_number_implemented=54)
assess_number_of_mentions(df_answers_doi, name=f"{columns[44][:2]}-Input-Factors-Not-Implemented")
print("\n")

# Assess margin between suggested and used output indicators:
# I think this should be based on results[results[columns[48]==Yes]]. Papers with relevant content should be evaulated seperatrely.
print (f"Assessing output indicators not implemented in models")
df_answers_doi = get_list_of_fators_not_implemented(results, column_number_suggested=46, column_number_implemented=56)
assess_number_of_mentions(df_answers_doi, name=f"{columns[46][:2]}-Output-Indicators-Not-Implemented")
print("\n")

# Assess mentioned input factors:
assessed_column = 50
print (f"Assessing column '{columns[assessed_column]}'")
df_answers_doi = get_all_answers_with_doi(results[results[columns[48]] == "Yes"], column_number=assessed_column)
assess_number_of_mentions(df_answers_doi, name=f"{columns[assessed_column][:2]}-Used-Methods")
print("\n")