import fastapi
from backend.routes.trainings import router
from backend.routes.weather import router as weather_router
from backend.routes.personal_bests import router as personal_bests_router

app = fastapi.FastAPI()

app.include_router(router)
app.include_router(weather_router)
app.include_router(personal_bests_router)