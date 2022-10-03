from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
from omegaconf import MISSING
from schemas.variables_schema import VariableSchema
from schemas.weather_schema import WeatherSchema
from schemas.pgm_schema import PGMModel


@dataclass
class ConfigSchema:
    host: str = '127.0.0.1'
    port: int = 2000
    asynch: bool = False
    dynamic_weather: bool = False
    variables: Dict[str, VariableSchema] = field(default_factory=dict)
    weather: WeatherSchema = MISSING
    model: PGMModel = MISSING