import requests
import json
import pandas as pd

class Markit:
	def __init__(self):
		self.lookup_url = "http://dev.markitondemand.com/Api/v2/Lookup/json"
		self.quote_url = "http://dev.markitondemand.com/Api/v2/Quote/json"

	def company_search(self,string):
		param = dict(
			input = string.strip().lower()
		)
		request = requests.get(self.lookup_url,params = param)
		if request.status_code != 200:
			print("API Faulty Status Code.")
			return pd.DataFrame()
		request = request.json()
		return pd.DataFrame.from_records(request)

	def get_quote(self,string, *args):
		param = dict(
			symbol = string.strip().upper()
		)
		request = requests.get(self.quote_url,params = param)
		if request.status_code != 200:
			print("API Faulty Status Code.")
			return pd.DataFrame()
		request = request.json()
		data = pd.DataFrame.from_dict(request, orient = 'index')
		return data.loc[list(args),:]
	
	def get_price(self,string):
		param = dict(
			symbol = string.strip().upper()
		)
		request = requests.get(self.quote_url,params = param)
		if request.status_code != 200:
			print(f"API Faulty Status Code for {string.strip().upper()}.")
			return 0
		request = request.json()
		price = request['LastPrice']
		return price