from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools

import time
from datetime import datetime
import mraa
import math

B = 4275
R0 = 100000
TEMP_MODULE = mraa.Aio(1)

SCOPES = 'https://www.googleapis.com/auth/spreadsheets'
SPREADSHEET_ID = '190SkqjfInZmjhJmKWogohXDzLyzp40EhpMqDPC9zWdo'

def main():
	while(True):
		temperature = getTemp()
		appendToSheet(temperature)
		time.sleep(2)

def getTemp():
	print('getting temperature')
	data = TEMP_MODULE.read()

	R = (1023.0 / data - 1.0) * R0
	celsius = 1.0 / (math.log(R / R0) / B + 1 / 298.15) - 273.15
	fahrenheit = (9.0/5) * celsius + 32

	return fahrenheit

def appendToSheet(temperature):
	print('appending to google sheet')
	access_token = file.Storage('token.json')
	creds = access_token.get()
	if not creds or creds.invalid:
		flow = client.flow_from_clientsecrets('crdentials.json', SCOPES)
		creds = tools.run_flow(flow, store)
	service = build('sheets', 'v4', http=creds.authorize(Http()))

	range = 'A1:B1'

	body = {
		'values': [[datetime.now().strftime('%Y-%m-%d %H:%M:%S'), temperature]]
	}

	result = service.spreadsheets().values().append(spreadsheetId=SPREADSHEET_ID, range=range, valueInputOption='USER_ENTERED', body=body).execute()

if __name__ == '__main__':
	main()
