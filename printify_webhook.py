import requests
import os

headers = {
  'Content-Type': 'application/json',
  'Accept': 'application/json',
  'Authorization': 'Bearer %s' % os.environ['PRINTIFY_API_TOKEN']
}

r = requests.post('https://api.printify.com/v1/shops/912084/webhooks.json', params={

}, headers = headers, data='{"topic": "product:published","url": "https://0b0001f2.ngrok.io/printify_webhook", "secret": "optional-secret-value"}')

print r.json()