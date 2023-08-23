#!/usr/bin/python3
"""doc"""

from flask import jsonify
from api.v1.views import app_views


@app_views.route('/status')
def status():
    """doc"""
    return jsonify({'status': 'OK'})
