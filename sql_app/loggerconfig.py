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
    event_dict["filename"] = currentframe().f_back.f_back.f_back.f_back.f_globals["__name__"]

    # this is stupid as fuck but works in at least this specific case
    event_dict["line_auto"] = currentframe().f_back.f_back.f_back.f_back.f_lineno 
    return event_dict

# this looks like what's prefered by sumologic
def rename_event_to_message(_, __, event_dict):
    event_dict["message"] = event_dict.pop("event")
    return event_dict

#logging.basicConfig(format="%(message)s")
structlog.configure(processors=[
    add_standard_fields,
    rename_event_to_message,
    structlog.processors.JSONRenderer()])


