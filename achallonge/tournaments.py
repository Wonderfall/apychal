from achallonge import api
import asyncio


async def index(**params):
    """Retrieve a set of tournaments created with your account."""
    return await api.fetch_and_parse("GET", "tournaments", **params)


async def create(name, url, tournament_type="single elimination", **params):
    """Create a new tournament."""
    params.update({
        "name": name,
        "url": url,
        "tournament_type": tournament_type,
    })

    return await api.fetch_and_parse("POST", "tournaments", "tournament", **params)


async def show(tournament, **params):
    """Retrieve a single tournament record created with your account."""
    return await api.fetch_and_parse("GET", f"tournaments/{tournament}", **params)


async def update(tournament, **params):
    """Update a tournament's attributes."""
    await api.fetch("PUT", f"tournaments/{tournament}", "tournament", **params)


async def destroy(tournament):
    """Deletes a tournament along with all its associated records.

    There is no undo, so use with care!

    """
    await api.fetch("DELETE", f"tournaments/{tournament}")


async def process_check_ins(tournament, **params):
    """This should be invoked after a tournament's
    check-in window closes before the tournament is started.

    1) Marks participants who have not checked in as inactive.
    2) Moves inactive participants to bottom seeds (ordered by original seed).
    3) Transitions the tournament state from 'checking_in' to 'checked_in'

    """
    return await api.fetch_and_parse(
        "POST",
        f"tournaments/{tournament}/process_check_ins",
        **params)


async def abort_check_in(tournament, **params):
    """When your tournament is in a 'checking_in' or 'checked_in' state,
    there's no way to edit the tournament's start time (start_at)
    or check-in duration (check_in_duration).
    You must first abort check-in, then you may edit those attributes.

    1) Makes all participants active and clears their checked_in_at times.
    2) Transitions the tournament state from 'checking_in' or 'checked_in' to 'pending'

    """
    return await api.fetch_and_parse(
        "POST",
        f"tournaments/{tournament}/abort_check_in" ,
        **params)


async def start(tournament, **params):
    """Start a tournament, opening up matches for score reporting.

    The tournament must have at least 2 participants.

    """
    return await api.fetch_and_parse(
        "POST",
        f"tournaments/{tournament}/start",
        **params)


async def finalize(tournament, **params):
    """Finalize a tournament that has had all match scores submitted,
    rendering its results permanent.

    """
    return await api.fetch_and_parse(
        "POST",
        f"tournaments/{tournament}/finalize",
        **params)


async def reset(tournament, **params):
    """Reset a tournament, clearing all of its scores and attachments.

    You can then add/remove/edit participants before starting the
    tournament again.

    """
    return await api.fetch_and_parse(
        "POST",
        f"tournaments/{tournament}/reset",
        **params)
