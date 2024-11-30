from datetime import datetime
import json
from typing import List, Set


class Coordinates:
    latitude: float
    longitude: float

    def __init__(self, latitude: float, longitude: float):
        self.latitude = latitude
        self.longitude = longitude
        

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




ChemicalBuilding: List[Coordinates] = [
    {11.322838455948972, 75.93707398841441},
      {11.323049025649956, 75.93818836445224}, 
        {11.323857156577299, 75.93769502089383},
          {11.323663660647595, 75.93683021865614}
]

ArchitectureBuilding: List[Coordinates] = [
    {11.322007557778996, 75.93684182673987},
    {11.32230349439012, 75.93739321071692},
    {11.323060407791534, 75.93691147524223},
    {11.322844147024009, 75.93637169934891}
]

CCC: List[Coordinates] = [
    {11.321353481622175, 75.93373579179773},
    {11.321619646358643, 75.93398490434353},
    {11.321882441678381, 75.93357601616489},
    {11.321648284321869, 75.93337500811069}
]

NLHC: List[Coordinates] = [
    {11.321359034522976, 75.93296467400279},
    {11.321801453297315, 75.93335609245067},
    {11.32219223271836, 75.9328436901189},
    {11.321816805356052, 75.93247219842837} 
]

ELHC: List[Coordinates] = [
    {11.322287136228596, 75.93375889765586},
    {11.322691871360751, 75.93417593622033},
    {11.32295983361603, 75.93385141474354},
    {11.322567659605216, 75.9334656896549} 
]

ITLabComplex: List[Coordinates] = [
    {11.322656980426197, 75.93413465937873},
    {11.322962624890756, 75.93447341425362},
    {11.323151035699423, 75.9342129430683},
    {11.32287330416776, 75.93392115840716}, 
]

LH: List[Coordinates] = [
    {11.316584911457445, 75.92996491625425},
    {11.31626584403574, 75.93116887242365},
    {11.31696779189411, 75.93138913883303},
    {11.317225499592041, 75.93026277651238}
]
MBH: List[Coordinates] = [
    {11.316565957279074, 75.93733499148603},
    {11.316125775281366, 75.938649654567},
    {11.317515490426754, 75.93907932493981},
    {11.317899075772106, 75.93781596578395},
]

MainBuildingFront: List[Coordinates] = [
    {11.32084369351759, 75.93459623993493},
    {11.321225849654146, 75.9348953422709},
    {11.321877587624487, 75.93407356615589},
    {11.321516169478805, 75.93379561246994}
]


parkingSpace: List[List[Coordinates]] = [LH, MBH, ChemicalBuilding, MainBuildingFront]

def isInside(point: Coordinates, polygon: List[Coordinates]) -> bool:
    x, y = point.latitude, point.longitude
    n = len(polygon)
    inside = False

    p1x, p1y = polygon[0].latitude, polygon[0].longitude
    for i in range(n + 1):
        p2x, p2y = polygon[i % n].latitude, polygon[i % n].longitude
        if y > min(p1y, p2y):
            if y <= max(p1y, p2y):
                if x <= max(p1x, p2x):
                    if p1y != p2y:
                        xinters = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                    if p1x == p2x or x <= xinters:
                        inside = not inside
        p1x, p1y = p2x, p2y

    return inside


def isInParkingArea(coordinate: Coordinates):
    for area in parkingSpace:
        if isInside(coordinate, area):
            return True
    return False