import matplotlib.pyplot as plt
import pandas as pd

target_value = 12  # At least two points in each
exceptionality = 5  # min 5, ie. one of two voted exceptionality

file_core = (
    "2022-07-19-Final-Keywords-Publications-merged-Count-votes-only-included.csv"
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

# Read from file and drop all without a vote in the relevant criteria
data_with_votes_m = pd.read_csv(files[0]).dropna(
    subset=[inclusion_criteria_title_and_abstract[i] for i in range(0, 3)]
)
data_with_votes_j = pd.read_csv(files[1]).dropna(
    subset=[inclusion_criteria_title_and_abstract[i] for i in range(0, 3)]
)

for i in inclusion_criteria_title_and_abstract:
    data_with_votes_m.rename(columns={i: i + "(M)"}, inplace=True)
    data_with_votes_j.rename(columns={i: i + "(J)"}, inplace=True)

data_with_votes_joined = data_with_votes_m.merge(data_with_votes_j, how="left")
data_with_votes_joined = data_with_votes_joined.dropna(
    subset=[inclusion_criteria_title_and_abstract[i] + "(M)" for i in range(0, 3)]
    + [inclusion_criteria_title_and_abstract[i] + "(J)" for i in range(0, 3)]
)


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
    ].value_counts().plot(kind="bar", title=title)
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

data_with_votes_joined["Total of 2nd Screening Points"] = sum(
    [
        data_with_votes_joined[
            inclusion_criteria_title_and_abstract[criteria_number] + "(sum)"
        ]
        for criteria_number in range(0, 3)
    ]
)
data_with_votes_joined["Total of 2nd Screening Points"].value_counts().plot(
    kind="bar", title="Total of 2nd Screening Points"
)
plt.savefig("./" + file_core[:-4] + "-total-points" + "-joined" + ".png")
plt.close()


def get_relevant_papers(target_value, exceptionality, save=False):

    # Include based on True/False criteria and overall target points
    criterium_target_value = [
        data_with_votes_joined.loc[id, "Total of 2nd Screening Points"]
        >= target_value  # At least one of us has to have voted 3
        for id in data_with_votes_joined.index
    ]

    data_with_votes_joined["Include"] = criterium_target_value
    # Include based on max vote ("exceptional" performance for one of the criteria)
    for criteria in inclusion_criteria_title_and_abstract[0:3]:
        # Maximum reachable points
        maximum = exceptionality
        criterium_maximum = [
            data_with_votes_joined.loc[id, criteria + "(sum)"] >= maximum
            for id in data_with_votes_joined.index
        ]

        data_with_votes_joined["Include"] += criterium_maximum

    # Add papers that are included due to exceptional vote
    other_criterion = [
        data_with_votes_joined.loc[id, inclusion_criteria_title_and_abstract[6] + "(M)"]
        == True
        for id in data_with_votes_joined.index
    ]

    data_with_votes_joined["Include"] += other_criterion

    other_criterion = [
        data_with_votes_joined.loc[id, inclusion_criteria_title_and_abstract[6] + "(J)"]
        == True
        for id in data_with_votes_joined.index
    ]

    data_with_votes_joined["Include"] += other_criterion

    # Only write included papers to file (as we have a boolean column, adding True+True does not result in 2)
    if save is True:
        data_with_votes_joined[data_with_votes_joined["Include"] == True].to_csv(
            output_file + "-only-included-joined.csv"
        )
        print(
            f"Saved list of relevant papers to {output_file[:-4]}-only-included-joined.csv. \n"
        )
    relevant_papers = data_with_votes_joined["Include"].sum()
    if save is True:
        print(
            f"Number of relevant papers: \n"
            f"More then {target_value} points: {sum(criterium_target_value)}\n"
            f"+ At least one sees exceptionality (sum of points {exceptionality}): {sum(criterium_maximum)}\n"
            f"+ Vetoed in: {sum(other_criterion)}\n"
            f"= Total relevant papers: {relevant_papers} (of {len(data_with_votes_joined)} papers / ({round(relevant_papers/len(data_with_votes_joined)*100,1)} %)"
        )
    return relevant_papers


count_relevant = pd.DataFrame(
    columns=[(exceptionality - 1), str(exceptionality), str(exceptionality + 1)]
)

for margin in [-2, -1, 0, 1, 2, 3, 4]:
    count_relevant.loc[target_value + margin] = [
        get_relevant_papers(target_value + margin, exceptionality - 1),
        get_relevant_papers(
            target_value + margin, exceptionality, save=any([margin == 0])
        ),
        get_relevant_papers(target_value + margin, exceptionality + 1),
    ]

print(
    "Count of relevant papers dependent on points for exceptionality (columns) and total points (rows):"
)
print(count_relevant)
print(
    "Relative relevance of papers dependent on points for exceptionality (columns) and total points (rows):"
)
print(count_relevant / len(data_with_votes_joined.index))
