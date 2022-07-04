#from TwitterAPI import TwitterAPI
import tweepy
import os
import telegram
import psycopg2   
import json

CONSUMER_KEY = os.environ.get('CONSUMER_KEY', None)
CONSUMER_SECRET = os.environ.get('CONSUMER_SECRET', None)

ACCESS_TOKEN = os.environ.get('ACCESS_TOKEN', None)
ACCESS_TOKEN_SECRET = os.environ.get('ACCESS_TOKEN_SECRET', None)

TELEGRAM_BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN', None)
TELEGRAM_CHAT_ID = os.environ.get('TELEGRAM_CHAT_ID', None)

DATABASE_URL = os.environ.get('DATABASE_URL', None)
     


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

    bot = telegram.Bot(TELEGRAM_BOT_TOKEN)


    #답글이 있는데.
    if(replyId):    
        #유저가 서로 다를경우
        if(replyUserID != replyOrgUserID):
            try:
                bot.sendMessage(chat_id=TELEGRAM_CHAT_ID, text='Filterd Another User\nhttps://twitter.com/%s/status/%s\n-> https://twitter.com/%s/status/%s\n%s' % (replyUserScreenNm, replyId, replyOrgUserScreenNm, originId, message))
            except:
                print('except send telegram')
            
            return None
    
    #알티인 경우
    if(message[0:2] == 'RT') :
        try:
            bot.sendMessage(chat_id=TELEGRAM_CHAT_ID, text='Filterd RT\nhttps://twitter.com/%s/status/%s\n-> https://twitter.com/%s/status/%s\n%s' % (replyUserScreenNm, replyId, replyOrgUserScreenNm, originId, message))
        except:
            print('except send telegram')
            
        return None

    #언급이 없는 멘션은 제외
    if('@ffxiv_party_' not in message.lower()) :
        try:
            bot.sendMessage(chat_id=TELEGRAM_CHAT_ID, text='Filterd NO Mention\nhttps://twitter.com/%s/status/%s\n-> https://twitter.com/%s/status/%s\n%s' % (replyUserScreenNm, replyId, replyOrgUserScreenNm, originId, message))
        except:
            print('except send telegram')
        return None
    
    if(replyUserScreenNm == 'FFXIV_PFinder' or replyOrgUserScreenNm == "FFXIV_PFinder") :
        try:
            bot.sendMessage(chat_id=TELEGRAM_CHAT_ID, text='FFXIV_PFinder Blocked\nhttps://twitter.com/%s/status/%s\n-> https://twitter.com/%s/status/%s\n%s' % (replyUserScreenNm, replyId, replyOrgUserScreenNm, originId, message))
        except:
            print('except send telegram')
        return None

    targetId = ""
    targetUserScreenNm = ""
    if replyId :
        targetId = replyId
        targetUserScreenNm = replyUserScreenNm

    else : 
        targetId = originId
        targetUserScreenNm = replyOrgUserScreenNm

    auth = initApiObject()
    print('issue retweet begin')
    api = tweepy.API(auth)

    replyContents = ''
    try:
        # 텍스트의 금지단어 확인
        status = api.get_status(targetId, tweet_mode = "extended")
        replyContents = status.full_text 
        
        blameList = ['공론화', 'evernote', '에버노트', '짜증', '공익', 'ㅅㅂ', 'ㅁㅊ', 'ㅆㅂ', '시발', '미친', '병신', 'ㅄ', 'ㅂㅅ']
        if(replyContents in blameList):
            bot.sendMessage(chat_id=TELEGRAM_CHAT_ID, text='Filterd Blame\nhttps://twitter.com/%s/status/%s\n-> https://twitter.com/%s/status/%s\n%s' % (replyUserScreenNm, replyId, replyOrgUserScreenNm, originId, replyContents))
            return None
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
    
    #취소가 포함 시 리트윗 취소
    if("취소" in message):
        try:
            bot.sendMessage(chat_id=TELEGRAM_CHAT_ID, text='UnRetweet Success\nhttps://twitter.com/%s/status/%s\n-> https://twitter.com/%s/status/%s\n%s' % (replyUserScreenNm, replyId, replyOrgUserScreenNm, originId, replyContents))
            api.unretweet(targetId)
        except:
            print('except send telegram')
    else:
        try:
            api.retweet(targetId)
            bot.sendMessage(chat_id=TELEGRAM_CHAT_ID, text='Success\nhttps://twitter.com/%s/status/%s\n-> https://twitter.com/%s/status/%s\n%s' % (replyUserScreenNm, replyId, replyOrgUserScreenNm, originId, replyContents))
        except:
            print('except send telegram')


    try: 
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        #conn = psycopg2.connect(dbname='dear42v48752o6', user='isaqnovgiqqjow', password='44fb147180e478a7059983d8e84b60b8aa48a1c0b2ce6c31689abb5398dc3787', host='ec2-44-206-11-200.compute-1.amazonaws.com', port=5432)
        cursor = conn.cursor()

        cursor.execute("CALL public.\"insTweet\"('%s')" % json.dumps([{
            "tweetid" : targetId,
            "shorttext" : message,
            "fulltext" : replyContents,
            "tweeturl" : 'https://twitter.com/%s/status/%s' % (targetUserScreenNm, targetId)
        }]))

        #sql = " INSERT INTO {schema}.\"{table}\"(tweetid, shorttext, fulltext, tweeturl) VALUES ('{tweetid}','{shorttext}','{fulltext}','{tweeturl}') ;".format(schema='public',table='Tweet',tweetid=targetId,shorttext=message,fulltext=replyContents,tweeturl='https://twitter.com/%s/status/%s' % (targetUserScreenNm, targetId))
        #cursor.execute(sql)
        conn.commit()

        cursor.close()
        conn.close()

    except Exception as e:                             # 예외가 발생했을 때 실행됨
        print('except db connect %s' % e)
    # #리트윗 성공 시 RT 완료이라는 답글을 단다
    # try:
    #     print('mention begin')
    #     api.update_status(status = "@%s RT 완료" % replyOrgUserScreenNm, in_reply_to_status_id = originId)
    #     print('mention end')

    # except:
    #     print('except mention user')

    print('issue retweet end')
    
    return None           
