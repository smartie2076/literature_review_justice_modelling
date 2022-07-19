import pandas as pd
import os
import sys

intro = "Is the paper"
inclusion_criteria_title = ["implying a relation with energy issues?"]

inclusion_criteria_title_and_abstract = [
    "dealing with energy supply?",
    "highlighting the relevance of justice in planning?",
    "investigating the impact of policies on consumers?"
    "offer a structurized approach via eg a model or framework?",
    "clearly stating at least one justice indicator?",
    "hinting at at least one relevant justice indicator?",
    "otherwise relevant for the paper?",
    "otherwise relevant for my PhD?",
    "otherwise relevant for people I know?"
]

exclusion = [""]

file = "2022-07-19-Final-Keywords-Publications-merged-Count.csv"
output_file = file[:-4] + "-votes.csv"

AUTHORS = "Authors"
YEAR = "Publication Year"
TITLE = "Article Title"
ABSTRACT = "Abstract"

KEYWORD_LIST = [
    "energ",
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
    "people",
    "minorit",
    "population",
    "communit",
    "justice",
    "equit",
    "equalit",
]
KEYWORD_LIST += [key.capitalize() for key in KEYWORD_LIST]


def bold_keys(string):
    for word in KEYWORD_LIST:
        string = string.replace(word, "\033[1m"+word+ '\033[0m')
    return string

def paper_author_year_title_abstract(data, paper_id, title):
    # Display paper info on screen
    print(f"\n {data[AUTHORS][paper_id]}")
    print(f"{data[YEAR][paper_id]}\n")
    print(f"{bold_keys(data[TITLE][paper_id])}\n")
    if title is False:
        print(f"{bold_keys(data[ABSTRACT][paper_id])}\n \n")
    print(intro)

def get_vote_on_paper(data, paper_id, inclusion_criteria, title = False):
    for i in range(0, len(inclusion_criteria)):
        skip = 0
        try:
            # Check if the old file already included a vote on the inclusion criteria
            if (
                data.loc[paper_id, inclusion_criteria[i]] is True
                or data.loc[paper_id, inclusion_criteria[i]] is False
            ):
                vote = data.loc[paper_id, inclusion_criteria[i]]
                skip = 2
            # If keywords from group energy services, pass title as relevant
            elif (title is True) and ("Energ" in data[TITLE][paper_id] or "energ" in data[TITLE][paper_id] or "electr" in data[TITLE][paper_id] or "Electr" in data[TITLE][paper_id] or "heat" in data[TITLE][paper_id] or "Heat" in data[TITLE][paper_id]):
                vote = True
                skip = 2
            else:
                # No value for inclusion criteria stored - print information to receive a vote
                paper_author_year_title_abstract(data, paper_id, title)
        except:
            # May happen if the column for the inclusion criteria does not exist jet
            paper_author_year_title_abstract(data, paper_id, title)

        # Get a vote on the inclusion criteria for the paper.
        # Valid inputs: Affirmative, Negative, Pass, Exit (premature script exit)
        # Ask one time for a correct entry, if the input was invalid, but add "vote=None" if the input was invalid twice
        while skip < 2:
            vote = input(inclusion_criteria[i])
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

        # Save vote to data frame
        data.loc[paper_id, inclusion_criteria[i]] = vote


def save_and_quit(data):
    # In case of manual termination or end of data
    data.to_csv(output_file)
    print(f"Saved outputs to {output_file}.")
    print(
        f"Number of assessed titles: {len(data.index) - data[inclusion_criteria_title[0]].isna().sum()}")
    print(
        f"Number of potentially relevant titles: {data[inclusion_criteria_title[0]].sum()}")

    # Only works if all columns have already been created, ie. if all titles have been pre-selected already.
    if all([key in data.columns for key in inclusion_criteria_title_and_abstract]):
        print(f"Number of assessed papers (estimate): {len(data.index)-data[inclusion_criteria_title_and_abstract[0]].isna().sum()}")
        print(
            f"Number of papers left to assess (estimate): {data[inclusion_criteria_title_and_abstract[0]].isna().sum()}"
        )
        data["Include"]=[sum([data.loc[id, inclusion_criteria_title_and_abstract[i]] for i in range(0, 6)]) == 6 for id in data.index]
        print(f"Papers are relevant, if they fullfill the following inclusion criteria: "
              f"\n Does the title {inclusion_criteria_title[0]} And does the paper... {inclusion_criteria_title_and_abstract[0:5]}.")
        print(f"Intermediate number of relevant papers: {sum(data['Include'])}")
        print(f"Intermediate number of otherwise relevant papers: f{sum(data[inclusion_criteria_title_and_abstract[6]])}")
    sys.exit()


def evaluate_title_and_abstract():
    data = pd.read_csv(file)
    print(f"Original number of literature to assess: {len(data.index)}")
    data_with_votes = pd.read_csv(output_file)
    data = data.merge(data_with_votes, how="left")
    print(
        f"Number of literature to assess after merge with old votes: {len(data.index)}"
    )
    try:
        print(
            f"Number of papers left to assess (approximately): {data[inclusion_criteria_title_and_abstract[0]].isna().sum()}"
        )
    except:
        pass

    for i in data.index:
        # Get vote on the paper title first
        get_vote_on_paper(data, paper_id=i, inclusion_criteria=inclusion_criteria_title, title = True)

    for i in data.index:
        # Only assess entry if title fullfills inclusion criteria for the title
        if data.loc[id, inclusion_criteria_title[0]] is True or data.loc[id, inclusion_criteria_title[0]] is None:
            # Assess the inclusion criteria for the abstract and title together
            get_vote_on_paper(data, paper_id=i, inclusion_criteria=inclusion_criteria_title_and_abstract)

evaluate_title_and_abstract()
