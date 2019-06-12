from typing import Optional, Type, TypeVar, Union

from fbs_runtime.application_context.PyQt5 import ApplicationContext
from injector import Injector

# Will be populated when the application runs
injector: Optional[Injector] = None


T = TypeVar('T')


def get_service(interface: Type[T]) -> T:
    """ Resolve a service statically. This should only be used for very specific circumstances! """
    return injector.get(interface)


def get_resource(resource: str) -> Union[bytes, str]:
    """ Get a resource via the application context. This ensures it can be located whereever the app is installed. """
    application_context = get_service(ApplicationContext)
    return application_context.get_resource(resource)
