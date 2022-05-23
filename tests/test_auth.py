from base64 import b64encode
from urllib import response
import pytest
from models import User

"""testing if the connection okay"""
def test_ping(client):
    response = client.get("/ping")
    assert b"ok" in response.data
    assert response.status_code == 200

"""trying to login without authorization"""
def test_login_fail1(client):
    response = client.get("/login")
    assert response.status_code == 401

"""trying to login with non existing user"""
def test_login_fail2(client):
    credentials = b64encode(b"abc111@gmail.com:1234").decode('utf-8')
    response = client.get("/login", headers={"Authorization": f"Basic {credentials}"})
    assert response.status_code == 401

"""login with exisitng user and authorization"""
def test_login_success(client):
    credentials = b64encode(b"abc@gmail.com:1234").decode('utf-8')
    response = client.get("/login", headers={"Authorization": f"Basic {credentials}"})
    pytest.access_token =  response.json['token']
    assert pytest.access_token is not None
    assert response.status_code == 200

"""retrieving the all users"""
def test_get_users_success(client):
    response = client.get("/user", headers={"access-token": pytest.access_token})
    assert response.headers.get('content-type') == 'application/json'
    assert b"users" in response.data
    assert response.status_code == 200

"""retrieving a specific non exising user by public id"""
def test_get_user_fail(client, app):
    response = client.get("/user/test_id", headers={"access-token": pytest.access_token})
    assert b"User Not found!" in response.data
    assert response.status_code == 200

"""retrieving a specific exising user by public id"""
def test_get_user_success(client, app):
    with app.app_context():
        user = User.query.first()
        public_id = user.public_id
        response = client.get("/user/"+public_id, headers={"access-token": pytest.access_token})
        assert b"user" in response.data
        assert response.status_code == 200

