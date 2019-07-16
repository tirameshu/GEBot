import requests
from bs4 import BeautifulSoup

def scraping(grc):
    members = []
    url = "https://www.parliament.gov.sg/mps/constituency/details/" + grc
    #Load html's plain data into a variable
    plain_html_text = requests.get(url)
    #parse the data
    soup = BeautifulSoup(plain_html_text.text, "html.parser")
    lst = soup.find("ul", class_="constituency-members-list")
    items = lst.findAll("li")
    for item in items:
        members.append(item.string)
    return members
