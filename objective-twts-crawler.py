import requests
import simplejson
import urllib
import sys
import time

base_url = 'https://api.twitter.com/1/statuses/user_timeline.json?'
params = {'screen_name': 'nytimes', 'count': '200', 'page': 1}
sites = ['TechCrunch', 'CNETNews', 'RWW', 'mashable', 'Gizmodo', 'gigaom', 'allthingsd', 'TheNextWeb', 'verge', 'Wired', 'nytimesbits', 'WSJTech', 'SAI', 'guardiantech', 'HuffPostTech']

for site in sites:
    outfile = 'tweets/objective/' + site
    params['screen_name'] = site
    of = open(outfile, 'a')

    for p in range(1, 2):
        params['page'] = p
        url = base_url + urllib.urlencode(params)
        print url

        success = False
        while not success:
            r = requests.get(url)
            try:
                j = simplejson.loads(r.content)
            except simplejson.decoder.JSONDecodeError:
                print 'oops, got no response from twitter, try again'
                continue
            success = True
        
        for item in j:
            of.write(item['text'].encode('utf-8', 'ignore').strip() + '\n')
            of.write(item['created_at'].encode('utf-8', 'ignore').strip() + '\n')
            of.write('|\n') # delimiter of tweets

        time.sleep(30) # being nice to twitter api

    of.close()
