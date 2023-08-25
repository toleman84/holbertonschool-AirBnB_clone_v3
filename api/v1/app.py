#!/usr/bin/python3
"""doc"""

from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views
import os


app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown(error):
    """ al cerrar el programa cerrar el storage """
    storage.close()


@app.errorhandler(404)
def handle_404(error):
    """Handle 404 errors"""
    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":
    host = os.environ.get("HBNB_API_HOST", "0.0.0.0")
    port = os.environ.get("HBNB_API_PORT", 5000)
    app.run(host=host, port=port, threaded=True)
