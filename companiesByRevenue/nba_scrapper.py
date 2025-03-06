import requests

#extracting basic information such as name, gp, minutes and the club
url1 = "https://www.nba.com/stats/leaders"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"
}
response1 = requests.get(url1, headers=headers)

if response1.status_code == 200:
    print("Success")
else:
    print("Failed")

html_content = response1.text
print(html_content)
