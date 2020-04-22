import json
import iso8601
import tzlocal
import pytz
import itertools
import sys
import aiohttp
import asyncio

PY2 = sys.version_info[0] == 2
TEXT_TYPE = unicode if PY2 else str
tz = tzlocal.get_localzone()

CHALLONGE_API_URL = "api.challonge.com/v1"

_credentials = {
    "user": None,
    "api_key": None,
}


class ChallongeException(Exception):
    pass


def set_credentials(username, api_key):
    """Set the challonge.com api credentials to use."""
    _credentials["user"] = username
    _credentials["api_key"] = api_key


def assert_or_raise(cond, exc, *args):
    if achallonge.USE_EXCEPTIONS is not None and not cond:
        if achallonge.USE_EXCEPTIONS:
            raise exc(*args)
        else:
            log.warning('An exception `{}` has been raised: `{}`'.format(exc.__name__, args))


def set_timezone(new_tz=None):
    """Set the timezone for datetime fields.
    By default is your machine's time.
    If it's called without parameter sets the
    local time again.

    :keyword param new_tz: timezone string
    ex. 'Europe/Athens',
        'Asia/Seoul',
        'America/Los_Angeles',
        'UTC'

    :return
        None
    """
    global tz
    if new_tz:
        tz = pytz.timezone(new_tz)
    else:
        tz = tzlocal.get_localzone()


def get_credentials():
    """Retrieve the challonge.com credentials set with set_credentials()."""
    return _credentials["user"], _credentials["api_key"]


def get_timezone():
    """Return currently timezone in use."""
    return tz


async def fetch(method, uri, params_prefix=None, loop=None, timeout=30, **params):
    """Fetch the given uri and return the contents of the response."""
    params = _prepare_params(params, params_prefix)

    if method == "POST" or method == "PUT":
        r_data = {"data": params}
    else:
        r_data = {"params": params}

    # build the HTTP request and use basic authentication
    url = "https://%s/%s.json" % (CHALLONGE_API_URL, uri)


    timeout = aiohttp.ClientTimeout(total=timeout)

    async with aiohttp.ClientSession(loop=loop, timeout=timeout) as session:
        credentials = get_credentials()
        auth = aiohttp.BasicAuth(login=credentials[0], password=credentials[1])
        async with session.request(method, url, params=params, auth=auth) as response:
            resp = await response.json()
            assert_or_raise(response.status in [200, 401, 404, 406, 422, 500], ValueError, 'Unknown API return code', resp, response.status, response.reason, uri, params)
            assert_or_raise(response.status not in [401, 404, 406, 422, 500], ChallongeException, resp, response.status, response.reason, uri, params)
            return resp

async def fetch_and_parse(method, uri, params_prefix=None, **params):
    """Fetch the given uri and return python dictionary with parsed data-types."""
    response = await fetch(method, uri, params_prefix, **params)
    return _parse(json.loads(response.text))


def _parse(data):
    """Recursively convert a json into python data types"""

    if not data:
        return []
    elif isinstance(data, (tuple, list)):
        return [_parse(subdata) for subdata in data]

    # extract the nested dict. ex. {"tournament": {"url": "7k1safq" ...}}
    d = {ik: v for k in data.keys() for ik, v in data[k].items()}

    # convert datetime strings to datetime objects
    # and float number strings to float
    to_parse = dict(d)
    for k, v in to_parse.items():
        if k in {
                "name",
                "display_name",
                "display_name_with_invitation_email_address",
                "username",
                "challonge_username"}:
            continue # do not test type of fields which are always strings
        if isinstance(v, TEXT_TYPE):
            try:
                dt = iso8601.parse_date(v)
                d[k] = dt.astimezone(tz)
            except iso8601.ParseError:
                try:
                    d[k] = float(v)
                except ValueError:
                    pass

    return d


def _prepare_params(dirty_params, prefix=None):
    """Prepares parameters to be sent to challonge.com.

    The `prefix` can be used to convert parameters with keys that
    look like ("name", "url", "tournament_type") into something like
    ("tournament[name]", "tournament[url]", "tournament[tournament_type]"),
    which is how challonge.com expects parameters describing specific
    objects.

    """
    if prefix and prefix.endswith('[]'):
        keys = []
        values = []
        for k, v in dirty_params.items():
            if isinstance(v, (tuple, list)):
                keys.append(k)
                values.append(v)
        firstiter = ((k, v) for vals in zip(*values) for k, v in zip(keys, vals))
        lastiter = ((k, v) for k, v in dirty_params.items() if k not in keys)
        dpiter = itertools.chain(firstiter, lastiter)
    else:
        dpiter = dirty_params.items()

    params = []
    for k, v in dpiter:
        if isinstance(v, (tuple, list)):
            for val in v:
                val = _prepare_value(val)
                if prefix:
                    params.append(("%s[%s][]" % (prefix, k), val))
                else:
                    params.append((k + "[]", val))
        else:
            v = _prepare_value(v)
            if prefix:
                params.append(("%s[%s]" % (prefix, k), v))
            else:
                params.append((k, v))

    return params


def _prepare_value(val):
    if hasattr(val, "isoformat"):
        val = val.isoformat()
    elif isinstance(val, bool):
        # challonge.com only accepts lowercase true/false
        val = str(val).lower()
    return val