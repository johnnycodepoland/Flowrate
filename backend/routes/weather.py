from backend.services.weather import get_weather
from fastapi import APIRouter

router = APIRouter()

@router.get("/weather")
async def get_actual_weather(lat: float, lon: float):
    weather = await get_weather(lat, lon)

    return {"weather": weather}
