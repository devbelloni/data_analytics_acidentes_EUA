"""Column configuration for the US Accidents dataset (Moosavi et al., Kaggle)."""

from __future__ import annotations

RENAMES = {"TMC": "Traffic_Message_Channel", "Number": "Street_Number"}

ROAD_FEATURES = [
    "Amenity", "Bump", "Crossing", "Give_Way", "Junction", "No_Exit", "Railway",
    "Roundabout", "Station", "Stop", "Traffic_Calming", "Traffic_Signal", "Turning_Loop",
]

WEATHER_COLUMNS = [
    "Temperature(F)", "Humidity(%)", "Pressure(in)", "Visibility(mi)",
    "Wind_Speed(mph)", "Precipitation(in)",
]

# Columns read from the CSV (only those present in the file are loaded).
USECOLS = [
    "ID", "Severity", "Start_Time", "End_Time", "Start_Lat", "Start_Lng", "Distance(mi)",
    "City", "County", "State", "Timezone", "Weather_Condition", "Sunrise_Sunset",
    *WEATHER_COLUMNS, *ROAD_FEATURES,
]

REQUIRED_COLUMNS = ["Severity", "Start_Time"]

# Accidents lasting longer than this are treated as data-entry errors, not real durations.
MAX_DURATION_MIN = 7 * 24 * 60

WEEKDAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
