from flask import request, jsonify, g, abort
from flask_httpauth import HTTPBasicAuth
import json
import requests

from simple_api import app
from simple_api.firebase_authentication import firebase_auth
from simple_api.token_system import generate_auth_token, verify_auth_token

http_basic_auth = HTTPBasicAuth()


@app.route("/")
@app.route("/index")
def index():
    return jsonify(
        {
            "endpoints": [
                {
                    "endpoint": "/api/register",
                    "about": "register email and password through POST",
                },
                {
                    "endpoint": "/api/token",
                    "about": "send email and password to get authentication token to access the other parts of api",
                },
            ]
        }
    )


@app.route("/api/token")
@http_basic_auth.login_required
def get_auth_token():
    # g.user was set by the verify_password method to store
    # the user object for further usage
    token = generate_auth_token(g.user["idToken"])
    return jsonify({"token": token.decode("ascii")})


@app.route("/api/resource")
@http_basic_auth.login_required
def get_secret_resource():
    return "This is the secret Resource"


def _parse_firebase_error(e):
    error_json = e.args[1]
    error = json.loads(error_json)
    error_code = error["error"]["code"]
    return error, error_code


@app.route("/api/register", methods=["POST"])
def register_user():
    email = request.json.get("email")
    password = request.json.get("password")

    try:
        user = firebase_auth.create_user_with_email_and_password(email, password)
        firebase_auth.send_email_verification(user["idToken"])
    except requests.exceptions.HTTPError as e:
        error, error_code = _parse_firebase_error(e)
        return jsonify(error), error_code
    return jsonify({"email": email, "message": "Email verification link sent"}), 200


@app.route("/api/reset-password", methods=["POST"])
def reset_password():
    email = request.json.get("email")

    try:
        firebase_auth.send_password_reset_email(email)
    except requests.exceptions.HTTPError as e:
        error, error_code = _parse_firebase_error(e)
        return jsonify(error), error_code
    return jsonify({"email": email, "message": "Password reset link sent"}), 200


@http_basic_auth.verify_password
def verify_password(email_or_token, password):
    # TODO: improve exception handling (no internet, etc...)
    if verify_auth_token(email_or_token):
        return True

    try:
        # user is just a dictionary returned by firebase
        user = firebase_auth.sign_in_with_email_and_password(email_or_token, password)
        # set g.user to store the user object
        # g acts like a global variable which other
        # functions like get_auth_token() can use
        g.user = user
        return True
    except:
        return False
