import numpy as np
import pandas as pd

CREATE_PLOTS = True
RETRIEVE_METADATA = False
PRINT_RESULT_SNIPPETS = False
np.set_printoptions(linewidth=100000)  # Export processed data without linebreaks in csv

path_base = "2024_01_31_GoogleSheetDB"

FILENAME_PAPERS = (
    f"{path_base}/2024-01-31-JM-Papers"
)
FILENAME_INDICATORS =(
    f"{path_base}/2024-01-31-JM-Indicators"
)

FILENAME_DEFINITIONS = (
    f"{path_base}/2024-01-31-JM-Definitions"
)
CSV = ".csv"
PNG = ".png"

PARAMETER = "parameter"  # parameters/answer options
DOI = "doi"

RESULT_FOLDER = f"{path_base}-Evaluation"

# Columns
definitions_justice = pd.read_csv(FILENAME_DEFINITIONS +"-Justice" + CSV, header=None)[0].values
definitions_relevance = pd.read_csv(FILENAME_DEFINITIONS + "-Relevance" +CSV, header=None)[0].values
definitions_umbrella = pd.read_csv(FILENAME_DEFINITIONS + "-Umbrella" +CSV, header=None)[0].values

print("Drop-Down-Definitions:")
print(definitions_justice)
print(definitions_relevance)
print(definitions_umbrella)
