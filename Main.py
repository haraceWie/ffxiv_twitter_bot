#!/usr/bin/env python
from flask import Flask, request, send_from_directory, make_response
from flask_cors import CORS
from http import HTTPStatus

import Twitter, hashlib, hmac, base64, os, logging, json

CONSUMER_SECRET = os.environ.get('CONSUMER_SECRET', None)
CURRENT_USER_ID = os.environ.get('CURRENT_USER_ID', None)
	     
app = Flask(__name__)	
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

@app.route('/')
def default_route():        
    return send_from_directory('www', 'index.html')    		      


# CRC CHECK
@app.route("/webhook", methods=["GET"])
def twitterCrcValidation():
    
    crc = request.args['crc_token']
  
    validation = hmac.new(
        key=bytes(CONSUMER_SECRET, 'utf-8'),
        msg=bytes(crc, 'utf-8'),
        digestmod = hashlib.sha256
    )
    digested = base64.b64encode(validation.digest())
    response = {
        'response_token': 'sha256=' + format(str(digested)[2:-1])
    }
    print('responding to CRC call')

    return json.dumps(response)   
        
# CRC CHECK
@app.route("/api/tweet", methods=["GET"])
def getTweetListFromDatabase():
    

    response = Twitter.getTweetListFromDatabase()
    return json.dumps({
        "Items" : response,
        "Count" : len(response)
    }, ensure_ascii=False)   


# CRC CHECK
@app.route("/api/party", methods=["GET"])
def getTweetListFromDatabase():
    
    param = request.args.get('search')
    response = Twitter.getTweetListFromDatabase(param)

    

    return json.dumps(response, ensure_ascii=False)   



# 트위터 웹훅 수신부 
@app.route("/webhook", methods=["POST"])
def twitterEventReceived():
    requestJson = request.get_json()
    if 'tweet_create_events' in requestJson.keys():
        print('issued tweet_create_events')

        messageObject = requestJson['tweet_create_events'][0]
        
        Twitter.processMentionEvent(messageObject)
        return ('', HTTPStatus.OK)
    else:
        return ('', HTTPStatus.OK)
    
    return ('', HTTPStatus.OK)

                	    
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 65010))
    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)
    app.run(host='0.0.0.0', port=port, debug=True)
