from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
import os
import api.api as api

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For development only. In production, specify exact domains
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Declaring endpoints
app.include_router(api.api_router)

# First serve your API endpoints (these should take precedence)

# Then serve static assets from frontend directory
# Change this line - don't use "/" as the mount point
app.mount("/static", StaticFiles(directory="frontend"), name="static")

# Finally, handle the root URL to serve your index.html
@app.get("/", response_class=HTMLResponse)
async def root():
    with open(os.path.join("frontend", "index.html")) as f:
        return f.read()
