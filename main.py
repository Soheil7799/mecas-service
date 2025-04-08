from fastapi import FastAPI
from api import api
# Declaring endpoints
app = FastAPI()
app.include_router(api.api_router)






