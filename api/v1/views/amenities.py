#!/usr/bin/python3
""" endpoints for amenities """

from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', strict_slashes=False,
                 methods=['GET'])
def get_amenities():
    """ retrieves a list of all  amenities """

    amenities = []
    for amenity in storage.all("Amenity").values():
        amenities.append(amenity.to_dict())
    return jsonify(amenities)


@app_views.route('/amenities/<string:amenity_id>', methods=['GET'],
                 strict_slashes=False)
def get_amenity(amenity_id):
    """ information of an amenity according to the id """

    amenity = storage.get("Amenity", amenity_id)
    if amenity is not None:
        return jsonify(amenity.to_dict())
    abort(404)


@app_views.route('/amenities/<string:amenity_id>', strict_slashes=False,
                 methods=['DELETE'])
def delete_amenity(amenity_id):
    """ Deletes an amenity object. """

    amenity = storage.get('Amenity', amenity_id)
    if amenity is not None:
        storage.delete(amenity)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route('/amenities', strict_slashes=False, methods=['POST'])
def create_amenity():
    """Creates a new amenity object."""

    new_amenity = request.get_json()

    if not new_amenity:
        abort(400, description='Not a JSON')

    if 'name' not in new_amenity.keys():
        abort(400, description='Missing name')

    amenity = Amenity(**new_amenity)
    amenity.save()

    return make_response(jsonify(amenity.to_dict()), 201)


@app_views.route('/amenities/<string:amenity_id>', strict_slashes=False,
                 methods=['PUT'])
def update_amenity(amenity_id):
    """ Updates an amenity object. """

    amenity = request.get_json()
    if not amenity:
        abort(400, description='Not a JSON')
    amenity_in_storage = storage.get("Amenity", amenity_id)
    if not amenity_in_storage:
        abort(404)
    for key, value in amenity.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(amenity_in_storage, key, value)
    amenity_in_storage.save()
    return jsonify(data.to_dict()), 200
