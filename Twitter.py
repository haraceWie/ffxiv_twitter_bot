#from TwitterAPI import TwitterAPI
import tweepy
import os
import telegram

CONSUMER_KEY = os.environ.get('CONSUMER_KEY', None)
CONSUMER_SECRET = os.environ.get('CONSUMER_SECRET', None)

ACCESS_TOKEN = os.environ.get('ACCESS_TOKEN', None)
ACCESS_TOKEN_SECRET = os.environ.get('ACCESS_TOKEN_SECRET', None)


def initApiObject():
    
    #user authentication
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

    return auth

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


    # 리트윗한 유저 리스트를 가져와서 이미 리트윗을 했으면 리트윗을 해제한다.
    try:
        retweetUserList = api.get_retweeter_ids(targetId)
        print(retweetUserList)

        
        if(1538767694127693825 in retweetUserList):
            print('unretweet begin')
            api.unretweet(targetId)
            print('unretweet end')
    except:
        print('except get retweet user')
    
    api.retweet(targetId)

    try:
        token = "5461873552:AAGd2lqr8v29cNDSgWPxYH71FD18lTWt5UQ"
        bot = telegram.Bot(token)
        bot.sendMessage(chat_id='529686074', text='%s' % message)
    except:
        print('except send telegram')

    # #리트윗 성공 시 리트윗 성공이라는 답글을 단다
    # try:
    #     print('mention begin')
    #     api.update_status(status = "RT 완료", in_reply_to_status_id = originId, auto_populate_reply_metadata=True)
    #     print('mention end')

    # except:
    #     print('except mention user')

    print('issue retweet end')
    
    return None           
