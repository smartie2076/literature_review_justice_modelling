import numpy as np
import pandas as pd
import os, shutil
import matplotlib.pyplot as plt
import F13_assess_googlesheetDB_functions as f
import C13_assess_googlesheetDB as C

########################
# Only Evaluate Papers #
########################

papers = pd.read_csv(C.FILENAME_PAPERS + C.CSV, header=2, skiprows=[3,4], sep=";")
papers = papers.drop(columns=papers.columns[0])
print(f"Number of assessed papers: {len(papers.index)}.")
print(f"Columns: {papers.columns.tolist()}")
print(papers.head())

# Retrieve Metadata based on C.DOI (Authors, Title, Year, Journal)
if C.RETRIEVE_METADATA is True:
    papers = f.add_metadata_based_on_C.DOI(papers, "C.DOI")
    papers.to_C.CSV(C.FILENAME_PAPERS+"_with_metadata.C.CSV")
def evaluate_papers(paper_selection, group_folder):
    path_group = C.path_base + "/" + group_folder
    if os.path.isdir(path_group):
        shutil.rmtree(path_group)
    os.mkdir(path_group)
    # Evaluate single fields
    if C.RETRIEVE_METADATA is True:
        f.column_count_plot_store(paper_selection, path_group, keyword="year")
        f.column_count_plot_store(paper_selection, path_group, keyword="journal")

    f.column_count_plot_store(paper_selection, path_group, keyword="Country")
    f.column_count_plot_store(paper_selection, path_group, keyword="List of applied methods")

    # Retrieve Metadata based on C.DOI (Authors, Title, Year, Journal)
    db_further_reading = f.column_count_plot_store(paper_selection, path_group, keyword="Relevant cited papers")
    if C.RETRIEVE_METADATA is True:
        db_further_reading = f.add_metadata_based_on_C.DOI(db_further_reading, "Relevant cited papers")
        db_further_reading.to_C.CSV(path_group+f"/further_reading_list.C.CSV")

    # Evaluate Keywords
    keywords = f.column_count_plot_store(paper_selection, path_group, keyword="Author-defined keywords")
    f.plot_wordcloud(path_group, "Author-defined Keywords", ', '.join(keywords["Author-defined keywords"].values))

    # Justice definition
    dropdown_list_choices = C.definitions_justice # single-choice input
    dropdown_list_name = "Justice concept"
    filename = "Justice-concept-"

    # ... and geographical scale
    single_choice_list = ["Global","Continent/Union","Country-level","State/Region","City/municipality","Community","Households"]
    f.combine_dropdown_and_true_false(paper_selection, path_group, filename + "geoscale", dropdown_list_name, dropdown_list_choices, single_choice_list)
    # ... and time scale
    single_choice_list = ["Past", "Present", "Near future", "Far future"]
    f.combine_dropdown_and_true_false(paper_selection, path_group, filename + "timescale", dropdown_list_name, dropdown_list_choices, single_choice_list)
    # ... and sectors
    single_choice_list = ["Electricity","Heating","Cooling","Buildings","Industry","Mobility and Transport"]
    f.combine_dropdown_and_true_false(paper_selection, path_group, filename + "sectors", dropdown_list_name, dropdown_list_choices, single_choice_list)
    # ... and energy topics
    single_choice_list = ["Demand Assessment","Energy System Planning","Sector Coupling","Flexibility","Energy Access","Sufficiency","Policy","Technology-Specific","Digitalization","CO2 Emissions","Planetary ressources"]
    f.combine_dropdown_and_true_false(paper_selection, path_group, filename + "energy_topic", dropdown_list_name, dropdown_list_choices, single_choice_list)
    # ... and model types
    single_choice_list = ["Correlation and Regession","Formulaic Calculation","Energy System Model","Integrated Assessment Model","Agent-based modeling","Macro-Economic Model"]
    f.combine_dropdown_and_true_false(paper_selection, path_group, filename + "model_type", dropdown_list_name, dropdown_list_choices, single_choice_list)


single_choice_list = ["Correlation and Regession", "Formulaic Calculation", "Energy System Model",
                      "Integrated Assessment Model", "Agent-based modeling", "Macro-Economic Model"]

exclude_regressions = papers[papers["Correlation and Regession"]==1][papers["Formulaic Calculation"]==0][papers["Energy System Model"]==0][papers["Integrated Assessment Model"]==0][papers["Agent-based modeling"]==0][papers["Macro-Economic Model"]==0]

paper_groups = {
    "All": papers,
    "Not-defined Concept": papers[papers["Justice concept"]=="Not defined"],
    "Excluding-only-regressions": papers.drop(exclude_regressions.index)}

for group in paper_groups.keys():
    print(f"Paper group {group} covers {len(paper_groups[group].index)} papers.")
    evaluate_papers(paper_groups[group], group_folder=group)

############################
# Only Evaluate Indicators #
############################

indicators = pd.read_csv(C.FILENAME_INDICATORS + C.CSV,header=2, skiprows=[3,4], sep=";")
indicators = indicators.drop(columns=indicators.columns[0])
print(f"Number of identified indicators: {len(indicators.index)}")
print(f"Columns: {indicators.columns.tolist()}")
print(indicators.head())

f.column_count_plot_store(indicators, C.path_base, keyword="Indicator")

# Retrieve Metadata based on C.DOI (Authors, Title, Year, Journal)
if C.RETRIEVE_METADATA is True:
    indicators = f.add_metadata_based_on_C.DOI(indicators, "C.DOI")
    indicators.to_C.CSV(C.FILENAME_INDICATORS+"_with_metadata.C.CSV")

##############################################
# Evaluate Papers and Indicators in parallel #
##############################################

