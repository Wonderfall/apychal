from achallonge import api
import asyncio


async def index(tournament):
    """Retrieve a tournament's participant list."""
    return await api.fetch_and_parse(
        "GET",
        f"tournaments/{tournament}/participants")


async def create(tournament, name, **params):
    """Add a participant to a tournament."""
    params.update({"name": name})

    return await api.fetch_and_parse(
        "POST",
        f"tournaments/{tournament}/participants",
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
        f"tournaments/{tournament}/participants/bulk_add",
        "participants[]",
        **params)


async def show(tournament, participant_id, **params):
    """Retrieve a single participant record for a tournament."""
    return await api.fetch_and_parse(
        "GET",
        f"tournaments/{tournament}/participants/{participant_id}",
        **params)


async def update(tournament, participant_id, **params):
    """Update the attributes of a tournament participant."""
    await api.fetch(
        "PUT",
        f"tournaments/{tournament}/participants/{participant_id}",
        "participant",
        **params)


async def check_in(tournament, participant_id):
    """Checks a participant in."""
    await api.fetch(
        "POST",
        f"tournaments/{tournament}/participants/{participant_id}/check_in")


async def undo_check_in(tournament, participant_id):
    """Marks a participant as having not checked in."""
    await api.fetch(
        "POST",
        f"tournaments/{tournament}/participants/{participant_id}/undo_check_in")


async def destroy(tournament, participant_id):
    """Destroys or deactivates a participant.

    If tournament has not started, delete a participant, automatically
    filling in the abandoned seed number.

    If tournament is underway, mark a participant inactive, automatically
    forfeiting his/her remaining matches.

    """
    await api.fetch(
        "DELETE",
        f"tournaments/{tournament}/participants/{participant_id}")


async def clear(tournament):
    """Deletes all participants in a tournament.
    (Only allowed if tournament hasn't started yet)
    """
    await api.fetch(
        "DELETE",
        f"tournaments/{tournament}/participants/clear")


async def randomize(tournament):
    """Randomize seeds among participants.

    Only applicable before a tournament has started.

    """
    await api.fetch("POST", f"tournaments/{tournament}/participants/randomize")
