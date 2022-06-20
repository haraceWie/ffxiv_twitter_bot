from TwitterAPI import TwitterAPI

import os

CONSUMER_KEY = 'v2C0ANZKl0kmlZVgKNgMPBNEM'
CONSUMER_SECRET = 'nH3Hc3KZOnBLem3YLIaO2CLg3xIie1jX2JT02kZLKUppWEy8Lm'

ACCESS_TOKEN = '1538767694127693825-oL63xkDbDFl6lkLawzvgvtv6qPsiym'
ACCESS_TOKEN_SECRET = '8O0seCq4opzOwEhD1sDnZ4tzwxpNWJ2xCN2G2kl7IZoPF'

#The environment name for the beta is filled below. Will need changing in future		
ENVNAME = 'dev'
WEBHOOK_URL = 'https://tranquil-beach-53738.herokuapp.com/webhook'

twitterAPI = TwitterAPI(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

r = twitterAPI.request('account_activity/all/:%s/webhooks' % ENVNAME, {'url': WEBHOOK_URL})

print (r.status_code)
print (r.text)
