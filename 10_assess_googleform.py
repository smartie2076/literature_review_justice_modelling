import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import collections

CREATE_PLOTS = True

FILENAME = "2023-01-31-Results-2022-11-23-Survery-Literature-Review-Justice-in-Modelling-Final"
CSV = ".csv"
PNG = ".png"

RESULT_FOLDER = "GoogleFormResults"

# Columns
column_file = "googleform_code"+CSV

print(column_file)

columns = pd.read_csv(column_file, header=None).squeeze("columns")
results = pd.read_csv(FILENAME + CSV)

'''
def get_all_answers_with_doi (results, column_number):
    string_of_answers = ""
    for paper in results.index:
        if pd.isna(results[columns[column_number]][paper]) is False and len(results[columns[column_number]][paper]) > 1:
            string_of_answers += results[columns[column_number]][paper] + ", "
    string_of_answers = string_of_answers[:-2]
    list_of_answers = [ele for ele in string_of_answers.split(", ") if ele != ""]
    list_of_answers = [x.lower() for x in list_of_answers]
    return list_of_answers
'''
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
    df_answers_doi = pd.DataFrame({"parameter": list_of_answers, "DOI": list_of_doi})
    return df_answers_doi

def get_list_of_fators_not_implemented (results, column_number_suggested, column_number_implemented):
    df_suggested_answes_and_doi = get_all_answers_with_doi(results=results, column_number=column_number_suggested)
    df_implemented_answers_and_doi = get_all_answers_with_doi(results=results, column_number=column_number_implemented)
    df_not_implemented_parameters = pd.DataFrame({
        "parameter": [i for i in df_suggested_answes_and_doi["parameter"] if i not in
                      df_implemented_answers_and_doi["parameter"].values],
        "DOI": [df_suggested_answes_and_doi["DOI"][i] for i in df_suggested_answes_and_doi.index if df_suggested_answes_and_doi["parameter"][i] not in df_implemented_answers_and_doi["parameter"].values]
    })

    return df_not_implemented_parameters # margin

#def get_doi_of_mentions(results, column_number):
import numpy as np
def assess_number_of_mentions(df_answers_with_doi, name):
    count_of_answers = collections.Counter(df_answers_with_doi["parameter"].values).most_common(1000)
    count_of_answers = pd.DataFrame.from_records(count_of_answers, columns=["word", "count"])
    if CREATE_PLOTS is True and len(count_of_answers[count_of_answers["count"]>1])>1:
        count_of_answers[count_of_answers["count"]>1].plot.barh(x="word", y="count")
        plt.savefig(RESULT_FOLDER+"/"+name+PNG)

    # Retrieve all DOIs where word occurs
    count_of_answers["DOI"] = [
        np.array2string(
            df_answers_with_doi[df_answers_with_doi["parameter"]==word]["DOI"].values,
            separator=", ")[1:-1]
        for word in count_of_answers["word"]]

    count_of_answers.to_csv(RESULT_FOLDER+"/"+name+CSV)
    print(f"The assessed papers are provide {len(count_of_answers.index)} different answers.")
    print(f"Answers occurring more then once are: {count_of_answers[count_of_answers['count']>1]}")
    return count_of_answers

# Assess author-defined keywords
assessed_column = 2
print (f"Assessing column '{columns[assessed_column]}'")
list_of_answers_and_doi = get_all_answers_with_doi(results, column_number=assessed_column)
assess_number_of_mentions(list_of_answers_and_doi, name=f"{columns[assessed_column][:1]}-Author-defined-keywords")
print("\n")

# Assess countries/cities:
assessed_column = 8
print (f"Assessing column '{columns[assessed_column]}'")
list_of_answers_and_doi = get_all_answers_with_doi(results, column_number=assessed_column)
assess_number_of_mentions(list_of_answers_and_doi, name=f"{columns[assessed_column][:1]}-Locations")
print("\n")

# Assess mentioned input factors:
assessed_column = 44
print (f"Assessing column '{columns[assessed_column]}'")
list_of_answers_and_doi = get_all_answers_with_doi(results, column_number=assessed_column)
assess_number_of_mentions(list_of_answers_and_doi, name=f"{columns[assessed_column][:2]}-Input-Factors-Suggested")
print("\n")

# Assess mentioned output indicators:
assessed_column = 46
print (f"Assessing column '{columns[assessed_column]}'")
list_of_answers_and_doi = get_all_answers_with_doi(results, column_number=assessed_column)
assess_number_of_mentions(list_of_answers_and_doi, name=f"{columns[assessed_column][:2]}-Output-Indicators-Suggested")
print("\n")

# Assess used input factors:
assessed_column = 54
print (f"Assessing column '{columns[assessed_column]}'")
# Only get answers where a model is directly applied
list_of_answers_and_doi = get_all_answers_with_doi(results[results[columns[48]] =="Yes"], column_number=assessed_column)
assess_number_of_mentions(list_of_answers_and_doi, name=f"{columns[assessed_column][:2]}-Input-Factors-Implemented")
print("\n")

# Assess used output indicators:
assessed_column = 56
print (f"Assessing column '{columns[assessed_column]}'")
# Only get answers where a model is directly applied
list_of_answers_and_doi = get_all_answers_with_doi(results[results[columns[48]] =="Yes"], column_number=assessed_column)
assess_number_of_mentions(list_of_answers_and_doi, name=f"{columns[assessed_column][:2]}-Output-Indicators-Implemented")
print("\n")

# Assess margin between suggested and used input factors:
# I think this should be based on results[results[columns[48]==Yes]]. Papers with relevant content should be evaulated seperatrely.
print (f"Assessing input factors not implemented in models")
list_of_answers_and_doi = get_list_of_fators_not_implemented(results, column_number_suggested=44, column_number_implemented=54)
assess_number_of_mentions(list_of_answers_and_doi, name=f"{columns[44][:2]}-Input-Factors-Not-Implemented")
print("\n")

# Assess margin between suggested and used output indicators:
# I think this should be based on results[results[columns[48]==Yes]]. Papers with relevant content should be evaulated seperatrely.
print (f"Assessing output indicators not implemented in models")
list_of_answers_and_doi = get_list_of_fators_not_implemented(results, column_number_suggested=46, column_number_implemented=56)
assess_number_of_mentions(list_of_answers_and_doi, name=f"{columns[46][:2]}-Output-Indicators-Not-Implemented")
print("\n")

# Assess mentioned input factors:
assessed_column = 50
print (f"Assessing column '{columns[assessed_column]}'")
list_of_answers_and_doi = get_all_answers_with_doi(results, column_number=assessed_column)
assess_number_of_mentions(list_of_answers_and_doi, name=f"{columns[assessed_column][:2]}-Used-Methods")
print("\n")