"""Main server driver"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from uvicorn import run

from routers import artists, songs

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
)
app.include_router(artists.router)
app.include_router(songs.router)

if __name__ == "__main__":
    run("main:app", host="0.0.0.0", port=8000, log_level="debug", reload=True)
