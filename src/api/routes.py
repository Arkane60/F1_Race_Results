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
    try:
        data = get_driver_standings(season)
        return JSONResponse(content=data)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

@router.get("/standings/constructors")
def constructor_standings(season: int = Query(...)):
    try:
        data = get_constructor_standings(season)
        return JSONResponse(content=data)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

@router.get("/races/points")
def points_progression(season: int = Query(...)):
    try:
        data = get_points_progression(season)
        return JSONResponse(content=data)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

@router.get("/stats/pilots")
def pilot_stats(season: int = Query(...)):
    try:
        data = get_pilot_stats(season)
        return JSONResponse(content=data)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)