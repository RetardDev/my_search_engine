import requests

x = requests.get('https://facebook.com')
print(x.page.json())