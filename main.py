from fastapi import FastAPI
from router.user import user_router
from config.models import init_db

app = FastAPI()

# Routers
app.include_router(user_router)

init_db()