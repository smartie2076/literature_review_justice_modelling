import requests
import pandas as pd


def read_file(filename):
    print(f"Reading from file {filename}")
    data = pd.read_excel(filename)
    print(f"Column titles: {data.columns}")
    print(data.head())
    return data


def doi2bib(doi):
    """
    Return a bibTeX string of metadata for a given DOI.
    """

    url = "http://dx.doi.org/" + doi

    headers = {"accept": "application/x-bibtex"}
    r = requests.get(url, headers=headers)

    return r.text


file = "2022-07-05-GoogleFormTesting-With-Leon/2022-07-05-Google-Form-Response-Leon-Version-2022-05-11.xlsx"

data = read_file(file)
import bibtexparser


for index, row in data.iterrows():
    print(index)
    doi = row["DOI"]
    bibtex = doi2bib(doi)
    bibjson = bibtexparser.loads(bibtex).entries
    if "DOI Not Found" not in bibtex:
        data.loc[index, "Author"] = bibjson[0]["author"]
        data.loc[index, "Year"] = bibjson[0]["year"]
        data.loc[index, "Title"] = bibjson[0]["title"]
        data.loc[index, "Journal"] = bibjson[0]["journal"]

data.to_excel(f"{file[:-5]}-metadata.xlsx")
