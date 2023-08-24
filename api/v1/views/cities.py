#!/usr/bin/python3
"""doc"""

from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage
<<<<<<< HEAD
from models.state import State
from models.city import City


@app_views.route('/states/<string:state_id>/cities', strict_slashes=False,
                 methods=['GET'])
def get_cities(state_id):
    """ retrieves a list of all city objects in a state """

    cities = []
    state = storage.get("State", state_id)
    if state is None:
        abort(404)
    for city in state.cities:
=======
from models.city import City


@app_views.route('/api/v1/states/<state_id>/cities', strict_slashes=False, methods=['GET'])
def get_cities(state_id):
    """ retrieves a list of all City objects """
    state = storage.get("State", state_id)
    if state is None:
        abort(404)
    cities = []
    for city in storage.all("City").values():
>>>>>>> b3e72e10a5c08a9c57c0000f8eb03339dc483856
        cities.append(city.to_dict())
    return jsonify(cities)


<<<<<<< HEAD
@app_views.route('/api/v1/cities/<city_id>', methods=['GET'],
=======
<<<<<<< HEAD
@app_views.route('/cities/string:city_id', methods=['GET'],
                 strict_slashes=False)
def get_city(city_id):
    """ info de una ciudad segun la id """
=======
@app_views.route('/states/<string:state_id>', methods=['GET'],
>>>>>>> 77790b855c98c3d3cb2afd9ef87c602ed076a4a8
                 strict_slashes=False)
def get_city(city_id):
    """Retrieves a City object"""
>>>>>>> b3e72e10a5c08a9c57c0000f8eb03339dc483856
    city = storage.get("City", city_id)
    if city is not None:
        return jsonify(city.to_dict())
    abort(404)


<<<<<<< HEAD
@app_views.route('/cities/<string:city_id>', strict_slashes=False,
                 methods=['DELETE'])
def delete_city(city_id):
    """Deletes a City object."""

=======
@app_views.route('/api/v1/cities/<city_id>', strict_slashes=False,
                 methods=['DELETE'])
def delete_city(city_id):
    """Deletes a City object."""
>>>>>>> b3e72e10a5c08a9c57c0000f8eb03339dc483856
    city = storage.get('City', city_id)
    if city is not None:
        storage.delete(city)
        storage.save()
<<<<<<< HEAD
        return jsonify({})
    abort(404)


@app_views.route('/states/<string:state_id>/cities',
                 strict_slashes=False,
                 methods=['POST'])
def create_city(state_id):
    """Creates a new city object."""

    state = storage.get("State", state_id)
    if state is None:
        abort(404)
    new_city = request.get_json()
    if not new_city:
        abort(400, description='Not a JSON')
    if 'name' not in new_city.keys():
        abort(400, description='Missing name')
    new_city['state_id'] = state_id
    city = City(**new_city)
=======
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route('/api/v1/states/<state_id>/cities',
                 strict_slashes=False, methods=['POST'])
def create_cities(state_id):
    """Creates a new City object."""
    state = storage.get("State", state_id)
    if state is None:
        abort(404)

    data = request.get_json()
    if not data:
        abort(400, description='Not a JSON')

    if 'name' not in data.keys():
        abort(400, description='Missing name')

    city = City(**data)
>>>>>>> b3e72e10a5c08a9c57c0000f8eb03339dc483856
    city.save()

    return make_response(jsonify(city.to_dict()), 201)


<<<<<<< HEAD
@app_views.route('/cities/<string:city_id>', strict_slashes=False,
                 methods=['PUT'])
def update_city(city_id):
    """Updates a State object."""

    city = request.get_json()
    if not city:
        abort(400, description='Not a JSON')
    current_city = storage.get("City", city_id)
    if not current_city:
        abort(404)
    for key, value in city.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(current_city, key, value)

    current_city.save()
    return jsonify(current_city.to_dict()), 200
=======
@app_views.route('/api/v1/cities/<city_id>', strict_slashes=False,
                 methods=['PUT'])
def update_city(city_id):
    """Updates a City object."""
    city = request.get_json()
    if not city:
        abort(400, description='Not a JSON')

    data = storage.get("City", city_id)
    if not data:
        abort(404)

    for key, value in data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(data, key, value)

    data.save()
    return jsonify(data.to_dict()), 200
>>>>>>> b3e72e10a5c08a9c57c0000f8eb03339dc483856
