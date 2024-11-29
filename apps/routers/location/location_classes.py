from datetime import datetime
import json
from typing import Set


class Contributor:
    def __init__(self, uuid: str):
        self.uuid = uuid

    def to_dict(self):
        return {
            "uuid": self.uuid
        }

    @staticmethod
    def from_dict(data):
        return Contributor(uuid=data["uuid"])


class BusArrayEntry:
    def __init__(
        self, 
        latitude: float, 
        longitude: float, 
        speed: float, 
        last_updated: datetime, 
        contributors: Set[Contributor], 
        no_of_contributors: int,
        confidence: float, 
        name: str = "Unknown"
    ):
        self.latitude = latitude
        self.longitude = longitude
        self.speed = speed
        self.last_updated = last_updated
        self.contributors = set(contributors) if contributors is not None else set()
        self.no_of_contributors = no_of_contributors
        self.confidence = confidence
        self.name = name

    def to_dict(self):
        return {
            "latitude": self.latitude,
            "longitude": self.longitude,
            "speed": self.speed,
            "last_updated": self.last_updated.isoformat() if isinstance(self.last_updated, datetime) else self.last_updated,  # Convert datetime to ISO format
            "contributors": [str(contrib) for contrib in self.contributors],  # List of dicts
            "no_of_contributors": self.no_of_contributors,
            "confidence": self.confidence,
            "name": self.name,
        }

    @staticmethod
    def from_dict(data):
        return BusArrayEntry(
            latitude=data["latitude"],
            longitude=data["longitude"],
            speed=data["speed"],
            contributors={contrib for contrib in data["contributors"]},
            last_updated=datetime.fromisoformat(data["last_updated"]),
            no_of_contributors=data["no_of_contributors"],
            confidence=data["confidence"],
            name=data.get("name", "Unknown"),
        )

class DistIndex:
        dist: float
        index: int
        def __init__(self, dist: float, index: int):
            self.dist = dist
            self.index = index