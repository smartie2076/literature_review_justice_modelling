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

DOI = "DOI"

PARAMETER = "parameter"  # parameters/answer options
COUNT = "count"

RESULT_FOLDER = f"{path_base}-Evaluation"

# Columns
definitions_justice = pd.read_csv(FILENAME_DEFINITIONS +"-Justice" + CSV, header=None)[0].values
definitions_relevance = pd.read_csv(FILENAME_DEFINITIONS + "-Relevance" +CSV, header=None)[0].values
definitions_umbrella = pd.read_csv(FILENAME_DEFINITIONS + "-Umbrella" +CSV, header=None)[0].values

print("Drop-Down-Definitions:")
print(definitions_justice)
print(definitions_relevance)
print(definitions_umbrella)

LIST_MODELLING_STEPS = ['Scenarios', 'Parameterization / Input factors', 'Pre-processing', 'Simulation', 'Optimization', 'Result processing']

MT_CORR = "Correlation and Regession"
MT_FORM = 'Formulaic Calculation'
MT_ESM = 'Energy System Model'
MT_IAM =  "Integrated Assessment Model"
MT_AGENT = "Agent-based modeling"
MT_CGE = "Macro-Economic Model"

LIST_MODEL_TYPES = [MT_CORR, MT_FORM, MT_ESM, MT_IAM, MT_AGENT, MT_CGE]