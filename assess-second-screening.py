import matplotlib.pyplot as plt
import pandas as pd

screened_by = "Martha"
# screened_by = "Jonathan"

file = "2022-07-19-Final-Keywords-Publications-merged-Count-votes-only-included.csv"
output_file = file[:-4] + "-2nd-screening"
if screened_by == "Martha":
    output_file += "-m"
elif screened_by == "Jonathan":
    output_file += "-j"
output_file += "-only-included.csv"

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

data_with_votes = pd.read_csv(output_file)


def title_multirow(text):
    letters_in_line = 60
    i = 0
    while i + letters_in_line < len(text):
        text = text[: i + letters_in_line] + " \n " + text[i + letters_in_line :]
        i += letters_in_line
    return text


title = title_multirow(inclusion_criteria_title_and_abstract[3])
data_with_votes[inclusion_criteria_title_and_abstract[3]].value_counts().plot(
    kind="bar", title=title
)
plt.tight_layout()
plt.savefig("./" + output_file[:-4] + "_distribution_method_type.png")
plt.close()

title = title_multirow(inclusion_criteria_title_and_abstract[4])
data_with_votes[inclusion_criteria_title_and_abstract[4]].value_counts().plot(
    kind="bar", title=title
)
plt.tight_layout()
plt.savefig("./" + output_file[:-4] + "_distribution_topic.png")
plt.close()

title = title_multirow(inclusion_criteria_title_and_abstract[5])
data_with_votes[inclusion_criteria_title_and_abstract[5]].value_counts().plot(
    kind="bar", title=title
)
plt.tight_layout()
plt.savefig("./" + output_file[:-4] + "_distribution_reader.png")
plt.close()
