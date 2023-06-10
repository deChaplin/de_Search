import requests

def getBannedStatus(key, accountList):  # Gets the accounts status
    response = requests.request("GET", "http://api.steampowered.com/ISteamUser/GetPlayerBans/v1/?key=" + key + "&steamids=" + accountList,data="", params="")
    return response.text

def getAccountName(key, steamId):   # Gets the Account Summaries
    response = requests.request("GET", "http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key=" + key + "&steamids=" + steamId, data="",params="")
    return response.text