import fastapi
from backend.routes.trainings import router
from backend.routes.weather import router as weather_router

app = fastapi.FastAPI()

app.include_router(router)
app.include_router(weather_router)