#!/usr/bin/python3
"""doc"""

from models.state import State
from flask import abort, jsonify, request
from api.v1.views import app_views
from models import storage


@app_views.route('/api/v1/states', strict_slashes=False, methods=['GET'])
@app_views.route('/api/v1/states/<int:state_id>', strict_slashes=False,
                 methods=['GET'])
def get_states(state_id):
    """Retrieves the list of all State objects."""
    states = storage.all('State')
    stat = storage.all.get('State', state_id)

    if state_id is None:
        return jsonify([state.to_dict() for state in states.values()])
    elif stat is not None:
        return jsonify(stat.to_dict())
    else:
        abort(404)


@app_views.route('/api/v1/states/<int:state_id>', strict_slashes=False,
                 methods=['DELETE'])
def delete_state(state_id):
    """Deletes a State object."""
    stat = storage.all.get('State', state_id)
    if stat is not None:
        storage.delete(stat)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route('/api/v1/states', strict_slashes=False, methods=['POST'])
def create_state():
    """Creates a new State object."""
    data = request.get_json()

    if not data:
        abort(400, description='Not a JSON')

    if 'name' not in data:
        abort(400, description='Missing name')

    state = State(name=data['name'])
    state.save()

    return jsonify(state.to_dict()), 201


@app_views.route('/api/v1/states/<int:state_id>', strict_slashes=False,
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
        if key in ['id', 'created_at', 'updated_at']:
            continue
        setattr(state, key, value)

    state.save()
    return jsonify(state.to_dict()), 200
