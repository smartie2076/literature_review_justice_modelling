import pandas as pd
import matplotlib.pyplot as plt

file_name = '2022-06-10-webofscience-5-search-term-groups-no-transport-0-1000.xls'
file_name_2 = '2022-06-10-webofscience-5-search-term-groups-no-transport-1001-1126.xls'

keywords_search_string = ["Energy", "electricit", "heat", "Climate", "decarbon", "sustainab", "renewable", "environment", "green",
			"carbon", "clean", "transition", "transformation", "development", "pathway", "strateg", "polic", "planning",
			"model", "indicator", "simulation", "optimi", "tool", "framework", "Consumer", "household", "prosumer",
			"social", "society", "population", "communit", "justice", "equit", "equality", "fairness"]
keywords_additional = ["distribution", "representative", "procedual", "burden", "poverty", "fair", "gender", "recognition", "cost", "benefit", "socio-economic", "disadvantage", "minority", "income", "acceptance", "poor"]
keywords = keywords_search_string + keywords_additional

keyword_string = ""
for keyword in keywords:
	keyword_string += keyword + "|"
keyword_string = keyword_string[:-1]

COUNT = "Count"
TOTAL_COUNT = "Total Count"
TITLE = "Article Title"
ABSTRACT = "Abstract"

def read_file(filename):
	print(f"Reading from file {filename}")
	data = pd.read_excel(filename)
	print(f"Column titles: {data.columns}")
	print(data.head())
	return data

def counting_keyword_relevance(data, column):
	for keyword in keywords:
		data[COUNT + "-" + keyword] = data[column].str.count(keyword)
	data[TOTAL_COUNT] = data[column].str.count(keyword_string)
	data[TOTAL_COUNT+"-search-terms"] = sum(data[COUNT+"-"+keyword] for keyword in keywords_search_string)
	data[TOTAL_COUNT+"-additional-terms"] = sum(data[COUNT+"-"+keyword] for keyword in keywords_additional)
	return data

title_and_abstract = TITLE+" AND " + ABSTRACT
data = read_file(file_name)
data.append(read_file(file_name_2))
print(f"Number of keywords: {len(keywords)}")
data[title_and_abstract] = data[TITLE] + data[ABSTRACT]
data["wordcount-"+title_and_abstract] = [len(data[title_and_abstract][i]) for i in data.index]
data = counting_keyword_relevance(data, title_and_abstract)
data["relative-indidence-total"] = data[TOTAL_COUNT] / data["wordcount-"+title_and_abstract]
data[TOTAL_COUNT].plot.hist(bins=20)
plt.xlabel('Incidence of keywords in title and abstract')
plt.ylabel('Number of papers')
len = len("2022-06-10-webofscience-5-search-term-groups-no-transport")
plt.savefig(f'./{file_name[:len]}-histogram-{TOTAL_COUNT}.png')
plt.close()
data["relative-indidence-total"].plot.hist(bins=20)
plt.xlabel('Incidence of keywords in title and abstract, relative to word count')
plt.ylabel('Number of papers')
plt.savefig(f'./{file_name[:len]}-histogram-relative-indidence-total.png')
plt.close()

data.to_excel(f'{file_name[:len]}-{COUNT}.xlsx')