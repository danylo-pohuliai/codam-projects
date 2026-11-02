from datetime import datetime
from typing import Optional, Any
from pydantic import BaseModel, Field, ValidationError


class SpaceStation(BaseModel):
    station_id: str = Field(..., min_length=3, max_length=10)
    name: str = Field(..., min_length=1, max_length=50)
    crew_size: int = Field(..., ge=1, le=20)
    power_level: float = Field(..., ge=0.0, le=100.0)
    oxygen_level: float = Field(..., ge=0.0, le=100.0)
    last_maintenance: datetime
    is_operational: bool = Field(default=True)
    notes: Optional[str] = Field(default=None, max_length=200)


valid_data: dict[str, Any] = {
    'station_id': "ISS001",
    'name': "International Space Station",
    'crew_size': 6,
    'power_level': 85.5,
    'oxygen_level': 92.3,
    'last_maintenance': datetime(2019, 6, 1, 12, 22),
    'is_operational': True
}

invalid_data: dict[str, Any] = {
    'station_id': "ISS001",
    'name': "International Space Station",
    'crew_size': 30,
    'power_level': 85.5,
    'oxygen_level': 92.3,
    'last_maintenance': datetime(2019, 6, 1, 12, 22),
    'is_operational': True
}


def main() -> None:
    print("Space Station Data Validation")
    print("========================================")
    try:
        station = SpaceStation(**valid_data)
        print("Valid station created:")
        print(f"ID: {station.station_id}")
        print(f"Name: {station.name}")
        print(f"Crew: {station.crew_size} people")
        print(f"Power: {station.power_level}%")
        print(f"Oxygen: {station.oxygen_level}%")
        print(f"Status: {"Operational" if station.is_operational
                         else "Not Operational"}")
    except ValidationError as e:
        print(e)
    print("\n========================================")
    try:
        SpaceStation(**invalid_data)
    except ValidationError as e:
        print(f"Expected validation error:\n{e.errors()[0]['msg']}")


if __name__ == "__main__":
    main()
