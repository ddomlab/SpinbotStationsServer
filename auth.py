"""
Handles API key auth

To call a protected route, a client must send:
X-API-Key: <key>
"""

import os
from functools import wraps
from flask import request, abort
from dotenv import load_dotenv

load_dotenv()
HTTP_KEY = os.environ.get("HTTP_API_KEY")

if not HTTP_KEY:
    raise RuntimeError("HTTP_API_KEY is not set. Please set before continuing")

def require_http_api_key(route_function):
    @wraps(route_function)
    def wrapper(*args, **kwargs):
        sent_key = request.headers.get("X-API-Key")
        print(request.headers)

        if sent_key is None:
            abort(401, description="Missing X-API-Key header")

        if sent_key != HTTP_KEY:
            abort(401, description="Invalid HTTP API key")
        
        return route_function(*args, **kwargs)
    return wrapper