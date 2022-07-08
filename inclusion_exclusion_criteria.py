import pandas as pd

intro = "Is the paper"
inclusion = [
    "dealing with the energy transition?",
    "highlighting justice as a core aspect of planning?",
    "working with a model or framework?",
    "mentioning a relevant justice aspect?",
]

exclusion = [""]

file = "2022-06-10-webofscience-5-search-term-groups-no-transport-merged-Count.csv"
output_file = file[:-4] + "-votes.csv"

AUTHORS = "Authors"
YEAR = "Publication Year"
TITLE = "Article Title"
ABSTRACT = "Abstract"

# import only system from os
import os


def get_vote_on_paper(data, paper_id):
    os.system("cls")

    print(f"{data[AUTHORS][paper_id]}")
    print(f"{data[YEAR][paper_id]}\n")
    print(f"{data[TITLE][paper_id]}\n")
    print(f"{data[ABSTRACT][paper_id]}\n \n")
    print(intro)

    for i in range(0, len(inclusion)):
        skip = 0
        try:
            if (
                data.loc[paper_id, inclusion[i]] is True
                or data.loc[paper_id, inclusion[i]] is False
            ):
                vote = data.loc[paper_id, inclusion[i]]
                skip = 2
        except:
            pass

        while skip < 2:
            vote = input(inclusion[i])
            if vote in ["y", "yes", "j", "ja", "1", "TRUE", "true"]:
                vote = True
                skip = 2
            elif vote in ["n", "no", "0", "FALSE", "false"]:
                vote = False
                skip = 2
            elif vote in ["p", "pass"]:
                vote = None
                skip = 2
            elif vote in ["exit", "quit", "x", "q"]:
                save_and_quit(data)
            else:
                print(
                    f"Wrong input. Please use y/yes/j/ja/1/TRUE/true or n/no/0/FALSE/false or p/pass or exit/quit/x. If you use an invalid key again, you will skip automatically"
                )
                skip += 1
                if skip == 2:
                    vote = None

        data.loc[paper_id, inclusion[i]] = vote


def save_and_quit(data):
    data.to_csv(output_file)
    print(f"Saved outputs to {output_file}.")
    os._exit()


def evaluate_title_and_abstract():
    data = pd.read_csv(file)
    print(f"Original number of literature to assess: {len(data.index)}")
    data_with_votes = pd.read_csv(output_file)
    data = data.merge(data_with_votes, how="left")
    print(
        f"Number of literature to assess after merge with old votes: {len(data.index)}"
    )
    print(
        f"Number of papers left to assess (approximately): {data[inclusion[0]].isna().sum()}"
    )

    for i in data.index:
        get_vote_on_paper(data, paper_id=i)


evaluate_title_and_abstract()
