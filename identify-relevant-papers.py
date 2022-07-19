import pandas as pd
import matplotlib.pyplot as plt

files = [
    "2022-07-19-Final-Keywords-Publications-Part1.xls",
    "2022-07-19-Final-Keywords-Publications-Part2.xls",
]

result_file_name = "2022-07-19-Final-Keywords-Publications-merged"

keywords_search_string = [
    "energy",
    "electricit",
    "heat",
    "climate",
    "carbon",
    "sustainab",
    "renewable",
    "environment",
    "transition",
    "transformation",
    "development",
    "pathway",
    "strateg",
    "polic",
    "planning",
    "model",
    "indicator",
    "simulation",
    "optimi",
    "tool",
    "framework",
    "scenario",
    "consumer",
    "household",
    "prosumer",
    "soci",
    "population",
    "communit",
    "people",
    "minorit",
    "justice",
    "equit",
    "equality",
]
keywords_additional = []
keywords = keywords_search_string + keywords_additional

SEARCH_KEYS = "search-keys"
ADDITIONAL_KEYS = "additional-keys"

RELATIVE_COUNT = "Relative-Count"
COUNT = "Count"
TOTAL_COUNT = "Total-Count"
TITLE = "Article Title"
ABSTRACT = "Abstract"
HISTOGRAM = "Histogram"
WORD_COUNT = "Word_Count"

title_and_abstract = TITLE + " AND " + ABSTRACT


def read_file(filename):
    data = pd.DataFrame()

    for file in files:
        print(f"Reading from file {file}")
        file_data = pd.read_excel(file)
        data = pd.concat([data, file_data], ignore_index=True)

    print(f"Column titles: {data.columns}")
    print(data.head())
    print(f"Number of entries: {len(data.index)}")
    data.drop_duplicates([TITLE, ABSTRACT])
    print(f"Number of entries after removing duplicates: {len(data.index)}")

    return data


def get_keyword_string():
    keyword_string = ""
    for keyword in keywords:
        keyword_string += keyword + "|"
    keyword_string = keyword_string[:-1]
    print(f"Number of keywords: {len(keywords)}")
    return keyword_string


def counting_keyword_relevance(data, column):
    keyword_string = get_keyword_string()
    for keyword in keywords:
        data[COUNT + "-" + keyword] = data[column].str.count(keyword)
    data[TOTAL_COUNT] = data[column].str.count(keyword_string)
    data[TOTAL_COUNT + "-" + SEARCH_KEYS] = sum(
        data[COUNT + "-" + keyword] for keyword in keywords_search_string
    )
    data[TOTAL_COUNT + "-" + ADDITIONAL_KEYS] = sum(
        data[COUNT + "-" + keyword] for keyword in keywords_additional
    )
    return data


def process_counts_to_plots(data):
    # Word count
    data[f"{WORD_COUNT}-{title_and_abstract}"] = [
        len(str(data[title_and_abstract][i]).split()) for i in range(0, len(data.index))
    ]
    data[f"{WORD_COUNT}-{title_and_abstract}"].plot.hist(bins=20)
    plt.xlabel("Number of words in title and abstract")
    plt.ylabel("Number of papers")
    plt.savefig(f"./{result_file_name}-{HISTOGRAM}-{WORD_COUNT}.png")
    plt.close()

    # Absolute keyword incidence
    data[TOTAL_COUNT].plot.hist(bins=20)
    plt.xlabel("Count of keywords in title and abstract")
    plt.ylabel("Number of papers")
    plt.savefig(f"./{result_file_name}-{HISTOGRAM}-{TOTAL_COUNT}.png")
    plt.close()

    # Keyword incidence relative to word count
    data[RELATIVE_COUNT] = (
        data[TOTAL_COUNT] / data[f"{WORD_COUNT}-{title_and_abstract}"]
    )
    data[RELATIVE_COUNT].plot.hist(bins=20)
    plt.xlabel("Count of keywords in title and abstract, relative to word count")
    plt.ylabel("Number of papers")
    plt.savefig(f"./{result_file_name}-{HISTOGRAM}-{RELATIVE_COUNT}.png")
    plt.close()


def assess_relevance_of_papers():
    data = read_file(files)

    data[title_and_abstract] = data[TITLE] + data[ABSTRACT]

    data = counting_keyword_relevance(data, title_and_abstract)
    process_counts_to_plots(data)

    data = data.sort_values(by=[RELATIVE_COUNT], ascending=False, ignore_index=True)
    data.to_csv(f"{result_file_name}-{COUNT}.csv")


assess_relevance_of_papers()
