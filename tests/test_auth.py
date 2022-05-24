from base64 import b64encode
from urllib import response
import pytest
from models import User

"""test for to check if the connection is okay"""


def test_ping(client):
    response = client.get("/ping")
    assert b"ok" in response.data
    assert response.status_code == 200


"""test for login without authorization"""


def test_login_fail1(client):
    response = client.get("/login")
    assert response.status_code == 401


"""test for login with non existing user"""


def test_login_fail2(client):
    credentials = b64encode(b"abc111@gmail.com:1234").decode('utf-8')
    response = client.get(
        "/login", headers={"Authorization": f"Basic {credentials}"})
    assert response.status_code == 401


"""test for login with exisitng user and valid authorization"""


def test_login_success(client):
    credentials = b64encode(b"abc@gmail.com:1234").decode('utf-8')
    response = client.get(
        "/login", headers={"Authorization": f"Basic {credentials}"})
    pytest.access_token = response.json['token']
    assert pytest.access_token is not None
    assert response.status_code == 200


"""test for retrieving the all users without access token"""


def test_get_users_fail(client):
    response = client.get("/user")
    assert response.headers.get('content-type') == 'application/json'
    assert b"Access Token is not present!" in response.data
    assert response.status_code == 401


"""test for retrieving the all users"""


def test_get_users_success(client):
    response = client.get(
        "/user", headers={"access-token": pytest.access_token})
    assert response.headers.get('content-type') == 'application/json'
    assert b"users" in response.data
    assert response.status_code == 200


"""test for retrieving a specific exising user by public id without access token"""


def test_get_user_fail1(client, app):
    with app.app_context():
        user = User.query.first()
        public_id = user.public_id
        response = client.get("/user/"+public_id)
        assert b"Access Token is not present!" in response.data
        assert response.status_code == 401


"""test for retrieving a specific non exising user by public id"""


def test_get_user_fail2(client):
    response = client.get(
        "/user/test_id", headers={"access-token": pytest.access_token})
    assert b"User Not found!" in response.data
    assert response.status_code == 404


"""test for retrieving a specific exising user by public id"""


def test_get_user_success(client, app):
    with app.app_context():
        user = User.query.first()
        public_id = user.public_id
        response = client.get("/user/"+public_id,
                              headers={"access-token": pytest.access_token})
        assert b"user" in response.data
        assert response.status_code == 200


"""test for creating new user with valid input"""


def test_create_user_success(client):
    new_user_data = {
        "email": "aaa@gmail.com",
        "password": "pwd123"
    }
    response = client.post("/user", json=new_user_data,
                           headers={"access-token": pytest.access_token})
    assert b"New user created Succesfully!" in response.data
    assert response.status_code == 201


"""test for creating new user with invalid input"""


def test_create_user_fail1(client):
    new_user_data = {}
    response = client.post("/user", json=new_user_data,
                           headers={"access-token": pytest.access_token})
    assert b"New user not created!Please check the input data!" in response.data
    assert response.status_code == 400


"""test for creating new user with valid input without access token"""


def test_create_user_fail2(client):
    new_user_data = {
        "email": "aaa@gmail.com",
        "password": "pwd123"
    }
    response = client.post("/user", json=new_user_data)
    assert b"Access Token is not present!" in response.data
    assert response.status_code == 401


"""test for deleting user with invalid input"""


def test_delete_user_fail1(client, app):
    with app.app_context():
        response = client.delete(
            "/user/test_id", headers={"access-token": pytest.access_token})
        assert b"User Not found!" in response.data
        assert response.status_code == 404


"""test for deleting user with valid input without access token"""


def test_delete_user_fail2(client, app):
    with app.app_context():
        user = User.query.filter_by(email="aaa@gmail.com").first()
        public_id = user.public_id
        response = client.delete("/user/"+public_id)
        assert b"Access Token is not present!" in response.data
        assert response.status_code == 401


"""test for deleting user with valid input"""


def test_delete_user_success(client, app):
    with app.app_context():
        user = User.query.filter_by(email="aaa@gmail.com").first()
        public_id = user.public_id
        response = client.delete(
            "/user/"+public_id, headers={"access-token": pytest.access_token})
        assert b"The user has been deleted!" in response.data
        assert response.status_code == 200
