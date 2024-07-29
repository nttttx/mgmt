import logging

log = logging.getLogger(__name__)

_HUMAN_TIME_REPR_MAP = {
    "s": 1,
    "m": 60,
    "h": 3600,
    "d": 86400,
    "w": 604800,
    "M": 2629800,
    "y": 31557600
}


def convert_human_time_string(human_time_repr: list[str]) -> int:
    time_delta = 0
    for time_string in human_time_repr:
        # Hacky trick:
        #   mapping human's input 
        #   with _HUMAN_TIME_REPR_MAP variable
        seconds = _HUMAN_TIME_REPR_MAP[time_string[-1]] * int(time_string[:-1])
        log.debug("%s -> %s" % (time_string, seconds))
        time_delta += seconds
    return time_delta
