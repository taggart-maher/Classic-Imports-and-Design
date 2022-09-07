import requests

token = 'd6cb0c64-5b6b-4769-81b0-7496540bc8d1'
page = 'johnrichard.com'
url = 'https://api.scrapingrobot.com?token=' + token + '&url=' + page
headers = {'Accept':'application/json'}
api = requests.get(url, headers=headers)

print(api.text)