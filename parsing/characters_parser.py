import requests
from bs4 import BeautifulSoup

if __name__ == "__main__":
    characters = []
    characters_list_link = "https://awoiaf.westeros.org/index.php/List_of_characters"
    characters_list_site = requests.get(characters_list_link).text
    parser = BeautifulSoup(characters_list_site, 'html.parser')
    parser = parser.find_all("div", id="mw-content-text")[0].find_all("li")
    for i in range(len(parser)):
        parser[i] = parser[i].find_all("a")[0]["title"], parser[i].find_all("a")[0][
            "href"]

    with open("characters_dataset.csv", "w") as file:
        file.write("name, link\n")
        for i in parser:
            file.write("{}, {}".format(i[0], i[1]) + "\n")
