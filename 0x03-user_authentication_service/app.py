#!/usr/bin/env python3
"""
Basic Flask app
"""
from flask import Flask
from auth import Auth
import bcrypt


app = Flask(__name__)
AUTH = Auth()


@app.route('/', methods=['GET'])
def basic():
    return jsonify({"message": "Bienvenue"})


@app.route('users/<email>/<password>', methods=['POST'])
def register_user(email, password):
    user = AUTH.find_user_by(email)
    try:
        if user is None:
            user = User(email, password)
            session.add(user)
            session.commit()

            return jsonify({"email": email, "message": "user created"})
    except Exception as e:
        return jsonify({"message": "email already registered"}), 400


def valid_login(email: str, password: str) -> bool:
        """
        Credentials validation

        Args: - email(str)
              - password(str)

        Returns: Boolean
        """
        user = AUTH.find_user_by(email)

        if user:
            password = user.password.encode('utf-8')






if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
