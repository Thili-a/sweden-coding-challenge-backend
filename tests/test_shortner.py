from flask import url_for
import pytest
from models import Link

"""test for creating a new link without access token"""
def test_create_link_fail1(client):
        new_link_data = {
            "original_url" : "https://en.wikipedia.org/wiki/Software_testing"
        }
        response = client.post("/create_link", json=new_link_data)
        assert b"Access Token is not present!" in response.data
        assert response.status_code == 401

"""test for creating a new link with invalid input"""
def test_create_link_fail2(client):
    new_link_data = {}
    response = client.post("/create_link", json=new_link_data, headers={"access-token": pytest.access_token})
    assert b"Link not found!" in response.data
    assert response.status_code == 400

"""test for creating a new link with valid input and access token"""
def test_create_link_success(client):
    response = client.get("/create_link")
    new_link_data = {
        "original_url" : "https://en.wikipedia.org/wiki/Software_testing"
    }
    response = client.post("/create_link", json=new_link_data, headers={"access-token": pytest.access_token})
    assert b"New link created successfully!" in response.data
    assert response.status_code == 201

"""test for trying to redirect to original url with invalid input """
def test_short_link_fail(client):
    response = client.get("/eH5v1")
    assert response.status_code == 404

"""test for redirecting to original url with valid input """
def test_short_link_success(client, app):
    with app.app_context():
        original_url = "https://en.wikipedia.org/wiki/Software_testing"
        link = Link.query.filter_by(original_url=original_url).first()
        short_url = link.short_url
        response = client.get("/"+short_url)
        assert b"https://en.wikipedia.org/wiki/Software_testing" in response.data

"""test for deleting link without access token"""
def test_delete_link_fail1(client, app):
    with app.app_context():
        original_url = "https://en.wikipedia.org/wiki/Software_testing"
        link = Link.query.filter_by(original_url=original_url).first()
        short_url = link.short_url
        response = client.delete("/delete_link/"+short_url)
        assert b"Access Token is not present!" in response.data
        assert response.status_code == 401

"""test for deleting link with invalid input"""
def test_delete_link_fail2(client, app):
    response = client.delete("/delete_link/test_1", headers={"access-token": pytest.access_token})
    assert b"Link not found!Check your Inputs!" in response.data
    assert response.status_code == 400

"""test for deleting link with valid input"""
def test_delete_link_success(client, app):
    with app.app_context():
        original_url = "https://en.wikipedia.org/wiki/Software_testing"
        link = Link.query.filter_by(original_url=original_url).first()
        short_url = link.short_url
        response = client.delete("/delete_link/"+short_url, headers={"access-token": pytest.access_token})
        assert b"The link has been deleted!" in response.data
        assert response.status_code == 200

