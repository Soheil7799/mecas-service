from fastapi import FastAPI
import api.api as api
# Declaring endpoints
app = FastAPI()
app.include_router(api.api_router)






