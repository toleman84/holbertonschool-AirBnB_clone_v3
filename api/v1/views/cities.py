#!/usr/bin/python3
"""doc"""

from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage
from models.city import City


@app_views.route('/cities/<city_id>', strict_slashes=False, methods=['GET'])
def get_cities():
    """ retrieves a list of all City objects """
    cities = []
    for city in storage.all("City").values():
        cities.append(city.to_dict())
    return jsonify(cities)


@app_views.route('/states/<string:state_id>', methods=['GET'],
                 strict_slashes=False)
def get_city(city_id):
    """Retrieves a City object"""
    city = storage.get("City", city_id)
    if city is not None:
        return jsonify(city.to_dict())
    abort(404)


@app_views.route('/api/v1/cities/<city_id>', strict_slashes=False,
                 methods=['DELETE'])
def delete_city(city_id):
    """Deletes a City object."""
    city = storage.get('City', city_id)
    if city is not None:
        storage.delete(city)
        storage.save()
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
    city.save()

    return make_response(jsonify(city.to_dict()), 201)


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
