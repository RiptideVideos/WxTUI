import requests
from urllib.parse import quote

def fetchAlerts():
    headers = {
        "User-Agent": "HackclubUsingWXTUI",
        "Accept": "application/geo+json"
    }
    response = requests.get("https://api.weather.gov/alerts/active", headers=headers)
    data = response.json()
    alerts = data["features"]

    rawproduct = {}

    for alert in alerts:
        prop = alert["properties"]
        if prop["event"] == "Test Message":
            continue
        rawproduct[prop["onset"]] = {
            "headline": {prop["headline"]},
            "event": {prop["event"]},
            "severity": {prop["severity"]},
            "onset": {prop["onset"]},
            "expires": {prop["expires"]},
            "areas": {prop["areaDesc"]},
            "sender": {prop["senderName"]},
            "id": {prop["id"]}
        }
    product = dict(sorted(rawproduct.items()))
    return product

def fetchTornado():
    headers = {
        "User-Agent": "HackclubUsingWXTUI",
        "Accept": "application/geo+json"
    }

    events = ["Tornado Warning", "Tornado Watch"]

    usableEvents = ",".join(quote(event) for event in events)

    response = requests.get(f"https://api.weather.gov/alerts/active?event={usableEvents}", headers=headers)
    data = response.json()
    alerts = data["features"]

    rawproduct = {}

    for alert in alerts:
        prop = alert["properties"]
        if prop["event"] == "Test Message":
            continue
        rawproduct[prop["onset"]] = {
            "headline": {prop["headline"]},
            "event": {prop["event"]},
            "severity": {prop["severity"]},
            "onset": {prop["onset"]},
            "expires": {prop["expires"]},
            "areas": {prop["areaDesc"]},
            "sender": {prop["senderName"]},
            "id": {prop["id"]}
        }
    product = dict(sorted(rawproduct.items()))
    return product

def fetchTstorm():
    headers = {
        "User-Agent": "HackclubUsingWXTUI",
        "Accept": "application/geo+json"
    }

    events = ["Severe Thunderstrom Warning", "Flash Flood Warning"]

    usableEvents = ",".join(quote(event) for event in events)

    response = requests.get(f"https://api.weather.gov/alerts/active?event={usableEvents}", headers=headers)
    data = response.json()
    alerts = data["features"]

    rawproduct = {}

    for alert in alerts:
        prop = alert["properties"]
        if prop["event"] == "Test Message":
            continue
        rawproduct[prop["onset"]] = {
            "headline": {prop["headline"]},
            "event": {prop["event"]},
            "severity": {prop["severity"]},
            "onset": {prop["onset"]},
            "expires": {prop["expires"]},
            "areas": {prop["areaDesc"]},
            "sender": {prop["senderName"]},
            "id": {prop["id"]}
        }
    product = dict(sorted(rawproduct.items()))
    return product

def fetchState(stateCodes: list):
    headers = {
        "User-Agent": "HackclubUsingWXTUI",
        "Accept": "application/geo+json"
    }

    usableStates = ",".join(quote(state) for state in stateCodes)

    response = requests.get(f"https://api.weather.gov/alerts/active?area={usableStates}", headers=headers)
    data = response.json()
    alerts = data["features"]

    rawproduct = {}

    for alert in alerts:
        prop = alert["properties"]
        if prop["event"] == "Test Message":
            continue
        rawproduct[prop["onset"]] = {
            "headline": {prop["headline"]},
            "event": {prop["event"]},
            "severity": {prop["severity"]},
            "onset": {prop["onset"]},
            "expires": {prop["expires"]},
            "areas": {prop["areaDesc"]},
            "sender": {prop["senderName"]},
            "id": {prop["id"]}
        }
    product = dict(sorted(rawproduct.items()))
    return product