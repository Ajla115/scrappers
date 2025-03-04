import requests
from bs4 import BeautifulSoup
import pandas as pd

url = "https://en.wikipedia.org/wiki/List_of_largest_companies_in_the_United_States_by_revenue"

page = requests.get(url)

soup = BeautifulSoup(page.text, "html")

table = soup.find_all("table")[0] #to access the first table I need

#second way
#print(soup.find("table", class_ = "wikitable sortable"))
world_table_titles = []
world_titles = table.find_all('th')
for title in world_titles:
    world_table_titles.append(title.text.strip())

#print(world_table_titles)

df = pd.DataFrame(columns = world_table_titles)
print(df)


