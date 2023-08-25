#!/usr/bin/python3
""" Endpoints for users apis """

from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage
from models.user import User


@app_views.route('/users', strict_slashes=False, methods=['GET'])
def get_users():
    """ retrieves a list of all user objects """
    users = []
    for user in storage.all("User").values():
        users.append(user.to_dict())
    return jsonify(users)


@app_views.route('/users/<string:user_id>', methods=['GET'],
                 strict_slashes=False)
def get_user(user_id):
    """information of a user according to the identification"""
    user = storage.get("User", user_id)
    if user is not None:
        return jsonify(user.to_dict())
    abort(404)


@app_views.route('/users/<string:user_id>', strict_slashes=False,
                 methods=['DELETE'])
def delete_user(user_id):
    """Deletes a user object."""
    user = storage.get('User', user_id)
    if user is not None:
        storage.delete(user)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route('/users', strict_slashes=False, methods=['POST'])
def create_user():
    """Creates a new user object."""
    new_user = request.get_json()

    if not new_user:
        abort(400, description='Not a JSON')
    if 'email' not in new_user.keys():
        abort(400, description='Missing email')
    if 'password' not in new_user.keys():
        abort(400, description='Missing password')

    user = User(**new_user)
    user.save()

    return make_response(jsonify(user.to_dict()), 201)


@app_views.route('/users/<string:user_id>', strict_slashes=False,
                 methods=['PUT'])
def update_user(user_id):
    """Updates a user object."""
    new_user = request.get_json()
    if not new_user:
        abort(400, description='Not a JSON')

    old_user = storage.get("User", user_id)
    if not old_user:
        abort(404)

    for key, value in new_user.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(old_user, key, value)

    old_user.save()
    return jsonify(old_user.to_dict()), 200
