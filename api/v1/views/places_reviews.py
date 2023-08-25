#!/usr/bin/python3
""" api endpoints para ciudades """

from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage
from models.place import Place
from models.review import Review
from models.city import City


@app_views.route('/places/<string:place_id>/reviews', strict_slashes=False,
                 methods=['GET'])
def get_reviews(place_id):
    """ retrieves a list of all review objects in a place """

    reviews = []
    place = storage.get("Place", pĺace_id)
    if place is None:
        abort(404)
    for review in place.reviews:
        reviews.append(review.to_dict())
    return jsonify(reviews)


@app_views.route('/reviews/<string:review_id>', methods=['GET'],
                 strict_slashes=False)
def get_review(city_id):
    """ info de una review segun la id """

    review = storage.get("Review", review_id)
    if review is not None:
        return jsonify(review.to_dict())
    abort(404)


@app_views.route('/reviews/<string:review_id>', strict_slashes=False,
                 methods=['DELETE'])
def review_city(review_id):
    """ Deletes a review object. """

    review = storage.get('Review', review_id)
    if review is not None:
        storage.delete(review)
        storage.save()
        return jsonify({})
    abort(404)


@app_views.route('/places/<string:place_id>/reviews',
                 strict_slashes=False,
                 methods=['POST'])
def create_review(place_id):
    """ Creates a new review object. """

    new_review = request.get_json()
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    if 'user_id' not in new_review:
        abort(400, description='Missing user_id')
    user = storage.get("User", new_review['user_id'])
    if user is None:
        abort(404)
    if 'text' not in new_review:
        abort(400, description='Missing text')

    review = Review(**rew_review)
    return make_response(jsonify(review.to_dict()), 201)


@app_views.route('/cities/<string:review_id>', strict_slashes=False,
                 methods=['PUT'])
def update_review(review_id):
    """Updates a review  object."""

    new_review = request.get_json()
    if not new_review:
        abort(400, description='Not a JSON')
    current_review = storage.get("Review", review_id)
    if not current_review:
        abort(404)
    for key, value in new_review.items():
        if key not in ['user_id', 'id', 'created_at', 'updated_at']:
            setattr(current_review, key, value)

    current_review.save()
    return jsonify(current_review.to_dict()), 200
