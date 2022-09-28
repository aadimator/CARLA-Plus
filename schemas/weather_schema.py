from dataclasses import dataclass, field
from omegaconf import MISSING

# //                            cloudiness   precip.  prec.dep.     wind   azimuth   altitude  fog dens  fog dist  fog fall  wetness
#   WP WP::Default         = {     -1.0f,    -1.0f,     -1.0f,  -1.00f,    -1.0f,     -1.0f,    -1.0f,    -1.0f,    -1.0f,   -1.0f};
#   WP WP::ClearNoon       = {     15.0f,     0.0f,      0.0f,   0.35f,     0.0f,     75.0f,     0.0f,     0.0f,     0.0f,    0.0f};
#   WP WP::CloudyNoon      = {     80.0f,     0.0f,      0.0f,   0.35f,     0.0f,     75.0f,     0.0f,     0.0f,     0.0f,    0.0f};
#   WP WP::WetNoon         = {     20.0f,     0.0f,     50.0f,   0.35f,     0.0f,     75.0f,     0.0f,     0.0f,     0.0f,    0.0f};
#   WP WP::WetCloudyNoon   = {     80.0f,     0.0f,     50.0f,   0.35f,     0.0f,     75.0f,     0.0f,     0.0f,     0.0f,    0.0f};
#   WP WP::MidRainyNoon    = {     80.0f,    30.0f,     50.0f,   0.40f,     0.0f,     75.0f,     0.0f,     0.0f,     0.0f,    0.0f};
#   WP WP::HardRainNoon    = {     90.0f,    60.0f,    100.0f,   1.00f,     0.0f,     75.0f,     0.0f,     0.0f,     0.0f,    0.0f};
#   WP WP::SoftRainNoon    = {     70.0f,    15.0f,     50.0f,   0.35f,     0.0f,     75.0f,     0.0f,     0.0f,     0.0f,    0.0f};
#   WP WP::ClearSunset     = {     15.0f,     0.0f,      0.0f,   0.35f,     0.0f,     15.0f,     0.0f,     0.0f,     0.0f,    0.0f};
#   WP WP::CloudySunset    = {     80.0f,     0.0f,      0.0f,   0.35f,     0.0f,     15.0f,     0.0f,     0.0f,     0.0f,    0.0f};
#   WP WP::WetSunset       = {     20.0f,     0.0f,     50.0f,   0.35f,     0.0f,     15.0f,     0.0f,     0.0f,     0.0f,    0.0f};
#   WP WP::WetCloudySunset = {     90.0f,     0.0f,     50.0f,   0.35f,     0.0f,     15.0f,     0.0f,     0.0f,     0.0f,    0.0f};
#   WP WP::MidRainSunset   = {     80.0f,    30.0f,     50.0f,   0.40f,     0.0f,     15.0f,     0.0f,     0.0f,     0.0f,    0.0f};
#   WP WP::HardRainSunset  = {     80.0f,    60.0f,    100.0f,   1.00f,     0.0f,     15.0f,     0.0f,     0.0f,     0.0f,    0.0f};
#   WP WP::SoftRainSunset  = {     90.0f,    15.0f,     50.0f,   0.35f,     0.0f,     15.0f,     0.0f,     0.0f,     0.0f,    0.0f};

#     'day': (45.0, 0.0),
#     'night': (-90.0, 0.0),
#     'sunset': (0.5, 0.0)}

# WEATHER_PRESETS = {
#     'clear':    [10.0, 0.0, 0.0, 5.0, 0.0, 0.0, 0.2, 0.0, 0.0, 0.0, 0.0331],
#     'overcast': [80.0, 0.0, 0.0, 50.0, 2.0, 0.75, 0.1, 10.0, 0.0, 0.03, 0.0331],
#     'rain':     [100.0, 80.0, 90.0, 100.0, 7.0, 0.75, 0.1, 100.0, 0.0, 0.03, 0.0331]}


@dataclass
class SunSchema:
    azimuth: float = -1.0
    altitude: float = -1.0

@dataclass
class WeatherSchema:
    cloudiness: float = -1.0
    rain: float = -1.0
    puddles: float = -1.0
    wind: float = -1.0
    fog: float = -1.0
    wetness: float = -1.0
    sun: SunSchema = SunSchema()
    