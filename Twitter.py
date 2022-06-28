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

    replyUserID = eventObj.get('in_reply_to_user_id')
    replyUserScreenNm = eventObj.get('in_reply_to_screen_name')
        
    replyOrgUserID = eventObj.get('user').get('id')
    replyOrgUserScreenNm = eventObj.get('user').get('screen_name')

    replyId = eventObj.get('in_reply_to_status_id_str')
    originId = eventObj.get('id_str')

    token = "5461873552:AAGd2lqr8v29cNDSgWPxYH71FD18lTWt5UQ"
    bot = telegram.Bot(token)


    #답글이 있는데.
    if(replyId):    
        #유저가 서로 다를경우
        if(replyUserID != replyOrgUserID):
            try:
                bot.sendMessage(chat_id='529686074', text='Slice[%s]\nFilterd Another User\nhttps://twitter.com/%s/status/%s\n-> https://twitter.com/%s/status/%s\n%s' % (message[0:2], replyUserScreenNm, replyId, replyOrgUserScreenNm, originId, message))
            except:
                print('except send telegram')
            
            return None
    
    #알티인 경우
    if(message[0:2] == 'RT') :
        try:
            bot.sendMessage(chat_id='529686074', text='Slice[%s]\nFilterd RT\nhttps://twitter.com/%s/status/%s\n-> https://twitter.com/%s/status/%s\n%s' % (message[0:2], replyUserScreenNm, replyId, replyOrgUserScreenNm, originId, message))
        except:
            print('except send telegram')
            
        return None

    #언급이 없는 멘션은 제외
    if('@ffxiv_party_' not in message.lower()) :
        try:
            bot.sendMessage(chat_id='529686074', text='Slice[%s]\nFilterd NO Mention\nhttps://twitter.com/%s/status/%s\n-> https://twitter.com/%s/status/%s\n%s' % (message[0:2], replyUserScreenNm, replyId, replyOrgUserScreenNm, originId, message))
        except:
            print('except send telegram')
        return None
    
    if(replyUserScreenNm == 'FFXIV_PFinder' or replyOrgUserScreenNm == "FFXIV_PFinder") :
        try:
            bot.sendMessage(chat_id='529686074', text='Slice[%s]\nFFXIV_PFinder Blocked\nhttps://twitter.com/%s/status/%s\n-> https://twitter.com/%s/status/%s\n%s' % (message[0:2], replyUserScreenNm, replyId, replyOrgUserScreenNm, originId, message))
        except:
            print('except send telegram')
        return None

    targetId = ""

    if replyId :
        targetId = replyId
    else : 
        targetId = originId

    auth = initApiObject()
    print('issue retweet begin')
    api = tweepy.API(auth)
        
    replyContents = ''
    try:
        # 텍스트의 금지단어 확인
        status = api.get_status(targetId, tweet_mode = "extended")
        replyContents = status.full_text 
        
    except:
        print('except get tweetStatus')




    # 리트윗한 유저 리스트를 가져와서 이미 리트윗을 했으면 리트윗을 해제한다.
    try:
        retweetUserList = api.get_retweeter_ids(targetId)

        
        if(1538767694127693825 in retweetUserList):
            print('unretweet begin')
            api.unretweet(targetId)
            print('unretweet end')
    except:
        print('except get retweet user')
    
    api.retweet(targetId)

    try:
        bot.sendMessage(chat_id='529686074', text='Slice[%s]\nSuccess\nhttps://twitter.com/%s/status/%s\n-> https://twitter.com/%s/status/%s\n%s' % (message[0:2], replyUserScreenNm, replyId, replyOrgUserScreenNm, originId, replyContents))
    except:
        print('except send telegram')

    # #리트윗 성공 시 RT 완료이라는 답글을 단다
    # try:
    #     print('mention begin')
    #     api.update_status(status = "@%s RT 완료" % replyOrgUserScreenNm, in_reply_to_status_id = originId)
    #     print('mention end')

    # except:
    #     print('except mention user')

    print('issue retweet end')
    
    return None           
