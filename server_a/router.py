from fastapi import APIRouter, status 
from typing import List
import logging
import os
import requests

from fetch_data import ingest_weather_for_locations
from model import single_counrty

# ---------------------------------------------------
# Logger init
# ---------------------------------------------------

logger = logging.getLogger("server-a.routes")

# ---------------------------------------------------
# Service B URL
# ---------------------------------------------------

# TODO : MODIFY: <endpoint_name>
SERVICE_B_URL = os.getenv(
    "SERVICE_B_URL",
    "http://server-b:8000/<endpoint_name>",  
)

# ---------------------------------------------------
# Routs
# ---------------------------------------------------

router = APIRouter(tags=["Server-A endpoints"])

@router.get("/server-a-health")
def health_check():
    logger.debug("Health check endpoint called")
    return {"status": "ok"}


"""
input example:
    [
  { "country": "Tel Aviv" },
  { "country": "Gaza" },
  { "country": "Teheran" },
  { "country": "Beirut" },
  { "country": "Damascus" }
]

output: list of timestamp per hour: this is one hour -> per country
    {
    'timestamp': datetime.datetime(2026, 1, 26, 23, 0), 
    'location_name': 'Damascus', 
    'country': 'Syria', 
    'latitude': 33.5102, 
    'longitude': 36.29128, 
    'temperature': 5.4, 
    'wind_speed': 11.1, 
    'humidity': 70
    }
"""
@router.post(
    "/get_data",
    status_code=status.HTTP_201_CREATED,
    summary="get data for each country in the list -> send to server_b to formatted",
)
def post_country_data(location_list: List[single_counrty]):

    # Extract plain strings 
    locations = [item.country for item in location_list]

    raw_data = ingest_weather_for_locations(locations)
    
    logger.info("Fetched %d records", len(raw_data))
    # for now, just return the raw data (later: send to Service B)
    return raw_data

    #TODO: COMMENTED OUT FOR CONNECTING TO SERVER_B
    # # Send to Service B the raw_data
    # try:
    #     resp = requests.post(SERVICE_B_URL, json=raw_data, timeout=5)
    #     resp.raise_for_status()
    #     server_b_result = resp.json()
    # except Exception as exc:
    #     server_b_result = {"error": str(exc)}

    # #TODO decide what to return
    # return {"field" : "stuff",
    #         "server_b_result": server_b_result,
    #         }




