import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

TOTAL_POINTS = "Total of 2nd Screening Points"
target_value = 13  # At least two points in each
exceptionality = 6  # min 5, ie. one of two voted exceptionality

file_core = (
    "2022-07-19-Final-Keywords-1st-Screening-Jonathan-Martha-Evaluation/2022-07-19-Final-Keywords-Publications-merged-Count-votes-only-included.csv"
)
output_file = file_core[:-4] + "-2nd-screening"

files = [output_file + "-m.csv", output_file + "-j.csv"]

inclusion_criteria_title_and_abstract = [
    "Does the paper define justice indicators? (0=nope, 1=probably/on the side, 2=yes, 3=exeptional)",
    "Does the paper implement justice indicators? (0=nope, 1=probably/on the side, 2=yes, 3=exeptional)",
    "Does the paper assess injustices between different defined groups? (0=nope, 1=probably/on the side, 2=yes, 3=exeptional)",
    "Is the paper describing justice in (1) a numerical approach, (2) a theoretical framework or (3) with other means?",
    "Which topic does the paper mainly address? (1) regional equity (eg. carbon emissions), (2) carbon pricing or tax, (3) SDG, (4) electrification, (5) the water-energy-nexus, (6) energy transition (7) policy, (8) data science/correlation or (9) else.",
    "Who might be interested in the paper? (1) Martha (local/consumer), (2) Jonathan (national), (3) Luisa (heat/sufficiency), (4) Alex (theory), (5) any.",
    "Paper must be included! (Veto)",
    "Paper is included based on the veto above, but is only relevant for the backgroud section.",
    "Discussion/2nd opinion necessary.",
]
'''
# Read from file and drop all without a vote in the relevant criteria
data_with_votes_m = pd.read_csv(files[0])
data_with_votes_m.dropna(
    subset=[inclusion_criteria_title_and_abstract[i] for i in range(0, 3)]
)
data_with_votes_j = pd.read_csv(files[1]).dropna(
    subset=[inclusion_criteria_title_and_abstract[i] for i in range(0, 3)]
)

for i in inclusion_criteria_title_and_abstract:
    data_with_votes_m.rename(columns={i: i + "(M)"}, inplace=True)
    data_with_votes_j.rename(columns={i: i + "(J)"}, inplace=True)

data_with_votes_joined = data_with_votes_m.merge(data_with_votes_j, how="left")
#data_with_votes_joined = data_with_votes_joined.dropna(
#    subset=[inclusion_criteria_title_and_abstract[i] + "(M)" for i in range(0, 3)]
#    + [inclusion_criteria_title_and_abstract[i] + "(J)" for i in range(0, 3)]
#)
'''
file_core = "2023-01-3rd-Screening-Paper-Screening/2023-01-24-Relevant-Papers-All-Data-Revoted.csv"
output_file = file_core[:-4] + "_3rd_screening"
data_with_votes_joined = pd.read_csv(file_core)
to_be_assessed = len(data_with_votes_joined)

def title_multirow(text):
    letters_in_line = 60
    i = 0
    while i + letters_in_line < len(text):
        text = text[: i + letters_in_line] + " \n " + text[i + letters_in_line :]
        i += letters_in_line
    return text


for criteria_number in range(0, 3, 1):
    title = title_multirow(inclusion_criteria_title_and_abstract[criteria_number])
    data_with_votes_joined[
        inclusion_criteria_title_and_abstract[criteria_number] + "(sum)"
    ] = (
        data_with_votes_joined[
            inclusion_criteria_title_and_abstract[criteria_number] + "(M)"
        ]
        + data_with_votes_joined[
            inclusion_criteria_title_and_abstract[criteria_number] + "(J)"
        ]
    )
    data_with_votes_joined[
        inclusion_criteria_title_and_abstract[criteria_number] + "(sum)"
    ].value_counts().sort_index().plot(kind="bar", title=title)
    plt.tight_layout()
    if criteria_number == 0:
        suffix = "_disribution_vote_definition_indicators"
    elif criteria_number == 1:
        suffix = "_disribution_vote_application_indicators"
    elif criteria_number == 2:
        suffix = "_disribution_vote_recognition_groups"
    else:
        print("Invalid criteria number range.")

    plt.savefig("./" + file_core[:-4] + suffix + "-joined" + ".png")
    plt.close()

data_with_votes_joined[TOTAL_POINTS] = sum(
    [
        data_with_votes_joined[
            inclusion_criteria_title_and_abstract[criteria_number] + "(sum)"
        ]
        for criteria_number in range(0, 3)
    ]
)
data_with_votes_joined[TOTAL_POINTS].value_counts().sort_index().plot(
    kind="bar",
    title=f"Total of 2nd Screening Points \n ({len(data_with_votes_joined)}/{round((len(data_with_votes_joined)/to_be_assessed)*100,2)}% assessed)",
)
plt.savefig("./" + file_core[:-4] + "-total-points" + "-joined" + ".png")
plt.close()

data_with_votes_joined["Large Voting Gap"] = [
    abs(
        data_with_votes_joined.loc[id, inclusion_criteria_title_and_abstract[0] + "(M)"]
        - data_with_votes_joined.loc[
            id, inclusion_criteria_title_and_abstract[0] + "(J)"
        ]
    )
    >= 2
    for id in data_with_votes_joined.index
]
data_with_votes_joined["Large Voting Gap"] += [
    abs(
        data_with_votes_joined.loc[id, inclusion_criteria_title_and_abstract[1] + "(M)"]
        - data_with_votes_joined.loc[
            id, inclusion_criteria_title_and_abstract[1] + "(J)"
        ]
    )
    >= 2
    for id in data_with_votes_joined.index
]
data_with_votes_joined["Large Voting Gap"] += [
    abs(
        data_with_votes_joined.loc[id, inclusion_criteria_title_and_abstract[2] + "(M)"]
        - data_with_votes_joined.loc[
            id, inclusion_criteria_title_and_abstract[2] + "(J)"
        ]
    )
    >= 2
    for id in data_with_votes_joined.index
]

print(
    f"\nNumber of papers with large voting gap: {sum(data_with_votes_joined['Large Voting Gap'])}"
)
large_voting_gap = data_with_votes_joined[
    data_with_votes_joined["Large Voting Gap"] == True
]
print(f"Following papers should be discussed:")
print(large_voting_gap["Article Title"])

print(
    f"\nAdditionally, following papers were marked as {inclusion_criteria_title_and_abstract[8]}:"
)
data_with_votes_joined["TBD"] = (
    data_with_votes_joined[inclusion_criteria_title_and_abstract[8] + "(M)"]
    + data_with_votes_joined[inclusion_criteria_title_and_abstract[8] + "(J)"]
)
tbd = data_with_votes_joined[data_with_votes_joined["TBD"] == True]
print(tbd["Article Title"])


def get_relevant_papers(
    data_with_votes_joined, target_value, exceptionality, save=False
):
    INCLUDE = "Include"
    SUFFIX_POINTS = "_points"

    """
    Order of relevance:
    Exceptionality > Total Points > Vetoed Twice > Vetoed Once"""

    ### DETERMINE ALL PAPERS THAT ARE INCLUDED AS BOTH OF US SAID THAT THEY ARE EXCEPTIONAL ###
    INCLUDED_EXCEPTIONAL = "Include_only_due_to_univocal_exceptionality"
    data_with_votes_joined[INCLUDED_EXCEPTIONAL] = [
        False for i in data_with_votes_joined.index
    ]

    # Include based on max vote ("exceptional" performance for one of the criteria)
    for criteria in inclusion_criteria_title_and_abstract[0:3]:
        criterium_maximum = [
            data_with_votes_joined.loc[id, criteria + "(sum)"] >= exceptionality
            for id in data_with_votes_joined.index
        ]
        data_with_votes_joined[INCLUDED_EXCEPTIONAL] += criterium_maximum

    data_with_votes_joined[INCLUDE] = data_with_votes_joined[INCLUDED_EXCEPTIONAL]

    print(sum(data_with_votes_joined[INCLUDED_EXCEPTIONAL]))
    data_with_votes_joined[INCLUDED_EXCEPTIONAL + SUFFIX_POINTS] = (
        data_with_votes_joined[INCLUDED_EXCEPTIONAL]
        * data_with_votes_joined[TOTAL_POINTS]
    )

    ### DETERMINE ALL PAPERS THAT ARE SO RELEVANT THAT THEY GOT THE TARGET VALUE OF POINTS ###

    INCLUDED_TARGET_VALUE = "Include_due_to_target_value_points"
    # Include based on True/False criteria and overall target points
    criterium_target_value = [
        data_with_votes_joined.loc[id, INCLUDED_EXCEPTIONAL] == False
        and data_with_votes_joined.loc[id, TOTAL_POINTS]
        >= target_value  # At least one of us has to have voted 3
        for id in data_with_votes_joined.index
    ]
    data_with_votes_joined[INCLUDED_TARGET_VALUE] = criterium_target_value
    data_with_votes_joined[INCLUDED_TARGET_VALUE + SUFFIX_POINTS] = (
        data_with_votes_joined[TOTAL_POINTS]
        * data_with_votes_joined[INCLUDED_TARGET_VALUE]
    )

    data_with_votes_joined[INCLUDE] += criterium_target_value

    all_relevant_papers_only_double_vote = data_with_votes_joined[INCLUDE]

    # Add papers that are included due to exceptional vote
    vetoes_martha = [
        data_with_votes_joined.loc[id, inclusion_criteria_title_and_abstract[6] + "(M)"]
        == True
        for id in data_with_votes_joined.index
    ]
    data_with_votes_joined[INCLUDE] += vetoes_martha

    vetoes_jonathan = [
        data_with_votes_joined.loc[id, inclusion_criteria_title_and_abstract[6] + "(J)"]
        == True
        for id in data_with_votes_joined.index
    ]
    data_with_votes_joined[INCLUDE] += vetoes_jonathan

    INCLUDED_DOUBLE_VETO = "Included_only_due_to_double_veto"
    data_with_votes_joined["Double_veto"] = [
        vetoes_martha[i] * vetoes_jonathan[i] for i in range(0, len(vetoes_jonathan))
    ]
    #(len(vetoes_jonathan), len(data_with_votes_joined[INCLUDED_EXCEPTIONAL].values))
    #print(data_with_votes_joined[INCLUDED_EXCEPTIONAL].index.values)
    #print(data_with_votes_m.iloc[139])
    data_with_votes_joined[INCLUDED_DOUBLE_VETO] = [
        (data_with_votes_joined.loc[i, INCLUDED_EXCEPTIONAL] is False
        and data_with_votes_joined.loc[i, INCLUDED_TARGET_VALUE] is False
        and vetoes_martha[i] is True
        and vetoes_jonathan[i] is True)
        for i in range(0, len(vetoes_jonathan))
    ]
    data_with_votes_joined["Double_veto" + SUFFIX_POINTS] = (
        data_with_votes_joined[TOTAL_POINTS] * data_with_votes_joined["Double_veto"]
    )
    data_with_votes_joined[INCLUDED_DOUBLE_VETO + SUFFIX_POINTS] = (
        data_with_votes_joined[TOTAL_POINTS]
        * data_with_votes_joined[INCLUDED_DOUBLE_VETO]
    )
    vetoes_two = sum(data_with_votes_joined[INCLUDED_DOUBLE_VETO])

    INCLUDED_SINGLE_VETO = "Included_only_due_to_single_veto"
    data_with_votes_joined["Single_veto"] = [
        (vetoes_martha[i] == True and vetoes_jonathan[i] == False)
        or (vetoes_martha[i] == False and vetoes_jonathan[i] == True)
        for i in range(0, len(vetoes_jonathan))
    ]
    data_with_votes_joined["Single_veto" + SUFFIX_POINTS] = (
        data_with_votes_joined[TOTAL_POINTS] * data_with_votes_joined["Single_veto"]
    )
    data_with_votes_joined[INCLUDED_SINGLE_VETO] = [
        data_with_votes_joined.loc[i, INCLUDED_EXCEPTIONAL] == False
        and data_with_votes_joined.loc[i, INCLUDED_TARGET_VALUE] == False
        and (
            (vetoes_martha[i] == True and vetoes_jonathan[i] == False)
            or (vetoes_martha[i] == False and vetoes_jonathan[i] == True)
        )
        for i in range(0, len(vetoes_jonathan))
    ]
    data_with_votes_joined[INCLUDED_SINGLE_VETO + SUFFIX_POINTS] = (
        data_with_votes_joined[TOTAL_POINTS]
        * data_with_votes_joined[INCLUDED_SINGLE_VETO]
    )

    vetoes_one = sum(data_with_votes_joined[INCLUDED_SINGLE_VETO])

    all_relevant_papers_only_double_vote += vetoes_two
    relevant_papers_two_vetoes = all_relevant_papers_only_double_vote.sum()
    number_of_relevant_papers = data_with_votes_joined[INCLUDE].sum()

    # Only write included papers to file (as we have a boolean column, adding True+True does not result in 2)
    if save is True:
        data_with_votes_joined.to_csv(output_file + "-all-joined.csv")

        data_relevant_papers = data_with_votes_joined[
            data_with_votes_joined[INCLUDE] == True
        ]
        data_relevant_papers.to_csv(output_file + "-only-included-joined.csv")

        get_inclusion_kinds(
            data_relevant_papers,
            INCLUDE,
            SUFFIX_POINTS,
            INCLUDED_EXCEPTIONAL,
            INCLUDED_TARGET_VALUE,
            INCLUDED_DOUBLE_VETO,
            INCLUDED_SINGLE_VETO,
        )

        print(
            f"Saved list of relevant papers to {output_file[:-4]}-only-included-joined.csv. \n"
        )

        print(
            f"Number of relevant papers: \n"
            f"  Exceptional (sum of points {exceptionality}): {sum(data_with_votes_joined[INCLUDED_EXCEPTIONAL])}\n"
            f"+ More then {target_value} points: {sum(data_with_votes_joined[INCLUDED_TARGET_VALUE])}\n"
            f"+ Vetoed in twice: {vetoes_two}\n"
            f"+ Vetoed in once: {vetoes_one}\n"  # Vetos of each individual count, ie. not two vetos required to include the paper
            f"= Total relevant papers: {number_of_relevant_papers} (of {len(data_with_votes_joined)} papers / ({round(number_of_relevant_papers/len(data_with_votes_joined)*100,1)}) %)"
            f"(Total relevant papers if only two vetoes valid: {relevant_papers_two_vetoes}"
        )

        TITLE = "Article Title"
        ABSTRACT = "Abstract"
        AUTHORS = "Authors"

        string_title = data_relevant_papers[TITLE].sum()
        string_abstracts = data_relevant_papers[ABSTRACT].sum()
        string_title_and_abstract = string_title + string_abstracts
        string_authors = data_relevant_papers[AUTHORS].sum()

        string_authors = re.sub(",.*?;", ";", string_authors)

        plot_wordcloud("Titles", string_title)
        plot_wordcloud("Abstracts", string_abstracts)
        plot_wordcloud("Titles and Abstracts", string_title_and_abstract)
        plot_wordcloud("Authors", string_authors)

    return number_of_relevant_papers


# Remove all names, so that only surnames remain
import re
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import collections

def plot_wordcloud(title, text):
    # Compare also: https://www.python-lernen.de/wordcloud-erstellen-python.htm
    # STOPWORDS.update(liste_der_unerwuenschten_woerter), now manually removed from string
    wordcloud = WordCloud(
        background_color="white", max_font_size=40, collocations=True
    ).generate(text)
    plt.figure(figsize=(12, 8))
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.title(title)
    wordcloud_name = (
            "./" + output_file + "_wordcloud_" + title.replace(" ", "_") + ".png"
    )
    print(wordcloud_name)
    plt.savefig(wordcloud_name)
    plt.close()
    return

def get_inclusion_kinds(
    relevant_papers,
    INCLUDE,
    SUFFIX_POINTS,
    INCLUDED_EXCEPTIONAL,
    INCLUDED_TARGET_VALUE,
    INCLUDED_DOUBLE_VETO,
    INCLUDED_SINGLE_VETO,
):

    ###   Plot distribution of reason for relevance relative to total points archieved ###

    point_count = pd.DataFrame()
    columns = [
        INCLUDED_EXCEPTIONAL + SUFFIX_POINTS,
        INCLUDED_TARGET_VALUE + SUFFIX_POINTS,
        INCLUDED_DOUBLE_VETO + SUFFIX_POINTS,
        INCLUDED_SINGLE_VETO + SUFFIX_POINTS,
    ]
    for column in columns:
        point_count[column] = relevant_papers[column].value_counts().sort_index()

    point_count = point_count.drop([0])

    point_count.plot.bar(
        stacked=True,
        title=f"Total of 2nd Screening Points \n Relevant papers: {len(relevant_papers)}",
    )
    plt.savefig(
        "./" + file_core[:-4] + "-total-points" + "-joined-only-relevant" + ".png"
    )
    plt.close()

    for person in ["(M)", "(J)"]:
        relevant_papers["Numeric" + person] = [
            relevant_papers.loc[i, inclusion_criteria_title_and_abstract[3] + person]
            == 1
            for i in relevant_papers.index
        ]
        relevant_papers["Theoretical" + person] = [
            relevant_papers.loc[i, inclusion_criteria_title_and_abstract[3] + person]
            == 2
            for i in relevant_papers.index
        ]
        relevant_papers["Other" + person] = [
            relevant_papers.loc[i, inclusion_criteria_title_and_abstract[3] + person]
            == 3
            for i in relevant_papers.index
        ]
        relevant_papers["Numeric" + person + SUFFIX_POINTS] = (
            relevant_papers[TOTAL_POINTS] * relevant_papers["Numeric" + person]
        )
        relevant_papers["Theoretical" + person + SUFFIX_POINTS] = (
            relevant_papers[TOTAL_POINTS] * relevant_papers["Theoretical" + person]
        )
        relevant_papers["Other" + person + SUFFIX_POINTS] = (
            relevant_papers[TOTAL_POINTS] * relevant_papers["Other" + person]
        )

        relevant_kinds = pd.DataFrame()

        for column in ["Numeric", "Theoretical", "Other"]:
            relevant_kinds[column] = (
                relevant_papers[column + person + SUFFIX_POINTS]
                .value_counts()
                .sort_index()
            )

        relevant_kinds = relevant_kinds.drop([0])

        relevant_kinds.plot.bar(
            stacked=True,
            title=f"Type of relevant papers {person}\n Relevant papers: {len(relevant_papers)}, of which {sum(relevant_papers['Numeric'+person])} numeric and {sum(relevant_papers['Theoretical'+person])} theoretical",
        )
        plt.savefig(
            "./"
            + file_core[:-4]
            + "-total-points-type-"
            + person
            + "-joined-only-relevant"
            + ".png"
        )
        plt.close()

        journals = relevant_papers["Source Title"].value_counts()
        journals.to_csv("./" + output_file + "_relevant_journals.csv")
        journals.plot(kind="bar")
        plt.savefig("./" + output_file + "_relevant_journals.png")
        plt.close()

        year = relevant_papers["Publication Year"].value_counts()
        year.to_csv("./" + output_file + "_publication_year.csv")
        year.plot(kind="bar")
        plt.savefig("./" + output_file + "_publication_year.png")
        plt.close()

    return


count_relevant = pd.DataFrame(
    columns=[
        (exceptionality - 1),
        str(exceptionality),
        str(exceptionality + 1),
        "Only vetos and total points",
    ]
)

for margin in [-2, -1, 0, 1, 2, 3, 4]:
    save = False
    if margin == 0:
        save = True
    count_relevant.loc[target_value + margin] = [
        get_relevant_papers(
            data_with_votes_joined, target_value + margin, exceptionality - 1
        ),
        get_relevant_papers(
            data_with_votes_joined, target_value + margin, exceptionality, save=save
        ),
        get_relevant_papers(
            data_with_votes_joined, target_value + margin, exceptionality + 1
        ),
        get_relevant_papers(
            data_with_votes_joined, target_value + margin, exceptionality + 2
        ),
    ]

print(
    "\nCount of relevant papers dependent on points for exceptionality (columns) and total points (rows):"
)
print(count_relevant)
print(
    "\nRelative relevance of papers dependent on points for exceptionality (columns) and total points (rows):"
)
print(count_relevant / len(data_with_votes_joined.index))
