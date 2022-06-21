#from TwitterAPI import TwitterAPI
import tweepy
import os

CONSUMER_KEY = os.environ.get('CONSUMER_KEY', None)
CONSUMER_SECRET = os.environ.get('CONSUMER_SECRET', None)

ACCESS_TOKEN = os.environ.get('ACCESS_TOKEN', None)
ACCESS_TOKEN_SECRET = os.environ.get('ACCESS_TOKEN_SECRET', None)


def initApiObject():
    
    #user authentication
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

    return auth
 
def processDirectMessageEvent(eventObj):
    
    # messageText = eventObj.get('message_data').get('text')
    # userID = eventObj.get('sender_id')

    # twitterAPI = initApiObject()
            
    # messageReplyJson = '{"event":{"type":"message_create","message_create":{"target":{"recipient_id":"' + userID + '"},"message_data":{"text":"Hello World!"}}}}'
        
    # #ignore casing
    # if(messageText.lower() == 'hello bot'):
            
    #     r = twitterAPI.request('direct_messages/events/new', messageReplyJson)
          
    return None      

def processLikeEvent(eventObj):
    #userHandle = eventObj.get('user', {}).get('screen_name')
    
    print ('This user liked one of your tweets: %s' % userHandle) 
    
    return None           


def processMentionEvent(eventObj):

    message = eventObj.get('text')

    if('@ffxiv_party_' not in message.lower()) :
        print('message not contains %s' % message)
        return None


    replyId = eventObj.get('in_reply_to_status_id_str')
    originId = eventObj.get('id_str')
    targetId = ""

    if replyId :
        targetId = replyId
    else : 
        targetId = originId

    

    auth = initApiObject()
            
            
    #r = twitterAPI.request('statuses/retweet/%s.json' % targetId, {})
    print('issue retweet begin')
    api = tweepy.API(auth)
    try:
        retweetUserList = api.get_retweeter_ids(targetId)
        
        if('1538767694127693825' in retweetUserList):
            api.unretweet(targetId)
    except:
        print('except get retweet user')
    

    
    api.retweet(targetId)
    print('issue retweet end')
    
    return None           
