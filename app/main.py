import logging

from fastapi import FastAPI

from app.api.v1.wallets import router

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

app = FastAPI(title="Wallet API")
app.include_router(router)


@app.get("/health")
async def health():
    return {"status": "ok"}
