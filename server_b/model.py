from pydantic import BaseModel
from datetime import datetime


class JsonModel(BaseModel):
    timestamp: datetime
    location_name: str
    country: str
    latitude: float
    longitude: float
    temperature: float
    wind_speed: float
    humidity: int
