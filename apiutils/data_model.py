from enum import Enum
from typing import Dict, Optional, Union
from typing_extensions import Annotated

from dateutil import parser
from pydantic import BaseModel, BeforeValidator, RootModel, conlist

ISODatetime = Annotated[
    str,
    BeforeValidator(lambda x: parser.parse(x).strftime("%Y-%m-%dT%H:%M:%SZ")),
]

class WeatherData(BaseModel):
    timestamp: ISODatetime
    temperature: float 
    precipitation: float 
    humidity: Optional[float] = None
    
class WeatherDataOutput(BaseModel):
    root: Dict[str, conlist(WeatherData, min_length=0)]
    
class ApiDataParams(BaseModel):
    forecast: Optional[bool] = True
