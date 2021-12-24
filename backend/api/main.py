"""Main server driver"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from uvicorn import run

from routers import ROUTE_REGISTRY

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
)


for router in ROUTE_REGISTRY:
    app.include_router(router)

FastAPIInstrumentor.instrument_app(app)

if __name__ == "__main__":
    run("main:app", host="0.0.0.0", port=8000, log_level="info", reload=True)
