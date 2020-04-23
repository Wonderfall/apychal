from achallonge import api
import asyncio


async def index(tournament, **params):
    """Retrieve a tournament's match list."""
    return await api.fetch_and_parse(
        "GET",
        f"tournaments/{tournament}/matches",
        **params)


async def show(tournament, match_id, **params):
    """Retrieve a single match record for a tournament."""
    return await api.fetch_and_parse(
        "GET",
        f"tournaments/{tournament}/matches/{match_id}",
        **params)


async def update(tournament, match_id, **params):
    """Update/submit the score(s) for a match."""
    await api.fetch(
        "PUT",
        f"tournaments/{tournament}/matches/{match_id}",
        "match",
        **params)


async def reopen(tournament, match_id):
    """Reopens a match that was marked completed, automatically resetting matches that follow it."""
    await api.fetch(
        "POST",
        f"tournaments/{tournament}/matches/{match_id}/reopen")


async def mark_as_underway(tournament, match_id):
    """Sets "underway_at" to the current time and highlights the match in the bracket"""
    await api.fetch(
        "POST",
        f"tournaments/{tournament}/matches/{match_id}/mark_as_underway")


async def unmark_as_underway(tournament, match_id):
    """Clears "underway_at" and unhighlights the match in the bracket"""
    await api.fetch(
        "POST",
        f"tournaments/{tournament}/matches/{match_id}/unmark_as_underway")
