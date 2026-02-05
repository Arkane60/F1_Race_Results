import requests

BASE_URL = "https://api.jolpi.ca/ergast/f1"

def fetch_jolpica_json(path: str):
    url = f"{BASE_URL}/{path}"
    resp = requests.get(url, headers={"User-Agent": "f1-race-results-app"})
    resp.raise_for_status()
    return resp.json()

def get_driver_standings(season: int):
    return fetch_jolpica_json(f"{season}/driverStandings.json")

def get_constructor_standings(season: int):
    return fetch_jolpica_json(f"{season}/constructorStandings.json")

def get_race_results(season: int):
    return fetch_jolpica_json(f"{season}/results.json?limit=1000")

def get_points_progression(season: int):
    return get_race_results(season)

def get_pilot_stats(season: int):
    data = get_race_results(season)
    stats = {}
    for race in data["MRData"]["RaceTable"]["Races"]:
        for res in race.get("Results", []):
            driver = f"{res['Driver']['givenName']} {res['Driver']['familyName']}"
            stats.setdefault(driver, {"wins": 0, "podiums": 0, "retirements": 0})
            pos = int(res['position']) if res.get('position') and res['position'].isdigit() else None
            status = res.get("status", "")
            if pos == 1: stats[driver]["wins"] += 1
            if pos and pos <= 3: stats[driver]["podiums"] += 1
            if "Retired" in status or "Accident" in status: stats[driver]["retirements"] += 1
    return stats