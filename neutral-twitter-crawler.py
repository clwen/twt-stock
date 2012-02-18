import requests
import simplejson
import urllib
import sys
import time

base_url = 'https://api.twitter.com/1/statuses/user_timeline.json?'
params = {'screen_name': 'nytimes', 'count': '200', 'page': 1}
# sites = ['TechCrunch', 'CNETNews', 'RWW', 'mashable', 'Gizmodo', 'gigaom', 'allthingsd', 'TheNextWeb', 'verge', 'Wired', 'nytimesbits', 'WSJTech', 'SAI', 'guardiantech', 'HuffPostTech']
sites = ['HuffPostTech']

for site in sites:
    outfile = 'tweets/neutral/' + site
    params['screen_name'] = site
    of = open(outfile, 'w')

    for p in range(1, 2):
        params['page'] = p
        url = base_url + urllib.urlencode(params)
        print url

        r = requests.get(url)
        j = simplejson.loads(r.content)
        
        for item in j:
            of.write(item['text'].encode('utf-8', 'ignore').strip() + '\n')
            of.write(item['created_at'].encode('utf-8', 'ignore').strip() + '\n')
            of.write('|\n') # delimiter of tweets

        time.sleep(30) # being nice to twitter api

    of.close()
