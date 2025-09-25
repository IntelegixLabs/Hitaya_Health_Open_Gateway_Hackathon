import functools
import json

from flask import Response, jsonify, request
from flask_api import status


def response(model):
    """Create a response with given model."""

    def decorator(func):
        """Decorator

        :param func: Decorated endpoint function
        :type func: :func:
        """

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            code = status.HTTP_200_OK
            object_ = func(*args, **kwargs)

            if isinstance(object_, tuple):
                object_, code = object_

            # If object_ is a :class:'Response' then return it
            if isinstance(object_, Response):
                return object_, code
            if isinstance(object_, dict):
                obj_ = model(**object_)
                return obj_.model_dump(mode="json", by_alias=True), code
            data: list = []
            for document in object_:
                obj_ = model(**document)
                data.append(obj_.model_dump(mode="json", by_alias=True))
            return jsonify(data), code

        return wrapper

    return decorator


def document_filter(collection):
    if filters := request.headers.get("x-filter"):
        return collection.find(json.loads(filters))
    return collection.find()


class Message:
    Success = "Success"
    NotFound = "Doesn't Exists"
    Found = "Already Exists"
