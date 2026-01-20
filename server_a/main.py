from fastapi import FastAPI
from router import router as endpoints
import logging

# ---------------------------------------------------
# Configure logging for the whole service
# ---------------------------------------------------
logging.basicConfig(
    level=logging.INFO,  # default level (change to DEBUG while developing)
    format="%(asctime)s [%(levelname)s] %(name)s - %(message)s",
)
logger = logging.getLogger("server-b")

# ---------------------------------------------------
# app
# ---------------------------------------------------

app = FastAPI(
    title="SERVER-B",
    version="1.0.0",
)

# startup log
@app.on_event("startup")
def startup_event():
    logger.info("SERVER-B starting up")


app.include_router(endpoints)


