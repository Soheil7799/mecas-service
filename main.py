from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
import os
import api.api as api

app = FastAPI()

# Add CORS middleware with more specific origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For production, consider being more specific
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Declaring endpoints
app.include_router(api.api_router)

# Serve static assets from frontend directory
app.mount("/static", StaticFiles(directory="frontend"), name="static")

# Handle the root URL to serve your index.html
@app.get("/", response_class=HTMLResponse)
async def root():
    with open(os.path.join("frontend", "index.html")) as f:
        return f.read()
