from TwitterAPI import TwitterAPI

import os
CONSUMER_KEY = 'v2C0ANZKl0kmlZVgKNgMPBNEM'
CONSUMER_SECRET = 'nH3Hc3KZOnBLem3YLIaO2CLg3xIie1jX2JT02kZLKUppWEy8Lm'

ACCESS_TOKEN = '1538767694127693825-oL63xkDbDFl6lkLawzvgvtv6qPsiym'
ACCESS_TOKEN_SECRET = '8O0seCq4opzOwEhD1sDnZ4tzwxpNWJ2xCN2G2kl7IZoPF'

ENVNAME = 'dev'

twitterAPI = TwitterAPI(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

r = twitterAPI.request('account_activity/all/:%s/subscriptions' %
                       ENVNAME, None, None, "POST")

#TODO: check possible status codes and convert to nice messages
print (r.status_code)
print (r.text)
       
