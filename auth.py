from flask import Blueprint, request, jsonify,make_response, current_app
from models import User
from app import db
from flask_sqlalchemy import SQLAlchemy
import uuid
import jwt
from werkzeug.security import generate_password_hash, check_password_hash
import datetime
from functools import wraps

auth = Blueprint('auth', __name__)

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        print(request.headers)
        if 'access-token' in request.headers:
            token = request.headers['access-token']

        if not token:
            return jsonify({'message' : 'Access Token is not present!'}), 401

        try: 
            data = jwt.decode(token, current_app.config['SECRET_KEY'],algorithms=["HS256"])
            current_user = User.query.filter_by(public_id=data['public_id']).first()
        except:
            return jsonify({'message' : 'Access Token is invalid!'}), 401

        return f(current_user, *args, **kwargs)

    return decorated

@auth.route('/ping')
def index():
    return 'ok'

@auth.route('/user', methods=['GET'])
@token_required
def get_all_users(current_user):

    if not current_user:
        return jsonify({'message' : 'Autentication failed. Cannot perform that function!'})

    users = User.query.all()

    output = []

    for user in users:
        user_data = {}
        user_data['public_id'] = user.public_id
        user_data['email'] = user.email
        user_data['password'] = user.password
        output.append(user_data)

    return jsonify({'users' : output})

@auth.route('/user/<public_id>', methods=['GET'])
@token_required
def get_one_user(current_user, public_id):

    if not current_user:
        return jsonify({'message' : 'Autentication failed. Cannot perform that function!'})

    user = User.query.filter_by(public_id=public_id).first()

    if not user:
        return jsonify({'message' : 'User Not found!'})

    user_data = {}
    user_data['public_id'] = user.public_id
    user_data['email'] = user.email
    user_data['password'] = user.password

    return jsonify({'user' : user_data})

@auth.route('/user', methods=['POST'])
# def create_user():
@token_required
def create_user(current_user):
    if not current_user:
        return jsonify({'message' : 'Autentication failed. Cannot perform that function!'})

    data = request.get_json()

    hashed_password = generate_password_hash(data['password'], method='sha256')

    new_user = User(public_id=str(uuid.uuid4()), email=data['email'], password=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message' : 'New user created Succesfully!'})

@auth.route('/login')
def login():
    auth = request.authorization

    if not auth or not auth.username or not auth.password:
        return make_response('Cannot verify', 401, {'WWW-Authenticate' : 'Basic realm="Login required!"'})

    user = User.query.filter_by(email=auth.username).first()

    if not user:
        return make_response('Cannot verify', 401, {'WWW-Authenticate' : 'Basic realm="Login required!"'})

    if check_password_hash(user.password, auth.password):
        token = jwt.encode({'public_id' : user.public_id, 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, current_app.config['SECRET_KEY'])

        return jsonify({'token' : token})

    return make_response('Cannot verify', 401, {'WWW-Authenticate' : 'Basic realm="Login required!"'})