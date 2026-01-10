from fastapi import FastAPI
import api

app = FastAPI(title="FRITIME Kosilo Service")

app.include_router(api.router, prefix="/kosilo")
