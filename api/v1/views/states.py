#!/usr/bin/python3
"""doc"""

from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage
from models.state import State


@app_views.route('/states', strict_slashes=False, methods=['GET'])
def get_statess():
    """ retrieves a list of all state objects """
    states = []
    for state in storage.all("State").values():
        states.append(state.to_dict())
    return jsonify(states)

@app_views.route('/states/<int:state_id>', strict_slashes=False,
                 methods=['GET'])
def get_state(state_id):
    """Retrieves a list of one State objects."""
    stat = storage.get('State', state_id)
    if stat is not None:
        return jsonify(stat.to_dict())
    else:
        abort(404)


@app_views.route('/states/<int:state_id>', strict_slashes=False,
                 methods=['DELETE'])
def delete_state(state_id):
    """Deletes a State object."""
    stat = storage.get('State', state_id)
    if stat is not None:
        storage.delete(stat)
        storage.save()
        return jsonify({})
    else:
        abort(404)


@app_views.route('/states', strict_slashes=False, methods=['POST'])
def create_state():
    """Creates a new State object."""
    data = request.get_json()

    if not data:
        abort(400, description='Not a JSON')

    if 'name' not in data.keys():
        abort(400, description='Missing name')

    state = State(**data)
    state.save()

    return make_response(jsonify(state.to_dict()), 201)


@app_views.route('/states/<int:state_id>', strict_slashes=False,
                 methods=['PUT'])
def update_state(state_id):
    """Updates a State object."""
    state = request.get_json()
    if not state:
        abort(400, description='Not a JSON')

    data = storage.get("State", state_id)
    if not data:
        abort(404)

    for key, value in data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(data, key, value)

    data.save()
    return jsonify(data.to_dict())
