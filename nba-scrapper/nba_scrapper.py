import requests

#extracting basic information such as name, gp, minutes and the club
url1 = "https://www.nba.com/stats/leaders"
response1 = requests.get(url1)

if response1.status_code == 200:
    print("Success")
else:
    print("Failed")

html_content = response1.text
print(html_content)
