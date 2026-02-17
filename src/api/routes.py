from fastapi import APIRouter, Query
from fastapi.responses import JSONResponse
from src.data.fetcher import (
    get_driver_standings,
    get_constructor_standings,
    get_points_progression,
    get_pilot_stats
)

router = APIRouter()


@router.get("/standings/drivers")
def driver_standings(season: int = Query(...)):
    """
    Retrieve driver standings for a given Formula 1 season.

    This endpoint returns the official driver championship standings
    for the specified season, including driver information, position,
    and total points.

    Args:
        season (int): The F1 season year (e.g., 2023).

    Returns:
        JSONResponse:
            - 200: A list of driver standings.
            - 500: An error message if data retrieval fails.

    Example:
        GET /standings/drivers?season=2023
    """
    try:
        data = get_driver_standings(season)
        return JSONResponse(content=data)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)


@router.get("/standings/constructors")
def constructor_standings(season: int = Query(...)):
    """
    Retrieve constructor standings for a given Formula 1 season.

    This endpoint returns the official constructor championship standings
    for the specified season, including team name, position, and total points.

    Args:
        season (int): The F1 season year (e.g., 2023).

    Returns:
        JSONResponse:
            - 200: A list of constructor standings.
            - 500: An error message if data retrieval fails.

    Example:
        GET /standings/constructors?season=2023
    """
    try:
        data = get_constructor_standings(season)
        return JSONResponse(content=data)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)


@router.get("/races/points")
def points_progression(season: int = Query(...)):
    """
    Retrieve cumulative points progression for all drivers
    during a given Formula 1 season.

    The response contains race-by-race cumulative points,
    allowing visualization of championship evolution.

    Args:
        season (int): The F1 season year (e.g., 2023).

    Returns:
        JSONResponse:
            - 200: A dictionary mapping races to drivers' cumulative points.
            - 500: An error message if data retrieval fails.

    Example:
        GET /races/points?season=2023
    """
    try:
        data = get_points_progression(season)
        return JSONResponse(content=data)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)


@router.get("/stats/pilots")
def pilot_stats(season: int = Query(...)):
    """
    Retrieve detailed statistics for each driver in a given F1 season.

    Statistics include:
        - Number of wins
        - Number of podium finishes
        - Number of retirements

    Args:
        season (int): The F1 season year (e.g., 2023).

    Returns:
        JSONResponse:
            - 200: A dictionary containing driver statistics.
            - 500: An error message if data retrieval fails.

    Example:
        GET /stats/pilots?season=2023
    """
    try:
        data = get_pilot_stats(season)
        return JSONResponse(content=data)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)