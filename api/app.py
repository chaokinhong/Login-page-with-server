from flask import Flask, jsonify, request, session
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from matplotlib.style import use
from flask_session import Session
from itsdangerous import json
from models import db, User
from config import ApplicationConfig




app = Flask(__name__)
#load the configuration
app.config.from_object(ApplicationConfig)

# set up session(server-side session), so the session in flask will always be store in the server side
server_session = Session(app)

#set up password hash
bcrypt = Bcrypt(app)

# solve block by CORS
CORS(app,supports_credentials=True)

# init the application instance with db
db.init_app(app)

# create a new app context
with app.app_context():
    db.create_all()

# return info about current login user
@app.route('/@me')
def get_current_user(): 
    # if have invalid session will return none
    user_id = session.get('user_id')

    if not user_id:
        return jsonify({'error':'Unauthorized'}),401
    
    user = User.query.filter_by(id=user_id).first()
    return jsonify({
        'id':user.id,
        'email':user.email
    })





@app.route('/register',methods=["POST"])
def register_user():
    email = request.json["email"]
    password = request.json["password"]
    
    # return true if have an existing user
    user_exists = User.query.filter_by(email=email).first() is not None

    if user_exists:
        # status code 409: conflict
        return jsonify({'error':'User already exists'}),409 
    
    hashed_password = bcrypt.generate_password_hash(password)
    new_user = User(email=email, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    session['user_id'] = new_user.id

    return jsonify({
        'id': new_user.id,
        'email': new_user.email
    })
    

@app.route('/login', methods=["POST"])
def login_user():
    email = request.json["email"]
    password = request.json["password"]

    user = User.query.filter_by(email=email).first()

    # no user in sql
    if user is None:
        return jsonify({'error':'Unauthorized'}),401

    # is password check is wrong, wrong password
    if not bcrypt.check_password_hash(user.password,password):
        return jsonify({'error':'Unauthorized'}),401
    
    #if actually get successful login, server has no way to keep the login session alive,
    # so need to return a cookie to client (server side sessions)
    # store the data inside the session
    # user_id: uuid
    session['user_id'] = user.id

    return jsonify({
        'id': user.id,
        'email':user.email
    })

@app.route('/logout', methods=['POST'])
def logout():
    session.pop('user_id')
    return '200'
    
     


if __name__ == "__main__":
    app.run(debug=True)