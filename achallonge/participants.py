from achallonge import api
import asyncio


async def index(tournament):
    """Retrieve a tournament's participant list."""
    return await api.fetch_and_parse(
        "GET",
        "tournaments/%s/participants" % tournament)


async def create(tournament, name, **params):
    """Add a participant to a tournament."""
    params.update({"name": name})

    return await api.fetch_and_parse(
        "POST",
        "tournaments/%s/participants" % tournament,
        "participant",
        **params)


async def bulk_add(tournament, names, **params):
    """Bulk add participants to a tournament (up until it is started).

    :param tournament: the tournament's name or id
    :param names: the names of the participants
    :type tournament: int or string
    :type names: list or tuple
    :return: each participants info
    :rtype: a list of dictionaries

    """
    params.update({"name": names})

    return await api.fetch_and_parse(
        "POST",
        "tournaments/%s/participants/bulk_add" % tournament,
        "participants[]",
        **params)


async def show(tournament, participant_id, **params):
    """Retrieve a single participant record for a tournament."""
    return await api.fetch_and_parse(
        "GET",
        "tournaments/%s/participants/%s" % (tournament, participant_id),
        **params)


async def update(tournament, participant_id, **params):
    """Update the attributes of a tournament participant."""
    await api.fetch(
        "PUT",
        "tournaments/%s/participants/%s" % (tournament, participant_id),
        "participant",
        **params)


async def check_in(tournament, participant_id):
    """Checks a participant in."""
    await api.fetch(
        "POST",
        "tournaments/%s/participants/%s/check_in" % (tournament, participant_id))


async def undo_check_in(tournament, participant_id):
    """Marks a participant as having not checked in."""
    await api.fetch(
        "POST",
        "tournaments/%s/participants/%s/undo_check_in" % (tournament, participant_id))


async def destroy(tournament, participant_id):
    """Destroys or deactivates a participant.

    If tournament has not started, delete a participant, automatically
    filling in the abandoned seed number.

    If tournament is underway, mark a participant inactive, automatically
    forfeiting his/her remaining matches.

    """
    await api.fetch(
        "DELETE",
        "tournaments/%s/participants/%s" % (tournament, participant_id))


async def randomize(tournament):
    """Randomize seeds among participants.

    Only applicable before a tournament has started.

    """
    await api.fetch("POST", "tournaments/%s/participants/randomize" % tournament)
