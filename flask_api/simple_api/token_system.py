from simple_api import app
from simple_api.firebase_authentication import firebase_auth
from itsdangerous import (
    TimedJSONWebSignatureSerializer as Serializer,
    BadSignature,
    SignatureExpired,
)


def generate_auth_token(idToken, expiration=3600):
    s = Serializer(app.config["SECRET_KEY"], expires_in=expiration)
    return s.dumps({"idToken": idToken})


def verify_auth_token(token):
    s = Serializer(app.config["SECRET_KEY"])
    try:
        data = s.loads(token)
    except SignatureExpired:
        return None  # valid token, but expired
    except BadSignature:
        return None  # invalid token

    return True
