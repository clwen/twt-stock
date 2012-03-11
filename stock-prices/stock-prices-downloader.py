import os
import urllib
import requests

symbols = {'apple': 'AAPL', 'google': 'GOOG', 'microsoft': 'MSFT', 'amazon': 'AMZN', 'rim': 'RIMM', 'dell': 'DELL', 'intel': 'INTC', 'yahoo': 'YHOO', 'nvidia': 'NVDA', 'netflix': 'NFLX'}

for (company, symbol) in symbols.iteritems():
    filename = '%s.csv' % (company)
    of = open(filename, 'w')
    base_url = 'http://ichart.finance.yahoo.com/table.csv?'
    params = {'s': symbol, 'g': 'w'}
    url = base_url + urllib.urlencode(params)
    print url
    r = requests.get(url)
    of.write(r.content)

