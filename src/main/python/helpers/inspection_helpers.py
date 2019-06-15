import inspect


def has_method(obj, name):
    """ Returns true if the object has a method and false otherwise. """
    return callable(getattr(obj, name, None))
