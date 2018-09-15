"""
competition.py
    Get the name of all competitors in a tournament with a single command.
"""
from urllib.request import (urlopen, urlparse, urlunparse, urlretrieve)
from bs4 import BeautifulSoup
import re


def get_html(link: str):
    """
    Open a url
    :param link:
    :type link:
    :return:
    :rtype:
    """
    page = urlopen(link)
    return page


def who_coming(soup: BeautifulSoup) -> str:
    """
    Get the Who's Coming link from the main tournament page.
    :param soup:
    :type soup: BeautifulSoup
    :return: The str representation of Who's Coming link
    :rtype: str
    """
    temp = soup.select_one("a[href*=whoIsComing]")
    return temp.attrs.get('href')


def participants_list(link: str, f):
    """
    Returns a dictionary categories and competitors.
    Sorted by category.
    :param link:
    :type link: str
    """
    page = get_html(link)
    soup = BeautifulSoup(page, 'html.parser')
    # Iterate through the values in the tables
    table = soup.find_all('table', attrs={'class': 'box'})
    for value in table:
        for member in value.contents:
            member_string = str(member).encode('utf8')
            names = re.search(b'[a-zA-Z]*, [a-zA-Z]*',member_string)
            category = re.search(b'>[a-zA-Z]* [a-zA-Z]*\\\'s [a-zA-Z]*', member_string)
            if category is not None:
                f.write(category.group(0).__str__().replace('b\">', '').replace('\"', ''))
            if names is not None:
                f.write(names.group(0).__str__().replace('b\'', '').replace('\'', ''))
            f.write("\n")
        f.write("-------------------------------------------------------------------------------------------------")
        f.write("\n")



def main():
    tournament_link = input("What is the main tournament link page?")
    f = open('participants', 'w')
    main_tournament_page = get_html(tournament_link)
    soup = BeautifulSoup(main_tournament_page, 'html.parser')
    who_is_coming_link = who_coming(soup)
    participants_list(who_is_coming_link, f)
    f.close()


if __name__ == "__main__":
    main()
