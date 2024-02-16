import matplotlib.pyplot as plt
from wordcloud import WordCloud
import numpy as np
import pandas as pd
import requests
import bibtexparser
import C13_assess_googlesheetDB as C



def plot_wordcloud(path_base, title, text):
    # Compare also: https://www.python-lernen.de/wordcloud-erstellen-python.htm
    # STOPWORDS.update(liste_der_unerwuenschten_woerter), now manually removed from string
    wordcloud = WordCloud(
        background_color="white", collocations=True,width=1600, height=800
    ).generate(text)
    plt.figure(figsize=(20, 10))
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.title(title)
    wordcloud_name = (
        path_base + "/" + "Wordcloud_" + title.replace(" ", "_") + ".png"
    )
    print(wordcloud_name)
    plt.savefig(wordcloud_name)
    plt.close()
    return

def add_metadata_based_on_doi(df, column_doi):
    for index, row in df.iterrows():
        url = "http://dx.doi.org/" + row[column_doi]
        headers = {"accept": "application/x-bibtex"}
        bibtex = requests.get(url, headers=headers).text
        bibjson = bibtexparser.loads(bibtex).entries
        if "DOI Not Found" not in bibtex:
            for key in ["author", "year", "title", "journal"]:
                try:
                    df.loc[index, key] = bibjson[0][key]
                except:
                    df.loc[index, key] = np.nan

    return df

def column_count_plot_store(df, path_base, keyword):
    df = get_all_answers_with_doi(df, keyword, sep=",", doi=False)
    df = df.value_counts().reset_index().rename(columns={0: keyword, 1: "count"})
    print(f"In total, {len(df.index)} {keyword} items are collected.")
    df.to_csv(path_base + f"/{keyword}"+C.CSV, index=False)
    df.plot(x=keyword, y="count", kind="bar")
    plt.savefig(path_base + f"/{keyword}"+C.PNG, bbox_inches="tight")
    plt.close()
    return df

def combine_dropdown_and_true_false(db, path_base, filename, dropdown_list_name, dropdown_list_choices,
                                    single_choice_list):
    df = pd.DataFrame(index=single_choice_list, columns=dropdown_list_choices)
    for dropdown_choice in df.columns:
        for single_choice in df.index:
            df.loc[single_choice, dropdown_choice] = len(
                db.loc[db[dropdown_list_name] == dropdown_choice].loc[db[single_choice] == 1].index)

    df.plot(kind="bar", stacked=True)
    plt.savefig(path_base + "/" + filename + ".png", bbox_inches="tight")
    plt.close()


def create_summary_csv(multiple_choice_list, path, name):
    dict_summary = {}
    max_len = 0
    for choice in multiple_choice_list:
        df_file = pd.read_csv(
            f"{path}/{name}-{choice.replace(' ', '-').replace('/', '-')}"
            + ".csv",
        )
        for col in df_file.columns:
            dict_summary.update({(choice, col): df_file[col].values.tolist()})
            if len(dict_summary[(choice, col)]) > max_len:
                max_len = len(dict_summary[(choice, col)])

    for key_len in dict_summary:
        while len(dict_summary[key_len]) <= max_len:
            dict_summary.update({key_len: dict_summary[key_len] + [None]})

    df_summary = pd.DataFrame(dict_summary)
    df_summary.to_csv(
        f"{path}/{name}-All"
        + ".csv",
        index=False
    )
    return

def get_all_answers_with_doi(df, column, sep=",", doi=True):
    list_of_answers = []
    list_of_doi = []

    for entry in df.index:
        if (
            pd.isna(df.loc[entry, column]) is False
            and len(df.loc[entry, column]) > 1
        ):
            answer_string = df[column][entry] + f"{sep} "
            answer_string.replace(f"{sep} ", sep)
            phrases_seperated_by_comma = [
                ele for ele in answer_string.split(sep) if ele != ""
            ]
            # Loop through removing spaces from first space of each string
            i = 0
            while i <2:
                i +=1
                for ele in range(0, len(phrases_seperated_by_comma)):
                    if phrases_seperated_by_comma[ele] != "":
                        if phrases_seperated_by_comma[ele][0] == " ":
                            phrases_seperated_by_comma[ele] = phrases_seperated_by_comma[ele][1:]

            phrases_seperated_by_comma = list(
                filter(lambda x: x != " " and x != "", phrases_seperated_by_comma)
            )
            list_of_answers += phrases_seperated_by_comma
            if doi is True:
                list_of_doi += [
                df[C.DOI][entry] for ele in phrases_seperated_by_comma
                ]
    list_of_answers = [x.lower() for x in list_of_answers]
    if doi is True:
        df_answers_doi = pd.DataFrame({column: list_of_answers, C.DOI: list_of_doi})
    else:
        df_answers_doi = pd.DataFrame({column: list_of_answers})
    return df_answers_doi

import collections
CREATE_PLOTS = False
def assess_number_of_mentions(df_answers_with_doi, keyword, name, path, number_of_mentions=1):
    df_answers_with_doi
    count_of_answers = collections.Counter(
        df_answers_with_doi[keyword].values
    ).most_common(1000)
    count_of_answers = pd.DataFrame.from_records(
        count_of_answers, columns=[keyword, C.COUNT]
    )

    # Retrieve all DOIs where word occurs
    doi_list = []
    number_doi = []
    for word in count_of_answers[keyword]:
        all_doi = df_answers_with_doi[df_answers_with_doi[keyword] == word][C.DOI].values
        doi_str = ""
        counter = 0
        for doi in all_doi:
            if doi not in doi_str:
                doi_str += doi + ", "
                counter += 1
        doi_list += [doi_str[:-2]]
        number_doi += [counter]

    count_of_answers[C.DOI] = doi_list
    count_of_answers[C.COUNT] = number_doi
    count_of_answers = count_of_answers.sort_values(by=C.COUNT, ascending=False)

    if (
        CREATE_PLOTS is True
        and len(count_of_answers[count_of_answers[C.COUNT] > 1]) > number_of_mentions
    ):
        count_of_answers[count_of_answers[C.COUNT] > number_of_mentions].plot.barh(
            x=keyword, y=C.COUNT
        )
        plt.savefig(path + "/" + name + ".png", bbox_inches="tight")
        plt.close()

    count_of_answers.to_csv(path + "/" + name + ".csv", index=False)
    return count_of_answers

def create_matrix_from_list_attributed_to_multiple_choice(df, path, name, column_with_list, multiple_choice_list):
    for choice in multiple_choice_list:
        df_answers_doi = get_all_answers_with_doi(
            df.loc[df[choice]==1],
            column = column_with_list,
        )
        file_name = name + "-" +choice.replace(" ", "-").replace("/", "-")
        assess_number_of_mentions(df_answers_doi, keyword=column_with_list,name=file_name, path=path)

    create_summary_csv(
        multiple_choice_list=multiple_choice_list,
        path=path,
        name=name
    )
    print("\n")



