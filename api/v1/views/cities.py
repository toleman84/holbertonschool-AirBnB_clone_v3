#!/usr/bin/python3
""" api endpoints para ciudades """

from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage
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
        cities.append(city.to_dict())
    return jsonify(cities)


@app_views.route('/cities/<string:city_id>', methods=['GET'],
                 strict_slashes=False)
def get_city(city_id):
    """ info de una ciudad segun la id """
    
    city = storage.get("City", city_id)
    if city is not None:
        return jsonify(city.to_dict())
    abort(404)


@app_views.route('/cities/<string:city_id>', strict_slashes=False,
                 methods=['DELETE'])
def delete_city(city_id):
    """Deletes a City object."""

    city = storage.get('City', city_id)
    if city is not None:
        storage.delete(city)
        storage.save()
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
    city.save()

    return make_response(jsonify(city.to_dict()), 201)


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
