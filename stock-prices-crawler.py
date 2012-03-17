import requests
import urllib
from BeautifulSoup import BeautifulSoup

symbols = {'apple': 'AAPL', 'google': 'GOOG', 'microsoft': 'MSFT', 'amazon': 'AMZN', 'rim': 'RIMM', 'dell': 'DELL', 'intel': 'INTC', 'yahoo': 'YHOO', 'nvidia': 'NVDA', 'netflix': 'NFLX'}
params = {'s': 'query', 'g': 'w'}

def get_recent_prices(company, symbol):
    filename = 'stock-prices/' + company
    fp = open(filename, 'w')
    base_url = 'http://finance.yahoo.com/q/hp?'
    params['s'] = symbol
    url = base_url + urllib.urlencode(params)
    data = []
    print url

    r = requests.get(url)
    soup = BeautifulSoup(r.content)
    table = soup.find('table', {'class': 'yfnc_datamodoutline1'})
    rows  = soup.findAll('tr')
    for row in rows:
        cells = row.findAll('td', {'class': 'yfnc_tabledata1'})
        if not cells:
            continue

        for cell in cells:
            if cell.string == None:
                continue

            data.append(cell.string)

    for i in range(0, 300, 7):
        output_line = data[i+4] 
        print output_line
        fp.write(output_line + '\n')

if __name__ == '__main__':
    for (company, symbol) in symbols.iteritems():
        get_recent_prices(company, symbol)

