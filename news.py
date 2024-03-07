import requests
from bs4 import BeautifulSoup
import json

url = 'https://www.moneycontrol.com/news/business/'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

articles = []
for article in soup.find_all('li', {'class': 'clearfix'}):
    title = article.find('h2').text.strip()
    summary = article.find('p').text.strip()
    img = article.find('img')['data-src']

    # Modify the height and width parameters
    img = img.replace("width=135", "width=200")  # Change width to 200
    img = img.replace("height=80", "height=150")  # Change height to 150
    
    link = article.find('a')['href']
    
    articles.append({
        'title': title,
        'summary': summary,
        'link': link,
        'img': img
    })

json_data = json.dumps(articles)

print(json_data)
