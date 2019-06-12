from typing import Optional, Union

from fbs_runtime.application_context.PyQt5 import ApplicationContext

# This will be set when the application starts properly.
application_context: Optional[ApplicationContext] = None


def get_resource(resource: str) -> Union[bytes, str]:
    return application_context.get_resource(resource)
