from functools import wraps
from django.http import HttpResponse
from django.db.models.query import ValuesQuerySet
import json

class GenericJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        try:
            return json.JSONEncoder.default(self, obj)
        except TypeError:
            return str(obj)

def json_response(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        obj = fn(*args, **kwargs)
        if isinstance(obj, ValuesQuerySet):
            obj = list(obj)

        return HttpResponse(json.dumps(obj,
                                       cls=GenericJsonEncoder),
                            content_type="application/json")
    return wrapper

