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
		request = requests.get(self.lookup_url,params = param).json()
		return pd.DataFrame.from_records(request)

	def get_quote(self,string):
		param = dict(
			symbol = string.strip().upper()
		)
		request = requests.get(self.quote_url,params = param).json()
		data = pd.DataFrame.from_dict(request, orient = 'index')
		return data.loc[['Name','Symbol','LastPrice','Open','Timestamp'],:]