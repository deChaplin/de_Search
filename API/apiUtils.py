import requests

def getBannedStatus(key, accountList):  # Gets the accounts status
    response = requests.request("GET", "http://api.steampowered.com/ISteamUser/GetPlayerBans/v1/?key=" + key + "&steamids=" + accountList,data="", params="")
    return response.text

def getAccountName(key, steamId):   # Gets the Account Summaries
    response = requests.request("GET", "http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key=" + key + "&steamids=" + steamId, data="",params="")
    return response.text

def getDict(word):
    response = requests.request("GET", f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}")
    return response.text


def getRexi(name, key):
    url = "https://search.rezi.one/indexes/rezi/search"

    payload = {
        "q": name,
        "limit": 10
    }
    headers = {
        "accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {key}"
    }

    response = requests.post(url, json=payload, headers=headers)

    return response.text