import pandas as pd

file_name = "2022-02-Paper-Idea-And-Keywords/2022-02-25-Keywords-Literature-Review-Paper-Idea.xlsx"


def join(tab, conjunction):
    data = pd.read_excel(file_name, sheet_name=tab, header=None)
    print(data)
    string = ""
    for value in data[0].values:
        if string == "":
            string = f'"{value}"'
        else:
            string += f' {conjunction} "{value}"'

    return string


tab_and = "AND"
tab_or = ["OR (people)", "OR (justice)"]

string_and = join(tab_and, "AND")
string_or_people = join(tab_or[0], "OR")
string_or_justice = join(tab_or[1], "OR")

search_string = f"{string_and} AND ({string_or_people}) AND ({string_or_justice})"

print(search_string)

text_file = open("2022-02-Paper-Idea-And-Keywords/search_string.txt", "w")

# write string to file
text_file.write(search_string)

# close file
text_file.close()
