from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from modules.schema_routes import router as schema_router
from modules.query_routes import router as query_router
from modules.object_routes import router as object_router

app = FastAPI()

# Configure CORS
origins = [
    "http://localhost",
    "http://localhost:80",
    "http://localhost:8080", # For frontend running on 8080 if not proxied
    "http://localhost:3000", # Common for Vite dev server
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(schema_router, prefix="/api", tags=["Schema"])
app.include_router(query_router, prefix="/api", tags=["Query"])
app.include_router(object_router, prefix="/api", tags=["Object"])

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
