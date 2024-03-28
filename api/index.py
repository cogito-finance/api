from http.server import BaseHTTPRequestHandler
from requests import Session
import requests
import json
import os

CMC_ID = '26016'
CMC_API_KEY = os.environ.get('CMC_API_KEY')


class handler(BaseHTTPRequestHandler):

    def do_GET(self):
        supply_req = requests.get(
            'https://tokensupply.singularitynet.io/tokensupply?tokensymbol=cgv&q=circulatingsupply')
        supply = supply_req.json()

        url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'
        parameters = {
            'id': CMC_ID,
        }
        headers = {
            'Accepts': 'application/json',
            'X-CMC_PRO_API_KEY': CMC_API_KEY,
        }

        session = Session()
        session.headers.update(headers)

        try:
            response = session.get(url, params=parameters)
            data = json.loads(response.text)
            price = data['data'][CMC_ID]['quote']['USD']['price']
            mcap = price * supply
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write("{:.2f}".format(mcap).encode())
        except Exception as e:
            print(e)
            self.send_response(500)
