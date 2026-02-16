import requests
from functools import lru_cache

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

def get_season_races(season: int):
    try:
        data = fetch_jolpica_json(f"{season}.json?limit=100")
        races = data.get("MRData", {}).get("RaceTable", {}).get("Races", [])
        return races or []
    except Exception:
        return []

@lru_cache(maxsize=10)
def get_points_progression(season: int):
    races = get_season_races(season)
    cumulative_points = {}
    points_progression = {}

    for race in races:
        round_number = race.get("round")
        race_name = f"{round_number} - {race.get('raceName', 'Unknown')}"
        if not round_number:
            continue

        try:
            race_results = fetch_jolpica_json(f"{season}/{round_number}/results.json")
            race_list = race_results.get("MRData", {}).get("RaceTable", {}).get("Races", [])
            if not race_list:
                continue
            results = race_list[0].get("Results", [])
        except Exception:
            continue

        points_progression[race_name] = {}
        for res in results:
            driver_data = res.get("Driver")
            if not driver_data:
                continue
            driver = f"{driver_data.get('givenName', '')} {driver_data.get('familyName', '')}".strip()
            if not driver:
                continue

            points = float(res.get("points", 0))
            cumulative_points[driver] = cumulative_points.get(driver, 0) + points
            points_progression[race_name][driver] = cumulative_points[driver]

    return points_progression

@lru_cache(maxsize=10)
def get_pilot_stats(season: int):
    races = get_season_races(season)
    stats = {}

    for race in races:
        round_number = race.get("round")
        if not round_number:
            continue

        try:
            race_results = fetch_jolpica_json(f"{season}/{round_number}/results.json")
            race_list = race_results.get("MRData", {}).get("RaceTable", {}).get("Races", [])
            if not race_list:
                continue
            results = race_list[0].get("Results", [])
        except Exception:
            continue

        for res in results:
            driver_data = res.get("Driver", {})
            given = driver_data.get("givenName", "")
            family = driver_data.get("familyName", "")
            if not given and not family:
                continue
            driver = f"{given} {family}".strip()
            stats.setdefault(driver, {"wins": 0, "podiums": 0, "retirements": 0})

            pos = None
            if res.get("position") and str(res["position"]).isdigit():
                pos = int(res["position"])

            if pos == 1:
                stats[driver]["wins"] += 1
            if pos and pos <= 3:
                stats[driver]["podiums"] += 1

            status = res.get("status", "")
            position_text = res.get("positionText", "")
            if position_text == "R" or any(s in status for s in ["Retired", "Accident", "DNF", "Collision", "Engine", "Gearbox"]):
                stats[driver]["retirements"] += 1

    return stats