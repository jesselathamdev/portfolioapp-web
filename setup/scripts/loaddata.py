# initial_data/loaddata.py

# this script bulk loads in market stock data that has been downloaded from the internets
# borrowed from http://mitchfournier.com/2011/10/11/how-to-import-a-csv-or-tsv-file-into-a-django-model/

csv_filepathname = '/Projects/django/portfolioapp/setup/data/NYSE-TSX-NASDAQ-SYMBOLS-2013-02-05.txt'
project_home = '/Projects/django/portfolioapp/'

import sys, os
import csv

sys.path.append(project_home)
os.environ['DJANGO_SETTINGS_MODULE'] = 'portfolioapp.settings'

from portfolioapp.apps.markets.models import Stock

dataReader = csv.reader(open(csv_filepathname, 'rU'), dialect='excel-tab')
# or dataReader = csv.reader(open(csv_filepathname), delimiter=',', quotechar='"')

for row in dataReader:
    if row[0] != 'Market':
        stock = Stock()
        market = row[0]
        if market == 'XNAS':
            stock.market_id = 3
        elif market == 'XTSE':
            stock.market_id = 1
        elif market == 'XNYS':
            stock.market_id = 4
        stock.symbol = row[1]
        stock.name = row[2]
        stock.last_price = 1.00 # give the data an assumed last_price
        stock.save()
