import pandas as pd
import os
import numpy as np
import sys
import matplotlib.pyplot as plt

intro = "Is the paper"
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


def assess_titles(data):
    assessed_titles = len(data.index) - data[inclusion_criteria_title[0]].isna().sum()
    print(
        f"Number of assessed titles: {assessed_titles} ({round(assessed_titles/len(data.index)*100,2)} % of titles)"
    )
    potentially_relevant_titles = data[inclusion_criteria_title[0]].sum()
    print(
        f"Number of potentially relevant titles: {potentially_relevant_titles} ({round(potentially_relevant_titles/assessed_titles*100,2)} % of assessed titles)"
    )
    print(
        f"Number of titles left to assess: {data[inclusion_criteria_title[0]].isna().sum()} ({round(data[inclusion_criteria_title[0]].isna().sum()/len(data.index)*100,2)} % of titles)\n"
    )


def assess_title_and_abstract(data):
    if all([key in data.columns for key in inclusion_criteria_title_and_abstract]):
        assessed_papers = (
            len(data.index)
            - data[inclusion_criteria_title_and_abstract[0]].isna().sum()
        )
        print(
            f"Number of assessed papers (estimate): {assessed_papers} ({round(assessed_papers/(data[inclusion_criteria_title[0]].sum())*100,2)} %)"
        )

        left_to_assess_papers = data[
            inclusion_criteria_title_and_abstract[0]
        ].isna().sum() - (len(data.index) - data[inclusion_criteria_title[0]].sum())
        print(
            f"Number of papers left to assess (estimate): {left_to_assess_papers} ({round(left_to_assess_papers/(data[inclusion_criteria_title[0]].sum())*100,2)} %)\n"
        )

    return assessed_papers, left_to_assess_papers


def bold_keys(string):
    for word in KEYWORD_LIST:
        string = string.replace(word, "\033[1m" + word + "\033[0m")
    return string


def paper_author_year_title_abstract(data, paper_id, title, displayed_paper_info):
    # Display paper info on screen
    if displayed_paper_info is False:

        print(f"\n {paper_id}. {data[AUTHORS][paper_id]} ({data[YEAR][paper_id]})\n")
        print(f"{bold_keys(str(data[TITLE][paper_id]))}\n")
        if title is False:
            print(f"{bold_keys(str(data[ABSTRACT][paper_id]))}\n \n")
        print(intro)
        displayed_paper_info = True

    return displayed_paper_info


def get_vote_on_paper(data, paper_id, inclusion_criteria, title=False):
    displayed_paper_info = False
    for i in range(0, len(inclusion_criteria)):
        skip = 0
        try:
            if (
                isinstance(data.loc[paper_id, inclusion_criteria[i]], np.bool_) is True
                or isinstance(data.loc[paper_id, inclusion_criteria[i]], bool) is True
            ):
                # Entries are read as np.bool_, and those do not pass the test here
                value = bool(data.loc[paper_id, inclusion_criteria[i]])
                # Check if the old file already included a vote on the inclusion criteria
                if value is True or value is False:
                    vote = data.loc[paper_id, inclusion_criteria[i]]
                    skip = 2
                # If keywords from group energy services, pass title as relevant
                elif (title is True) and (
                    "Energ" in data[TITLE][paper_id]
                    or "energ" in data[TITLE][paper_id]
                    or "electr" in data[TITLE][paper_id]
                    or "Electr" in data[TITLE][paper_id]
                    or "heat" in data[TITLE][paper_id]
                    or "Heat" in data[TITLE][paper_id]
                ):
                    vote = True
                    skip = 2
                else:
                    # No value for inclusion criteria stored - print information to receive a vote
                    displayed_paper_info = paper_author_year_title_abstract(
                        data, paper_id, title, displayed_paper_info
                    )
            else:
                # No value for inclusion criteria stored - print information to receive a vote
                displayed_paper_info = paper_author_year_title_abstract(
                    data, paper_id, title, displayed_paper_info
                )
        except:
            # May happen if the column for the inclusion criteria does not exist jet
            displayed_paper_info = paper_author_year_title_abstract(
                data, paper_id, title, displayed_paper_info
            )

        # Get a vote on the inclusion criteria for the paper.
        # Valid inputs: Affirmative, Negative, Pass, Exit (premature script exit)
        # Ask one time for a correct entry, if the input was invalid, but add "vote=None" if the input was invalid twice
        while skip < 2:
            vote = input(inclusion_criteria[i])
            if vote in ["y", "yes", "Yes", "j", "ja", "1", "TRUE", "true"]:
                vote = True
                skip = 2
            elif vote in ["n", "no", "No", "0", "FALSE", "false"]:
                vote = False
                skip = 2
            elif vote in ["p", "pass", "Pass"]:
                vote = None
                skip = 2
            elif vote in ["Exit", "Quit", "exit", "quit", "x", "q"]:
                save_and_quit(data)
            else:
                print(
                    f"Wrong input. Please use y/yes/Yes/j/ja/1/TRUE/true or n/no/No/0/FALSE/false or p/pass/Pass or Exit/exit/Quit/quit/x. If you use an invalid key again, you will skip automatically"
                )
                skip += 1
                if skip == 2:
                    vote = None

        # Save vote to data frame
        data.loc[paper_id, inclusion_criteria[i]] = vote

    return displayed_paper_info


def save_and_quit(data):
    # In case of manual termination or end of data
    data.to_csv(output_file)
    print(f"Saved outputs to {output_file}.\n")
    assess_titles(data)
    # Only works if all columns have already been created, ie. if all titles have been pre-selected already.
    assessed_papers, left_to_assess_papers = assess_title_and_abstract(data)
    if all([key in data.columns for key in inclusion_criteria_title_and_abstract]):
        data["Include"] = [
            sum(
                [
                    data.loc[id, inclusion_criteria_title_and_abstract[i]]
                    for i in range(0, 6)
                ]
            )
            == 5
            for id in data.index
        ]
        # Add papers that are included due to exceptional vote
        other_criterion = [
            data.loc[id, inclusion_criteria_title_and_abstract[7]] == True
            for id in range(0, len(data.index))
        ]
        data["Include"] += other_criterion
        data[data["Include"] == True].to_csv(output_file[:-4] + "-only-included.csv")
        print(
            f"Saved list of relevant papers to {output_file[:-4]}-only-included.csv. \n"
        )
        relevant_papers = data["Include"].sum()

        # All titles that were discharged are assessed
        data["Assessed"] = ~data[inclusion_criteria_title]

        # All titles+abstracts that were assessed dont have any "NaN" left in the inclusion criteria columns
        overall_vote = data[inclusion_criteria_title_and_abstract].dropna()
        overall_vote["Assessed"] = True
        data["Assessed"] += overall_vote["Assessed"].reindex(
            data.index, fill_value=False
        )

        plot_data = pd.DataFrame(
            {
                "All inclusion criteria fullfilled": data["Include"].values.astype(
                    float
                ),
                "Energy relation of title": data[
                    inclusion_criteria_title[0]
                ].values.astype(float),
                "Paper ID": data.index.tolist(),
                "Finished assessment": data["Assessed"],
            }
        )

        # Get likelihood of a paper to be selected as relevant in a bin
        bins = 25
        plot_data = plot_data.rolling(bins).mean()
        plot_data = plot_data.iloc[::bins, :]

        # Plot likelihood - ideally this likelyhood decreases with the Paper ID
        # As this would indicate that my relevance ranking is working correctly
        plot_data.plot(
            x="Paper ID",
            y=[
                "All inclusion criteria fullfilled",
                "Energy relation of title",
                "Finished assessment",
            ],
            title=f"Relevance likelihood depending on Paper ID \n (bins of {bins}, assessed: {assessed_papers}, relevant: {relevant_papers})",
            xlabel="Paper ID, ranked by relevance with own algorithm",
            ylabel=f"Percentage of papers",
            style=["o", "o", "-"],
        )

        plot_data.to_csv("./data_likelihood_of_relevance.csv")
        plt.savefig("./likelihood_of_relevance.png")

        print(
            f"Papers are relevant, if they fullfill the following inclusion criteria: "
            f"\n Does the title {inclusion_criteria_title[0]} And does the paper... {inclusion_criteria_title_and_abstract[0:5]}."
        )
        print(
            f"Intermediate number of relevant papers: {sum(data['Include'])} ({round(sum(data['Include'])/assessed_papers*100,2)} % of assessed papers)"
        )
        print(
            f"Within those, intermediate number of otherwise relevant papers: {data[inclusion_criteria_title_and_abstract[6]].sum()} ({round(data[inclusion_criteria_title_and_abstract[6]].sum()/assessed_papers*100,2)} % of assessed papers)"
        )

    sys.exit()


def check_duplicates(data):
    print("\n Checking for duplicates based on DOI or Title independently:")
    duplicated = data["DOI"].duplicated() + data[TITLE].duplicated()
    duplicated = duplicated[duplicated == True]
    number_of_potential_duplicates = 0
    for item in duplicated.index:
        if isinstance(data.loc[item, "DOI"], str):
            print(
                f"Possible duplicate: {data.loc[item, AUTHORS]} with DOI {data.loc[item,'DOI']}"
            )
            number_of_potential_duplicates += 1

    print(
        f"It is possible that there are {number_of_potential_duplicates} duplicates in the input file. \n"
    )


def evaluate_title_and_abstract():
    data = pd.read_csv(file)
    print(f"Original number of literature to assess: {len(data.index)}")
    data_with_votes = pd.read_csv(output_file)
    data = data.merge(data_with_votes, how="left")
    data.drop(
        data.columns[data.columns.str.contains("unnamed", case=False)],
        axis=1,
        inplace=True,
    )

    print(
        f"Number of literature to assess after merge with old votes: {len(data.index)}"
    )

    try:
        check_duplicates(data)
        assess_titles(data)
        assess_title_and_abstract(data)
    except:
        pass

    for i in data.index:
        # Get vote on the paper title first
        get_vote_on_paper(
            data, paper_id=i, inclusion_criteria=inclusion_criteria_title, title=True
        )

    count = 0
    for i in data.index:
        # If you want to skip to the less-relevant paper abstracts:
        # i += 1700
        # Boolean values stored as np.bool_
        try:
            value = bool(data.loc[i, inclusion_criteria_title[0]])
        except:
            value = None
            print(
                f"The title inclusion criteria of paper {data.loc[i,TITLE]} is None, as DataFrame returns {data.loc[i, inclusion_criteria_title[0]]}."
            )

        # Only assess entry if title fullfills inclusion criteria for the title
        if value is True or value is None:
            # Assess the inclusion criteria for the abstract and title together
            displayed_paper_info = get_vote_on_paper(
                data,
                paper_id=i,
                inclusion_criteria=inclusion_criteria_title_and_abstract,
            )
            if displayed_paper_info is True:
                count += 1

        if count == 10:
            print(
                f"\n \033[93m You reviewed 10 papers. Well done! Better save and restart now! \033[0m"
            )
            count = 0

    # Save and quit when program end is reached:
    save_and_quit(data)


evaluate_title_and_abstract()
