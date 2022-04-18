import structlog
import logging
import time
from inspect import currentframe

#fuck yes
def get_linenumber():
    cf = currentframe()
    return cf.f_back.f_lineno

def add_standard_fields(_, __, event_dict):
    event_dict["timestamp"] = int(time.time())
    event_dict["filename"] = currentframe().f_back.f_back.f_back.f_back.f_back.f_globals["__name__"]
    event_dict["line_auto"] = currentframe().f_back.f_back.f_back.f_back.f_back.f_lineno 
    return event_dict

# Going one level too deep with filename gets to "importlib._bootstrap"

# this looks like what's prefered by sumologic
def rename_event_to_message(_, __, event_dict):
    event_dict["message"] = event_dict.pop("event")
    event_dict["logger Name"] = dir(_)
    event_dict["Tracking cat"] = type(_.root)
    return event_dict

#logging.basicConfig(format="%(message)s")
structlog.configure(processors=[
        structlog.stdlib.add_log_level,
        structlog.processors.StackInfoRenderer(),
        add_standard_fields,
        rename_event_to_message,
        structlog.processors.JSONRenderer()
    ],
    wrapper_class=structlog.stdlib.BoundLogger,
    logger_factory=structlog.stdlib.LoggerFactory(),
    cache_logger_on_first_use=True,)

"""
log everythying as json
    find uvicorn logger option
add log level 
"""