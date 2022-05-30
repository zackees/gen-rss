"""
Date generating and parsing functionality. now_local() is better than datetime.now()
because now_local() generates a timezone aware datetime, which is REQUIRED for anything
date related.
"""

# pylint: disable=all
# flake8: noqa

from datetime import datetime
from typing import Optional, Union

import pytz
from dateutil.parser import parse



def iso_fmt(date_obj: Union[datetime, str]) -> str:
    if isinstance(date_obj, datetime):
        return date_obj.isoformat()
    elif isinstance(date_obj, str):
        return parse_datetime(date_obj).isoformat()
    else:
        raise ValueError(f"{__file__} Unexpected type: {type(date_obj)}")


def _my_date_parse(date_string: str) -> datetime:
    try:
        return datetime.fromisoformat(date_string)
    except ValueError as verr:
        if "Invalid isoformat" in str(verr):
            return parse(date_string, fuzzy=True)
        else:
            raise


def parse_datetime(s, tzinfo=None) -> datetime:  # type: ignore
    date: datetime = _my_date_parse(s)
    if tzinfo:
        if isinstance(tzinfo, str):
            tzinfo = pytz.timezone(tzinfo)
        if date.tzinfo is None:
            date = date.replace(tzinfo=tzinfo)
        else:
            date = date.astimezone(tzinfo)
    return date


def now_local(tz_str: str) -> datetime:
    """Returns timezone aware now, which allows subtractions"""
    ts = datetime.now()
    tz = pytz.timezone(tz_str)
    ts = ts.astimezone(tz)
    return ts
