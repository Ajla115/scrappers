import requests
from bs4 import BeautifulSoup

url = "https://www.scrapethissite.com/pages/forms/"

#print(requests.get(url))
page = requests.get(url)

soup = BeautifulSoup(page.text, "html")
#parse in html format

#print(soup.prettify())
#print(soup.find("div"))
#print(soup.find_all("div", class_ = "col-md-12"))
#print(soup.find_all("p", class_ = "lead"))


#print(soup.find("p", class_ = "lead").text)
#text can only be used with a find option, not find all

#print(soup.find_all("td"))

print(soup.find("th").text.strip())
