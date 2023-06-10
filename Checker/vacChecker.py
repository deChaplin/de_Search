import json
from collections import namedtuple

import Checker.database as database
import Checker.apiUtils as api


def start_up():
    database.create_database()


def check_vac(KEY, account, discord_id):
    steamID, name, game_banned, game_bans, vac_banned, vac_bans, last_ban = \
        format_api_response(KEY, account, api.getBannedStatus(KEY, account))

    # Add the account to the database
    database.add_account(steamID, name, game_banned, game_bans, vac_banned, vac_bans, discord_id)

    return steamID, name, game_banned, game_bans, vac_banned, vac_bans, last_ban


def get_discord_id():
    # Returns the number of discord IDs in the database
    discord_ids = database.get_discord_id_list()
    return discord_ids


def add_account(KEY, account, discord_id):
    steamID, name, game_banned, game_bans, vac_banned, vac_bans, last_ban = \
        format_api_response(KEY, account, api.getBannedStatus(KEY, account))

    database.add_account(steamID, name, game_banned, game_bans, vac_banned, vac_bans, discord_id)
    return name


def format_api_response(KEY, account, response):
    accountStatus = json.loads(response, object_hook=lambda d: namedtuple('X', d.keys())(
        *d.values()))  # Loads json for the account status

    for i in accountStatus.players:
        # Calls the function to get the account name passing through the current steamID
        nameResponse = api.getAccountName(KEY, account)
        accountData = json.loads(nameResponse, object_hook=lambda d: namedtuple('X', d.keys())(
            *d.values()))  # Loads the json for the account summaries

        # Checks if the steamIDs match and returns a name
        for x in accountData.response.players:
            if x.steamid == i.SteamId:
                name = x.personaname

        # Changes variables if the account is game banned
        if i.NumberOfGameBans > 0:
            game_banned = "Yes"
        else:
            game_banned = "No"

        # Changes variables if the account is VAC banned
        if i.VACBanned:
            vac_banned = "Yes"
        else:
            vac_banned = "No"

        return i.SteamId, name, game_banned, str(i.NumberOfGameBans), vac_banned, \
            str(i.NumberOfVACBans), str(i.DaysSinceLastBan)


def remove_account(steam_id, discord_id):
    if str(discord_id) == str(database.get_discord_id(steam_id)):
        database.remove_account(steam_id)
        return True
    else:
        return False


# Get the steamID from the database
def get_steam_id(discord_id):
    steam_id = database.get_steamid_from_discord(discord_id)
    return steam_id