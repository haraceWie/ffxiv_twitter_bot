#!/usr/bin/env python
from flask import Flask, request, send_from_directory, make_response
from flask_cors import CORS
from http import HTTPStatus
import flask_sqlalchemy
import flask_praetorian

import Twitter, hashlib, hmac, base64, os, logging, json

CONSUMER_SECRET = os.environ.get('CONSUMER_SECRET', None)
CURRENT_USER_ID = os.environ.get('CURRENT_USER_ID', None)
	     
app = Flask(__name__)	
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

app.config['SECRET_KEY'] = 'top secret'
app.config['JWT_ACCESS_LIFESPAN'] = {'hours': 24}
app.config['JWT_REFRESH_LIFESPAN'] = {'days': 30}

db = flask_sqlalchemy.SQLAlchemy()
guard = flask_praetorian.Praetorian()

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
    

    response = Twitter.getTweetListFromDatabase('')
    return json.dumps({
        "Items" : response,
        "Count" : len(response)
    }, ensure_ascii=False)   


# CRC CHECK
@app.route("/api/party", methods=["GET"])
def getPartyList():
    
    param = request.args.get('search')
    response = Twitter.getTweetListFromDatabase(param)

    

    return json.dumps({
        "Items" : response,
        "Count" : len(response)
    }, ensure_ascii=False)   



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



# A generic user model that might be used by an app powered by flask-praetorian
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Text, unique=True)
    password = db.Column(db.Text)
    roles = db.Column(db.Text)
    is_active = db.Column(db.Boolean, default=True, server_default='true')

    @property
    def rolenames(self):
        try:
            return self.roles.split(',')
        except Exception:
            return []

    @classmethod
    def lookup(cls, username):
        return cls.query.filter_by(username=username).one_or_none()

    @classmethod
    def identify(cls, id):
        return cls.query.get(id)

    @property
    def identity(self):
        return self.id

    def is_valid(self):
        return self.is_active




# Initialize the flask-praetorian instance for the app
guard.init_app(app, User)

# Initialize a local database for the example
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(os.getcwd(), 'database.db')}"
db.init_app(app)


# Add users for the example
with app.app_context():
    db.create_all( checkfirst=True)

    #data = User.query.filter_by(userid=userid, password=password).first()
    if db.session.query(User).filter_by(username='Yasoob').count() < 1:
        user = User()
        user.password = 'strongpassword'
        user.username = 'Yasoob'
        user.roles = 'Yasoob'
        db.session.add(user)
        # db.session.add(User(username='Yasoob',
        #   password=guard.hash_password('strongpassword'),
        #   roles='admin'
        #     ))
    db.session.commit()




  
@app.route('/api/login', methods=['POST'])
def login():
    """
    Logs a user in by parsing a POST request containing user credentials and
    issuing a JWT token.
    .. example::
       $ curl http://localhost:5000/api/login -X POST \
         -d '{"username":"Yasoob","password":"strongpassword"}'
    """
    req = request.get_json(force=True)
    username = req.get('username', None)
    password = req.get('password', None)
    user = guard.authenticate(username, password)
    ret = {'access_token': guard.encode_jwt_token(user)}
    return ret, 200

  
@app.route('/api/refresh', methods=['POST'])
def refresh():
    """
    Refreshes an existing JWT by creating a new one that is a copy of the old
    except that it has a refrehsed access expiration.
    .. example::
       $ curl http://localhost:5000/api/refresh -X GET \
         -H "Authorization: Bearer <your_token>"
    """
    print("refresh request")
    old_token = request.get_data()
    new_token = guard.refresh_jwt_token(old_token)
    ret = {'access_token': new_token}
    return ret, 200
  
  
@app.route('/api/protected')
@flask_praetorian.auth_required
def protected():
    """
    A protected endpoint. The auth_required decorator will require a header
    containing a valid JWT
    .. example::
       $ curl http://localhost:5000/api/protected -X GET \
         -H "Authorization: Bearer <your_token>"
    """
    return {'message': f'protected endpoint (allowed user {flask_praetorian.current_user().username})'}



                	    
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 65010))
    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)
    app.run(host='0.0.0.0', port=port, debug=True)






