This is the async version of [pychal](https://github.com/ZEDGR/pychal).

Please note that it :
- Only supports **Python 3.6+** (modern `asyncio`, removed legacy code).
- Replaces `requests` with `aiohttp` (which makes this module asynchronous).

That's it for the main differences, otherwise it should be the same to use as the original.

*Why don't you submit this as a PR?* I don't trust my tech skills to be honest, what I did here was very simple. However it breaks compatibility with older versions of Python, which can be an issue. If you're going to use an async version of `pychal`, I think you're already aware of the reason why.