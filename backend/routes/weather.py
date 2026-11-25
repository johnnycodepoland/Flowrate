from backend.services.weather import get_weather
from fastapi import APIRouter, Query

router = APIRouter()

@router.get("/weather")
async def get_actual_weather(lat: float = Query(ge=-90, le=90), lon: float = Query(ge=-180, le=180)):
    weather = await get_weather(lat, lon)

    return weather
