
# Task and Solution Description

This is a URL shortner Flask Application.The task includes the user authentication and URL shortner module.

# Running the Application

- Clone the repository and change to branch ```develop```.
- In the terminal run the folowing commands to setuop the application in local enviornment.
```
  pipenv shell
```
```
  pip install -r requirements.txt
```
```
  pip install -Iv PyJWT==2.4.0
```
```
  export FLASK_APP=app.py 
```
- To run the application run ```flask run``` in the terminal. Application will be run on ```http://127.0.0.1:5000```.

## API Reference

To run APIs, use a client like Postman.


#### Login

```http
  GET /login
```
For login ```Basic Authorization``` is required.
![This is an image](./readme_images/login.jpg)

#### Get all users

```http
  GET /user
```
In ```Headers``` need to pass the access-token retrieved by the login.
![This is an image](./readme_images/users.jpg)

## Technical choices and Architecture

Used **Flask** framework with **sqlite** database for the URL shortner Application.

```bash
├── app.py
├── auth.py
├── shortner.py
├── models.py
├── tests
│   ├── conftest.py
│   ├── test_auth.py
│   └── test_shortner.py
├── requirements.txt
└── README.md
```


## Running Tests

To run tests, run the following command in the terminal

```
  python -m pytest
```
![This is an image](./readme_images/tests.jpg)

### Trade-offs and Imporovents

- I have used JSON Web Token(jwt) for authentication. But due to dependancy between jwt and PyJWT, it is better to upgrade the application to Flask-JWT-Extended.
- It is better to dockerize the application for easy and effective deployment. 