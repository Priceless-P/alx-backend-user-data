#!/usr/bin/env python3
""" Session authentication
views"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models.user import User
from os import getenv


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def login():
    """ POST /auth_session/login
    Return
        - Logged in user
    """
    user_email = request.form.get('email')

    if not user_email:
        return jsonify({"error": "email missing"}), 400

    user_password = request.form.get('password')

    if not user_password:
        return jsonify({"error": "password missing"}), 400

    try:
        users = User.search({'email': user_email})
    except Exception:
        return jsonify({"error": "no user found for this email"}), 404

    if not users:
        return jsonify({"error": "no user found for this email"}), 404

    for user in users:
        if not user.is_valid_password(user_password):
            return jsonify({"error": "wrong password"}), 401

    from api.v1.app import auth
    user = users[0]
    session_id = auth.create_session(user.id)

    SESSION_NAME = getenv("SESSION_NAME")

    user_json = jsonify(user.to_json())
    user_json.set_cookie(SESSION_NAME, session_id)

    return user_json


@app_views.route('/auth_session/logout',
                 methods=['DELETE'], strict_slashes=False)
def logout():
    """ DELETE /auth_session/logout
    Return:
        - Empty dictionary if deleted
    """
    from api.v1.app import auth

    delete_ = auth.destroy_session(request)

    if not delete_:
        abort(404)
    return jsonify({}), 200
