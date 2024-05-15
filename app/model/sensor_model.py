from datetime import date

from pydantic import BaseModel

# Declare a variable as a str
# and get editor support inside the function
def main(user_id: str):
    return user_id


# A Pydantic model
class User(BaseModel):
    id: float
    name: str
    joined: date


class SensorRequestInnerData(BaseModel):
    id: int
    pm2: float
    pm10: float
    tvoc: float
    hcho: float
    temp: float
    humidity: float
    co2: float

class SensorRequestData(BaseModel):
    data : SensorRequestInnerData
