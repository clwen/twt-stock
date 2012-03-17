import requests
import simplejson
import urllib
import sys
import time

companies = {# 'apple': ['apple', 'iphone', 'iphone4s', 'iphone4', 'siri', 'ipod', 'mac', 'macintosh', 'itunes', 'ios'],
        # 'google': ['google', 'android', 'droid', 'googleplus', 'gplus', 'gmail', 'youtube', 'chrome', 'googlemap', 'gmap'],
        'microsoft': ['windows', 'windows8', 'xbox', 'xbox360', 'kinect', 'msn', 'bing', 'ie'],
        # 'amazon': ['amazon', 'kindle', 'kindlefire'],
        'rim': ['rim', 'blackberry'],
        'dell': ['dell'],
        'intel': ['intel', 'xeon'],
        'yahoo': ['yahoo', 'yahoomail', 'ymail', 'yim'],
        'nvidia': ['nvidia', 'tegra', 'tegra3', 'geforce'],
        'netflix': ['netflix']
        }

def get_tweets(query, outfile):
    twt_search_url = 'http://search.twitter.com/search.json?'
    params = {'q': query, 'lang': 'en', 'rpp': '100', 'page': 1}
    of = open(outfile, 'w')

    for p in range(1, 16):
        params['page'] = p
        url = twt_search_url + urllib.urlencode(params)
        print url

        success = False
        while not success:
            r = requests.get(url)
            try:
                j = simplejson.loads(r.content)
            except simplejson.decoder.JSONDecodeError:
                print 'oops, got no response from twitter'
                print 'sleep for 120 seconds and try again'
                time.sleep(120)
                continue
            success = True

        if 'error' in j:
            print j['error']
            of.close()
            return

        # if not other results in current page, don't have to dive into suceeding pages
        if len(j['results']) == 0:
            of.close()
            return

        for item in j['results']:
            of.write(item['text'].encode('utf-8', 'ignore').strip() + '\n')
            of.write(item['created_at'].encode('utf-8', 'ignore').strip() + '\n')
            of.write('|\n') # delimiter of tweets

    of.close()

if __name__ == '__main__':
    for (company, keyword_list) in companies.iteritems():
        for keyword in keyword_list:
            query = '#' + keyword
            outfile = 'tweets/' + company + '_' + keyword
            get_tweets(query, outfile)
            # print 'sleep for three seconds.. being nice to twitter..'
            # time.sleep(3)

