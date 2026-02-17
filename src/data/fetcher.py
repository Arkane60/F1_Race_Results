import requests
from functools import lru_cache

BASE_URL = "https://api.jolpi.ca/ergast/f1"

def fetch_jolpica_json(path: str):
    """
    Perform a GET request to the Jolpica F1 API.

    Args:
        path (str): API endpoint path (e.g., "2023/driverStandings.json").

    Returns:
        dict: Parsed JSON response from the API.

    Raises:
        requests.HTTPError: If the request fails or returns a non-200 status.
    """
    url = f"{BASE_URL}/{path}"
    resp = requests.get(url, headers={"User-Agent": "f1-race-results-app"})
    resp.raise_for_status()
    return resp.json()

@lru_cache(maxsize=10)
def get_driver_standings(season: int):
    """
    Retrieve full driver championship standings for a given F1 season.

    Handles API pagination automatically to ensure all standings
    are retrieved even if the API limits results per request.

    Results are cached (LRU cache, maxsize=10) to reduce API calls.

    Args:
        season (int): F1 season year (e.g., 2023).

    Returns:
        list[dict]: List of driver standings including:
            - Driver information
            - Position
            - Points
            - Wins
    """
    all_standings = []
    limit = 100
    offset = 0

    while True:
        data = fetch_jolpica_json(
            f"{season}/driverStandings.json?limit={limit}&offset={offset}"
        )

        lists = data.get("MRData", {}).get("StandingsTable", {}).get("StandingsLists", [])
        if not lists:
            break

        standings_chunk = lists[0].get("DriverStandings", [])
        if not standings_chunk:
            break

        all_standings.extend(standings_chunk)

        total = int(data.get("MRData", {}).get("total", 0))
        offset += limit

        if offset >= total:
            break

    return all_standings

@lru_cache(maxsize=10)
def get_constructor_standings(season: int):
    """
    Retrieve full constructor championship standings for a given F1 season.

    Handles API pagination automatically.
    Results are cached to optimize performance and reduce external API calls.

    Args:
        season (int): F1 season year (e.g., 2023).

    Returns:
        list[dict]: List of constructor standings including:
            - Constructor name
            - Position
            - Points
            - Wins
    """
    all_standings = []
    limit = 100
    offset = 0

    while True:
        data = fetch_jolpica_json(
            f"{season}/constructorStandings.json?limit={limit}&offset={offset}"
        )

        lists = data.get("MRData", {}).get("StandingsTable", {}).get("StandingsLists", [])
        if not lists:
            break

        standings_chunk = lists[0].get("ConstructorStandings", [])
        if not standings_chunk:
            break

        all_standings.extend(standings_chunk)

        total = int(data.get("MRData", {}).get("total", 0))
        offset += limit

        if offset >= total:
            break

    return all_standings

@lru_cache(maxsize=10)
def get_all_season_results(season: int):
    """
    Retrieve all race results for a given F1 season.

    Automatically handles pagination to fetch all races
    and their complete results.

    Cached to prevent repeated heavy API calls.

    Args:
        season (int): F1 season year.

    Returns:
        list[dict]: List of race objects including:
            - Race metadata (name, round, date)
            - Full results per driver
    """
    all_races = []
    limit = 100
    offset = 0

    while True:
        data = fetch_jolpica_json(
            f"{season}/results.json?limit={limit}&offset={offset}"
        )

        race_chunk = data.get("MRData", {}).get("RaceTable", {}).get("Races", [])
        if not race_chunk:
            break

        all_races.extend(race_chunk)

        total = int(data.get("MRData", {}).get("total", 0))
        offset += limit

        if offset >= total:
            break

    return all_races

@lru_cache(maxsize=10)
def get_points_progression(season: int):
    """
    Compute cumulative points progression for all drivers
    across a full F1 season.

    Points are accumulated race after race to allow
    championship evolution visualization.

    Cached to improve performance.

    Args:
        season (int): F1 season year.

    Returns:
        dict[str, dict[str, float]]:
            {
                "1 - Bahrain Grand Prix": {
                    "Driver Name": cumulative_points,
                    ...
                },
                ...
            }
    """
    races = get_all_season_results(season)

    cumulative_points = {}
    points_progression = {}

    for race in races:
        round_number = race.get("round")
        race_name = f"{round_number} - {race.get('raceName', 'Unknown')}"
        results = race.get("Results", [])

        points_progression[race_name] = {}

        for res in results:
            driver_data = res.get("Driver", {})
            driver = f"{driver_data.get('givenName','')} {driver_data.get('familyName','')}".strip()
            if not driver:
                continue

            points = float(res.get("points", 0))
            cumulative_points[driver] = cumulative_points.get(driver, 0) + points
            points_progression[race_name][driver] = cumulative_points[driver]

    return points_progression


@lru_cache(maxsize=10)
def get_pilot_stats(season: int):
    """
    Compute season statistics for each driver.

    Statistics include:
        - Total wins (P1 finishes)
        - Total podiums (Top 3 finishes)
        - Total retirements (DNF, accidents, mechanical failures)

    Retirement detection is based on position text and status keywords.

    Cached to optimize performance.

    Args:
        season (int): F1 season year.

    Returns:
        dict[str, dict[str, int]]:
            {
                "Driver Name": {
                    "wins": int,
                    "podiums": int,
                    "retirements": int
                }
            }
    """
    races = get_all_season_results(season)
    stats = {}

    for race in races:
        results = race.get("Results", [])

        for res in results:
            driver_data = res.get("Driver", {})
            driver = f"{driver_data.get('givenName','')} {driver_data.get('familyName','')}".strip()
            if not driver:
                continue

            stats.setdefault(driver, {"wins": 0, "podiums": 0, "retirements": 0})

            pos = res.get("position")
            if pos and str(pos).isdigit():
                pos = int(pos)
            else:
                pos = None

            if pos == 1:
                stats[driver]["wins"] += 1
            if pos and pos <= 3:
                stats[driver]["podiums"] += 1

            status = res.get("status", "")
            position_text = res.get("positionText", "")
            if position_text == "R" or any(
                s in status for s in ["Retired", "Accident", "DNF", "Collision", "Engine", "Gearbox"]
            ):
                stats[driver]["retirements"] += 1

    return stats