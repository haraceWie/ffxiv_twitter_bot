#from TwitterAPI import TwitterAPI
import tweepy
import os
import telegram
import psycopg2   
import json
import pymysql
import datetime
import pytz
import requests
import json


CONSUMER_KEY = os.environ.get('CONSUMER_KEY', None)
CONSUMER_SECRET = os.environ.get('CONSUMER_SECRET', None)

ACCESS_TOKEN = os.environ.get('ACCESS_TOKEN', None)
ACCESS_TOKEN_SECRET = os.environ.get('ACCESS_TOKEN_SECRET', None)

TELEGRAM_BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN', None)
TELEGRAM_CHAT_ID = os.environ.get('TELEGRAM_CHAT_ID', None)

DATABASE_URL = os.environ.get('DATABASE_URL', None)
     
PREDEFINED_KEYWORD = [
    {"Keyword" : "변옥", "TagList" : ["변옥"]}
  , {"Keyword" : "영식", "TagList" : ["영식"]}
  , {"Keyword" : "변영", "TagList" : ["변옥", "영식"]}
  , {"Keyword" : "절렉", "TagList" : ["절렉"]}
  , {"Keyword" : "절테마", "TagList" : ["절테마"]}
  , {"Keyword" : "절 테마", "TagList" : ["절테마"]}
  , {"Keyword" : "절바하", "TagList" : ["절바하"]}
  , {"Keyword" : "절 바하", "TagList" : ["절바하"]}
  , {"Keyword" : "절용시", "TagList" : ["절용시"]}
  , {"Keyword" : "절 용시", "TagList" : ["절용시"]}

  , {"Keyword" : "구인", "TagList" : ["구인"]}
  , {"Keyword" : "구직", "TagList" : ["구직"]}
  , {"Keyword" : "고정팟", "TagList" : ["고정팟"]}
  , {"Keyword" : "사장", "TagList" : ["사장팟"]}

  , {"Keyword" : "1층", "TagList" : ["1층"]}
  , {"Keyword" : "2층", "TagList" : ["2층"]}
  , {"Keyword" : "3층", "TagList" : ["3층"]}
  , {"Keyword" : "4층", "TagList" : ["4층"]}

  , {"Keyword" : "1-2층", "TagList" : ["1층", "2층"]}
  , {"Keyword" : "1-3층", "TagList" : ["1층", "2층", "3층"]}
  , {"Keyword" : "1-4층", "TagList" : ["1층", "2층", "3층", "4층"]}
  , {"Keyword" : "2-3층", "TagList" : ["2층", "3층"]}
  , {"Keyword" : "2-4층", "TagList" : ["2층", "3층", "4층"]}
  , {"Keyword" : "3-4층", "TagList" : ["3층", "4층"]}

  , {"Keyword" : "1~2층", "TagList" : ["1층", "2층"]}
  , {"Keyword" : "1~3층", "TagList" : ["1층", "2층", "3층"]}
  , {"Keyword" : "1~4층", "TagList" : ["1층", "2층", "3층", "4층"]}
  , {"Keyword" : "2~3층", "TagList" : ["2층", "3층"]}
  , {"Keyword" : "2~4층", "TagList" : ["2층", "3층", "4층"]}
  , {"Keyword" : "3~4층", "TagList" : ["3층", "4층"]}

  , {"Keyword" : "1층-2층", "TagList" : ["1층", "2층"]}
  , {"Keyword" : "1층-3층", "TagList" : ["1층", "2층", "3층"]}
  , {"Keyword" : "1층-4층", "TagList" : ["1층", "2층", "3층", "4층"]}
  , {"Keyword" : "2층-3층", "TagList" : ["2층", "3층"]}
  , {"Keyword" : "2층-4층", "TagList" : ["2층", "3층", "4층"]}
  , {"Keyword" : "3층-4층", "TagList" : ["3층", "4층"]}

  , {"Keyword" : "1층~2층", "TagList" : ["1층", "2층"]}
  , {"Keyword" : "1층~3층", "TagList" : ["1층", "2층", "3층"]}
  , {"Keyword" : "1층~4층", "TagList" : ["1층", "2층", "3층", "4층"]}
  , {"Keyword" : "2층~3층", "TagList" : ["2층", "3층"]}
  , {"Keyword" : "2층~4층", "TagList" : ["2층", "3층", "4층"]}
  , {"Keyword" : "3층~4층", "TagList" : ["3층", "4층"]}

  , {"Keyword" : "1-2", "TagList" : ["1층", "2층"]}
  , {"Keyword" : "1-3", "TagList" : ["1층", "2층", "3층"]}
  , {"Keyword" : "1-4", "TagList" : ["1층", "2층", "3층", "4층"]}
  , {"Keyword" : "2-3", "TagList" : ["2층", "3층"]}
  , {"Keyword" : "2-4", "TagList" : ["2층", "3층", "4층"]}
  , {"Keyword" : "3-4", "TagList" : ["3층", "4층"]}

  , {"Keyword" : "1~2", "TagList" : ["1층", "2층"]}
  , {"Keyword" : "1~3", "TagList" : ["1층", "2층", "3층"]}
  , {"Keyword" : "1~4", "TagList" : ["1층", "2층", "3층", "4층"]}
  , {"Keyword" : "2~3", "TagList" : ["2층", "3층"]}
  , {"Keyword" : "2~4", "TagList" : ["2층", "3층", "4층"]}
  , {"Keyword" : "3~4", "TagList" : ["3층", "4층"]}
]

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


    
    if(replyUserScreenNm == 'FFXIV_PFinder' or replyOrgUserScreenNm == "FFXIV_PFinder" or replyUserScreenNm == 'FFIXV_14' or replyOrgUserScreenNm == "FFIXV_14" or replyOrgUserScreenNm == "uaplnslza6CHzO7" or replyUserScreenNm == "uaplnslza6CHzO7" or replyOrgUserScreenNm == "ff14_creamswoo" or replyUserScreenNm == "ff14_creamswoo" or replyOrgUserScreenNm == "kamain00" or replyUserScreenNm == "kamain00" or replyOrgUserScreenNm == "SasageEon59921" or replyUserScreenNm == "SasageEon59921" or replyOrgUserScreenNm == "224_ff14" or replyUserScreenNm == "224_ff14" ) :
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
        
        blameList = ['공론화', 'evernote', '에버노트', '짜증', '공익', '시발', '미친', '병신', '메갈', '한남', '사사게', '뒷담', '앞담', '한녀', '디씨', '갤벤']
        #if(replyContents in blameList):
        if any(keyword in replyContents for keyword in blameList):
            bot.sendMessage(chat_id=TELEGRAM_CHAT_ID, text='Filterd Blame Keyword\nhttps://twitter.com/%s/status/%s\n-> https://twitter.com/%s/status/%s\n%s' % (replyUserScreenNm, replyId, replyOrgUserScreenNm, originId, replyContents))
            return None
    except:
        print('except get tweetStatus')


    #언급이 없는 멘션은 제외
    if(replyId) :     
        if('@ffxiv_party_' not in message.lower()) :
            
            try:
                bot.sendMessage(chat_id=TELEGRAM_CHAT_ID, text='Filterd NO Mention\nhttps://twitter.com/%s/status/%s\n-> https://twitter.com/%s/status/%s\n%s' % (replyUserScreenNm, replyId, replyOrgUserScreenNm, originId, message))
            except:
                print('except send telegram')
            return None
    else :
        if('@ffxiv_party_' not in replyContents.lower()) :
            
            try:
                bot.sendMessage(chat_id=TELEGRAM_CHAT_ID, text='Filterd NO Mention\nhttps://twitter.com/%s/status/%s\n-> https://twitter.com/%s/status/%s\n%s' % (replyUserScreenNm, replyId, replyOrgUserScreenNm, originId, message))
            except:
                print('except send telegram')
            return None

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


    conn = None
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

        board_write('free', '알티자동등록', replyContents + '\nhttps://twitter.com/%s/status/%s' % (targetUserScreenNm, targetId), 'admin', '최고관리자')
    except Exception as e:     
        if(conn):
            conn.close()

        print('except db connect : %s' % e)




    # #리트윗 성공 시 RT 완료이라는 답글을 단다
    # try:
    #     print('mention begin')
    #     api.update_status(status = "@%s RT 완료" % replyOrgUserScreenNm, in_reply_to_status_id = originId)
    #     print('mention end')

    # except:
    #     print('except mention user')

    print('issue retweet end')
    
    return None           


def getTweetListFromDatabase(param) :
    conn = None
    try: 
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        cursor = conn.cursor()

        sql = ""
        if(param):
            sql = " SELECT tweetid, fulltext, tweeturl, insdts FROM {schema}.\"{table}\" WHERE fulltext LIKE '%".format(schema='public',table='Tweet') + param + "%' ORDER BY InsDts DESC LIMIT 200;"
        else :
            sql = " SELECT tweetid, fulltext, tweeturl, insdts FROM {schema}.\"{table}\" ORDER BY InsDts DESC LIMIT 200;".format(schema='public',table='Tweet')
            
        cursor.execute(sql)
        rows = cursor.fetchall()

        conn.commit()
        cursor.close()
        conn.close()

        convertRows = []
        for row in rows:
            tweetID = row[0]
            fullText = row[1]
            tweetUrl = row[2]
            insDts = row[3]

            tagList = []
            for keyword in PREDEFINED_KEYWORD:
                if (keyword.get('Keyword') in fullText) :
                    for tag in keyword.get('TagList'):
                        tagList.append(tag)
                        
            convertRow = {
                'TagList' : sorted(list(set(tagList))),
                'TweetUrl' : tweetUrl,
                'InsDts' : str(insDts),
                'FullText' : fullText,
                'TweetID' : tweetID
            }
            #if(len(convertRow.get('TagList')) > 0):
            convertRows.append(convertRow) 

        return convertRows
        

    except Exception as e:     
        if(conn):
            conn.close()

        print('except db connect : %s' % e)
        return []


def board_write(board, subject, content, mb_id, nickname):
    # MySQL connection 및 cursor를 생성합니다.
    conn = pymysql.connect(host = '203.245.44.84', 
                           user = 'haracewie', 
                           password = 'asas7146!!',
                           db = 'haracewie', 
                           port=3306,
                           charset = 'utf8')
    curs = conn.cursor()
    
    ca_name = '기타'
    wr_1 = '기타'
    if ('용시' in content):
        ca_name = '절용시'
    elif  ('절렉' in content):
        ca_name = '절렉'
    elif  ('알렉' in content):
        ca_name = '절렉'
    elif  ('절테마' in content):
        ca_name = '절테마'
    elif  ('절바하' in content):
        ca_name = '절바하'
    elif  ('연영' in content):
        ca_name = '연영'
    elif  ('연옥' in content):
        ca_name = '연영'
    elif  ('변영' in content):
        ca_name = '변영'
    elif  ('변옥' in content):
        ca_name = '변영'
    elif  ('영식' in content):
        ca_name = '연영'

    if ('대타' in content):
        wr_1 = '대타'
    elif ('구인' in content):
        wr_1 = '구인'
    elif  ('구직' in content):
        wr_1 = '구직'
    elif  ('사장팟' in content):
        wr_1 = '사장팟'
    elif  ('모출' in content):
        wr_1 = '구인'

    API_HOST = "https://girinworkshop.pe.kr/api/twitter_migrate.php"
    headers = {'Content-Type': 'application/json', 'charset': 'UTF-8', 'Accept': '*/*'}
    body = {
          "bo_table" : board
          , "ca_name" : ca_name
          , "mb_id" : "admin"
          , "wr_subject" : subject
          , "wr_content" : content
          , "wr_1" : wr_1
     }
    
    try:
        response = requests.post(url, headers=headers, data=json.dumps(body, ensure_ascii=False, indent="\t"))
        print("response status %r" % response.status_code)
        print("response text %r" % response.text)
          
    except Exception as ex:
        print(ex)
    

