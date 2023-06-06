import pandas as pd

data_revote = pd.read_csv(
    "2023-01-3rd-Screening-Paper-Screening/2023-01-24-Relevant_Articles_Revote.csv",
    sep=";",
)
data_revote.reset_index(drop=True)

data = pd.read_csv(
    "2022-10-2nd-Screening-Jonathan-Martha-Score-Results/2022-09-30-2nd-screening-only-included-joined.csv"
)
data.drop(
    data.columns[data.columns.str.contains("unnamed", case=False)],
    axis=1,
    inplace=True,
)
data.reset_index(drop=True)

columns_data_revote = list(data_revote.columns)
columns_data_revote.remove("Assignee")
columns_data_revote.remove("DOI")

data_new = data.drop(columns_data_revote, axis=1)
data_new = data_new.merge(data_revote, how="left", on="DOI")
data_new.to_csv("2022-09-30-2nd-screening-only-included-joined.csv")
