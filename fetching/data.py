import requests
from urllib.parse import quote

pinkAlerts = [
    "Tornado Warning",
    "Tornado Emergency"
]
def masterFetch(whatToFetch: str, stateCodes: list, extreme: bool, severe: bool, moderate: bool):
    
    url = ""
    if whatToFetch == "all":
        url = "https://api.weather.gov/alerts/active"
    elif whatToFetch == "tornado":
        events = ["Tornado Warning", "Tornado Watch", "Tornado Emergency"]
        usableEvents = ",".join(quote(event) for event in events)
        url = f"https://api.weather.gov/alerts/active?event={usableEvents}"
    elif whatToFetch == "storm/flood":
        events = ["Severe Thunderstorm Warning", "Flash Flood Warning", "Flash Flood Emergency", "Flood Warning"]
        usableEvents = ",".join(quote(event) for event in events)
        url = f"https://api.weather.gov/alerts/active?event={usableEvents}"
    elif whatToFetch == "state":
        usableStates = ",".join(quote(stateCode) for stateCode in stateCodes)
        url = f"https://api.weather.gov/alerts/active?area={usableStates}"
        
    
    headers = {
        "User-Agent": "HackclubUsingWXTUI",
        "Accept": "application/geo+json"
    }
    response = requests.get(url, headers=headers)
    data = response.json()
    alerts = data["features"]

    rawproduct = {}

    for alert in alerts:
        prop = alert["properties"]
        if prop["event"] == "Test Message":
            continue
        if prop["severity"] == "Unknown" or prop["severity"] == "Minor":
            continue
        if prop["severity"] == "Extreme" and not extreme:
            continue
        if prop["severity"] == "Severe" and not severe:
            continue
        if prop["severity"] == "Moderate" and not moderate:
            continue
        if prop["severity"] == "Moderate":
            color = "yellow"
        elif prop["severity"] == "Severe":
            color = "orange"
        elif prop["severity"] == "Extreme":
            color = "red"
        if prop["event"] == "Tornado Warning":
            color = "pink"
        rawproduct[prop["onset"]] = {
            "headline": ", ".join({prop["headline"]}),
            "event": ", ".join({prop["event"]}),
            "severity": ", ".join({prop["severity"]}),
            "onset": ", ".join({prop["onset"]}),
            "expires": ", ".join({prop["expires"]}),
            "areas": ", ".join({prop["areaDesc"]}),
            "sender": ", ".join({prop["senderName"]}),
            "id": ", ".join({prop["id"]}),
            "color": color
            }
    product = dict(sorted(rawproduct.items(), key=lambda x: x[0], reverse=True))
    return product


def idFetch(id):
    url = f"https://api.weather.gov/alerts/{id}"

    headers = {
        "User-Agent": "HackclubUsingWXTUI",
        "Accept": "application/geo+json"
    }
    response = requests.get(url, headers=headers)
    data = response.json()

    product = []

    prop = data["properties"]
    product.append(prop["senderName"])
    product.append(prop["headline"])
    product.append(prop["description"])
    product.append(prop["instruction"])

    return product