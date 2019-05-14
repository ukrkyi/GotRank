import json

import bs4
import mechanicalsoup


# def fast_get_character_page(link):
#     browser = mechanicalsoup.StatefulBrowser()
#     try:
#         browser.open('https://awoiaf.westeros.org' + link)
#         return browser.get_current_page()
#     except mechanicalsoup.LinkNotFoundError:
#         return None
#

def get_character_page(link):
    """
    (string) -> (bs4.BeautifulSoup)
    This function get page of character by link
    """

    print('Connecting')
    browser = mechanicalsoup.StatefulBrowser()
    browser.open("https://awoiaf.westeros.org/index.php/List_of_characters")
    try:
        browser.follow_link(link)
    except mechanicalsoup.LinkNotFoundError:
        link = link.replace('(', '\(').replace(')', '\)')
        print(link)
        browser.follow_link(link)
    return browser.get_current_page()


def get_row_name(row):
    result = row.find_all('th', scope="row")
    if len(result) == 0:
        return None
    else:
        return result[0].text


def get_names_from_row(row):
    names = row.find_all('td')[0].decode_contents().split('<br/>')
    names = list(map(lambda x: bs4.BeautifulSoup(x, 'html.parser').text.split('[')[0], names))
    names = list(map(lambda x: x.strip(), names))
    return names


def get_table(character_page):
    if character_page is None:
        return character_page
    else:
        print('Got page')
    rows = character_page.find_all("tbody")
    if rows:
        rows = rows[0].find_all('tr')
        print('Got rows')
    else:
        rows = None
    return rows


def parse_character(link, name):
    rows = get_table(get_character_page(link))
    if rows is None:
        return None
    print('Got')
    aliases = []
    for i in rows:
        if get_row_name(i) in ["Alias", "Other Titles"]:
            names = get_names_from_row(i)
            aliases += names
    character_data = {"name": name, 'aliases': aliases}
    return json.dumps(character_data)


print(parse_character('/index.php/Addam_Osgrey', ""))
