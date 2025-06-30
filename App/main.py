from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# ✅ This is the correct import
from app import config

from app.routes import ai_routes

app = FastAPI(
    title="SmartSDLC",
    version="1.0",
    description="AI-powered SDLC automation with IBM Watsonx"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(ai_routes.router)

@app.get("/")
def read_root():
    return {"message": "SmartSDLC backend is running!"}


from app.routes import auth_routes
app.include_router(auth_routes.router)
