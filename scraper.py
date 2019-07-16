import requests
from bs4 import BeautifulSoup

def scrape(url):
    looped = False
    #Load html's plain data into a variable
    plain_html_text = requests.get(url)
    #parse the data
    soup = BeautifulSoup(plain_html_text.text, "html.parser")
    lst = soup.find("ul", class_="constituency-members-list")
    if lst == None:
        if looped:
            return None
        looped = True
        return scrape(url + "-GRC")
    return lst

def scraping(grc):
    members = []
    grc_lst = grc.split(" ") # list of words in grc name
    grc_edited = "-".join(grc_lst[:-1]) # account for grcs with multiple words in name 
    url = "https://www.parliament.gov.sg/mps/constituency/details/" + grc_edited
    lst = scrape(url)
    if (lst == None):
        return []
    items = lst.findAll("li")
    for item in items:
        members.append(item.string)
    return members
