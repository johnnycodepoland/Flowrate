import fastapi
from backend.routes.trainings import router

app = fastapi.FastAPI()

app.include_router(router)