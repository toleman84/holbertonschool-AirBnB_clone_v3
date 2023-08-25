#!/usr/bin/python3
"""doc"""

from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage
from models.place import Place
from models.user import User
from models.city import City


@app_views.route('/cities/<string:city_id>/places', methods=['GET'],
                 strict_slashes=False)
def get_places(city_id):
    """ obtiene places dentro de una ciudad """

    places = []
    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    for place in city.places:
        places.append(place.to_dict())
    return jsonify(places)


@app_views.route('/places/<string:place_id>', methods=['GET'],
                 strict_slashes=False)
def get_place(place_id):
    """ information of a place according to the identification """

    place = storage.get("Place", place_id)
    if place is not None:
        return jsonify(place.to_dict())
    abort(404)


@app_views.route('/places/<string:place_id>', strict_slashes=False,
                 methods=['DELETE'])
def delete_place(place_id):
    """ Deletes a place object. """

    place = storage.get('Place', place_id)
    if place is not None:
        storage.delete(place)
        storage.save()
        return jsonify({})
    abort(404)


@app_views.route('/cities/<string:city_id>/places',
                 strict_slashes=False, methods=['POST'])
def create_place(city_id):
    """ Creates a new place object. """

    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    kwargs = request.get_json()
    if 'user_id' not in kwargs:
        return make_response(jsonify({'error': 'Missing user_id'}), 400)
    user = storage.get("User", kwargs['user_id'])
    if user is None:
        abort(404)
    if 'name' not in kwargs:
        return make_response(jsonify({'error': 'Missing name'}), 400)
    kwargs['city_id'] = city_id
    place = Place(**kwargs)
    place.save()
    return make_response(jsonify(place.to_dict()), 201)

@app_views.route('/places/<string:place_id>', strict_slashes=False,
                 methods=['PUT'])
def update_place(place_id):
    """ Updates a place object. """

    place = request.get_json()
    if not place:
        abort(400, description='Not a JSON')

    old_place = storage.get("Place", place_id)
    if not old_place:
        abort(404)

    for key, value in place.items():
        if key not in ['id', 'user_id', 'created_at', 'updated_at']:
            setattr(old_place, key, value)

    old_place.save()
    return jsonify(old_place.to_dict()), 200
