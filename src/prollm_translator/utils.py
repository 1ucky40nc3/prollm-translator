import datetime


def timestamp() -> str:
    """Return a current timestamp."""
    return datetime.datetime.now().strftime("%Y%m%d%H%M%S")
