import pandas as pd
import os
import numpy as np
import sys
import matplotlib.pyplot as plt

intro = "Is the paper"

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


def assess_titles(data, inclusion_criteria_title):
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


def assess_title_and_abstract(
    data, inclusion_criteria_title, inclusion_criteria_title_and_abstract
):
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
    else:
        assessed_papers = 0
        left_to_assess_papers = (
            len(data.index) - data[inclusion_criteria_title[0]].sum()
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


def get_vote_on_paper(
    data,
    paper_id,
    output_file,
    primarily_assessed_inclusion_criteria,
    inclusion_criteria_title,
    inclusion_criteria_title_and_abstract,
    number_of_inclusion_criteria,
    target_value_of_inclusion_criteria,
    dict_options_inclusion_criteria_title_and_abstract,
    list_index_positive_vote,
    title=False,
):
    displayed_paper_info = False
    for i in range(0, len(primarily_assessed_inclusion_criteria)):
        skip = 0
        try:
            if (
                isinstance(
                    data.loc[paper_id, primarily_assessed_inclusion_criteria[i]],
                    np.bool_,
                )
                is True
                or isinstance(
                    data.loc[paper_id, primarily_assessed_inclusion_criteria[i]], bool
                )
                is True
            ):
                # Entries are read as np.bool_, and those do not pass the test here
                value = bool(
                    data.loc[paper_id, primarily_assessed_inclusion_criteria[i]]
                )
                # Check if the old file already included a vote on the inclusion criteria
                if value is True or value is False:
                    vote = data.loc[paper_id, primarily_assessed_inclusion_criteria[i]]
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
            elif (
                isinstance(
                    int(data.loc[paper_id, primarily_assessed_inclusion_criteria[i]]),
                    int,
                )
                is True
            ):
                vote = int(data.loc[paper_id, primarily_assessed_inclusion_criteria[i]])
                skip = 2
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
            vote = input(primarily_assessed_inclusion_criteria[i])
            valid_values = dict_options_inclusion_criteria_title_and_abstract[
                primarily_assessed_inclusion_criteria[i]
            ]
            if True in valid_values and vote in [
                "y",
                "yes",
                "Yes",
                "j",
                "ja",
                "t",
                "TRUE",
                "true",
                "True",
            ]:
                vote = True
                skip = 2
            elif False in valid_values and vote in [
                "n",
                "no",
                "No",
                "f",
                "FALSE",
                "false",
                "False",
            ]:
                vote = False
                skip = 2
            elif vote in ["p", "pass", "Pass"]:
                vote = None
                skip = 2
            elif vote in ["Exit", "Quit", "exit", "quit", "x", "q"]:
                save_and_quit(
                    output_file,
                    data,
                    inclusion_criteria_title,
                    inclusion_criteria_title_and_abstract,
                    dict_options_inclusion_criteria_title_and_abstract,
                    number_of_inclusion_criteria,
                    target_value_of_inclusion_criteria,
                    list_index_positive_vote,
                )
            elif (
                any([isinstance(x, int) for x in valid_values])
                and vote.isdigit()
                and int(vote) in valid_values
            ):
                vote = int(vote)
                skip = 2
            else:
                wrong_value_message = (
                    f"Wrong input {vote}. Valid values are: {valid_values}. "
                )
                if True in valid_values:
                    wrong_value_message += (
                        "You may use y/yes/Yes/j/ja/t/TRUE/true/True for True. "
                    )
                if False in valid_values:
                    wrong_value_message += (
                        "You may use n/no/No/f/FALSE/false/False for False. "
                    )
                wrong_value_message += "To skip the question use p/pass/Pass and to terminate the script, use Exit/exit/Quit/quit/x. If you use an invalid key again, you will skip automatically."
                print(wrong_value_message)
                skip += 1
                if skip == 2:
                    vote = None

        # Save vote to data frame
        data.loc[paper_id, primarily_assessed_inclusion_criteria[i]] = vote

    return displayed_paper_info


def save_and_quit(
    output_file,
    data,
    inclusion_criteria_title,
    inclusion_criteria_title_and_abstract,
    dict_options_inclusion_criteria_title_and_abstract,
    number_of_inclusion_criteria,
    target_value_of_inclusion_criteria,
    list_index_positive_vote,
):
    # In case of manual termination or end of data
    data.to_csv(output_file)
    print(f"Saved outputs to {output_file}.\n")
    assess_titles(data, inclusion_criteria_title)
    # Only works if all columns have already been created, ie. if all titles have been pre-selected already.
    assessed_papers, left_to_assess_papers = assess_title_and_abstract(
        data, inclusion_criteria_title, inclusion_criteria_title_and_abstract
    )
    if all([key in data.columns for key in inclusion_criteria_title_and_abstract]):
        # Include based on True/False criteria and overall target points
        criterium_target_value = [
            sum(
                [
                    data.loc[id, inclusion_criteria_title_and_abstract[i]]
                    for i in range(0, number_of_inclusion_criteria)
                ]
            )
            >= target_value_of_inclusion_criteria
            for id in data.index
        ]

        data["Include"] = criterium_target_value

        # Include based on max vote ("exceptional" performance for one of the criteria)
        for criteria in inclusion_criteria_title_and_abstract[
            0:number_of_inclusion_criteria
        ]:
            if (
                dict_options_inclusion_criteria_title_and_abstract[criteria]
                != [True, False]
                and dict_options_inclusion_criteria_title_and_abstract[criteria]
                != [False, True]
            ) and any(
                [
                    isinstance(x, int)
                    for x in dict_options_inclusion_criteria_title_and_abstract[
                        criteria
                    ]
                ]
            ):
                # Maximum reachable points
                maximum = max(
                    dict_options_inclusion_criteria_title_and_abstract[criteria]
                )
                criterium_maximum = [
                    data.loc[id, criteria] == maximum for id in data.index
                ]

                data["Include"] += criterium_maximum

        # Add papers that are included due to exceptional vote
        other_criterion = [
            data.loc[
                id, inclusion_criteria_title_and_abstract[list_index_positive_vote]
            ]
            == True
            for id in range(0, len(data.index))
        ]

        data["Include"] += other_criterion

        # Only write included papers to file (as we have a boolean column, adding True+True does not result in 2)
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
        # data.to_csv(output_file)
        # print(
        #    f"Saved outputs to {output_file}, including column 'Include'  und 'Assessed'.\n"
        # )

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

        plot_data.to_csv(output_file[:-4] + "_data_likelihood_of_relevance.csv")
        plt.savefig(output_file[:-4] + "_likelihood_of_relevance.png")

        print(
            f"Papers are relevant, if they fullfill the following inclusion criteria: "
            f"\n Does the title {inclusion_criteria_title[0]}, And does the paper... {inclusion_criteria_title_and_abstract[0:number_of_inclusion_criteria]} (or is included exceptionally: {inclusion_criteria_title_and_abstract[list_index_positive_vote]})."
        )
        print(
            f"Intermediate number of relevant papers: {sum(data['Include'])} ({round(sum(data['Include'])/assessed_papers*100,2)} % of assessed papers)"
        )
        print(
            f"Within those, intermediate number of positive-vetoed relevant papers: {data[inclusion_criteria_title_and_abstract[list_index_positive_vote]].sum()} ({round(data[inclusion_criteria_title_and_abstract[list_index_positive_vote]].sum()/assessed_papers*100,2)} % of assessed papers)"
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


def evaluate_title_and_abstract(
    file,
    output_file,
    inclusion_criteria_title,
    inclusion_criteria_title_and_abstract,
    dict_options_inclusion_criteria_title_and_abstract,
    number_of_inclusion_criteria,
    target_value_of_inclusion_criteria,
    list_index_positive_vote,
):
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
        assess_titles(data, inclusion_criteria_title)
        assess_title_and_abstract(
            data, inclusion_criteria_title, inclusion_criteria_title_and_abstract
        )
    except:
        pass

    for i in data.index:
        # Get vote on the paper title first
        get_vote_on_paper(
            data,
            paper_id=i,
            output_file=output_file,
            primarily_assessed_inclusion_criteria=inclusion_criteria_title,
            inclusion_criteria_title=inclusion_criteria_title,
            inclusion_criteria_title_and_abstract=inclusion_criteria_title_and_abstract,
            number_of_inclusion_criteria=number_of_inclusion_criteria,
            target_value_of_inclusion_criteria=target_value_of_inclusion_criteria,
            dict_options_inclusion_criteria_title_and_abstract=dict_options_inclusion_criteria_title_and_abstract,
            list_index_positive_vote=list_index_positive_vote,
            title=True,
        )

    count = 0
    for i in data.index:
        # If you want to skip to the less-relevant paper abstracts:
        # i += 1000
        # Makey sure that i does not increase over actual number of papers when skipping to higher numbers
        if i > len(data.index) - 1:
            save_and_quit(
                output_file,
                data,
                inclusion_criteria_title,
                inclusion_criteria_title_and_abstract,
                dict_options_inclusion_criteria_title_and_abstract,
                number_of_inclusion_criteria,
                list_index_positive_vote,
            )
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
                output_file=output_file,
                primarily_assessed_inclusion_criteria=inclusion_criteria_title_and_abstract,
                inclusion_criteria_title=inclusion_criteria_title,
                inclusion_criteria_title_and_abstract=inclusion_criteria_title_and_abstract,
                number_of_inclusion_criteria=number_of_inclusion_criteria,
                target_value_of_inclusion_criteria=target_value_of_inclusion_criteria,
                list_index_positive_vote=list_index_positive_vote,
                dict_options_inclusion_criteria_title_and_abstract=dict_options_inclusion_criteria_title_and_abstract,
            )
            if displayed_paper_info is True:
                count += 1

        if count == 10:
            print(
                f"\n \033[93m You reviewed 10 papers. Well done! Better save and restart now! \033[0m"
            )
            count = 0

    # Save and quit when program end is reached:
    save_and_quit(
        output_file,
        data,
        inclusion_criteria_title,
        inclusion_criteria_title_and_abstract,
        dict_options_inclusion_criteria_title_and_abstract,
        number_of_inclusion_criteria,
        target_value_of_inclusion_criteria,
        list_index_positive_vote,
    )


if __name__ == "__main__":
    main()
