import matplotlib.pyplot as plt
from wordcloud import WordCloud
import numpy as np
import pandas as pd
import requests
import bibtexparser

def get_list_from_list_of_str(list_of_str, sep=","):
    list_of_answers = []
    for entry in list_of_str:
        if isinstance(entry, type(np.nan)) is False and entry != "-":
            answer_string = entry# + f"{sep} "
            answer_string.replace(f"{sep} ", sep)
            phrases_seperated_by_comma = [
                    ele for ele in answer_string.split(sep) if ele != ""
                ]
            for ele in range(0, len(phrases_seperated_by_comma)):
                if phrases_seperated_by_comma[ele][0] == " ":
                    phrases_seperated_by_comma[ele] = phrases_seperated_by_comma[ele][1:].capitalize()

            phrases_seperated_by_comma = list(
                    filter(lambda x: x != " ", phrases_seperated_by_comma)
                )
            list_of_answers += phrases_seperated_by_comma

    return list_of_answers
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
    list = get_list_from_list_of_str(df[keyword].values.tolist())
    if keyword == "Relevant cited papers":
        list = [i.replace(" ", "") for i in list]
    df = pd.DataFrame(list)
    df = df.value_counts().reset_index().rename(columns={0: keyword, 1: "count"})
    print(f"In total, {len(df.index)} {keyword} items are collected.")
    df.to_csv(path_base + f"/{keyword}.csv", index=False)
    df.plot(x=keyword, y="count", kind="bar")
    plt.savefig(path_base + f"/{keyword}.png", bbox_inches="tight")
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
