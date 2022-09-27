import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from wordcloud import WordCloud

file = "2022-07-19-Final-Keywords-Publications-merged-Count.csv"
output_file = file[:-4] + "-votes.csv"
included_file = output_file[:-4] + "-only-included.csv"
TITLE = "Article Title"
ABSTRACT = "Abstract"
AUTHORS = "Authors"
JOURNAL_NAME = "Source Title"
YEAR = "Publication Year"
data_with_votes = pd.read_csv(included_file)

print(f"Number of potentialy relevant files: {len(data_with_votes)}")

string_title = data_with_votes[TITLE].sum()
string_abstracts = data_with_votes[ABSTRACT].sum()
string_title_and_abstract = string_title + string_abstracts
string_authors = data_with_votes[AUTHORS].sum()
# Remove all names, so that only surnames remain
import re

string_authors = re.sub(",.*?;", ";", string_authors)


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
        "./" + output_file[:-4] + "_wordcloud_" + title.replace(" ", "_") + ".png"
    )
    print(wordcloud_name)
    plt.savefig(wordcloud_name)
    plt.close()
    return


plot_wordcloud("Titles", string_title)
plot_wordcloud("Abstracts", string_abstracts)
plot_wordcloud("Titles and Abstracts", string_title_and_abstract)
plot_wordcloud("Authors", string_authors)

data_with_votes[JOURNAL_NAME].value_counts().plot(kind="bar")
plt.savefig("./" + output_file[:-4] + "_relevant_journals.png")
plt.close()

data_with_votes[YEAR].value_counts().plot(kind="bar")
plt.savefig("./" + output_file[:-4] + "_publication_year.png")
plt.close()
