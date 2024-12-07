from datetime import datetime
import json
from typing import List, Set
from math import radians, cos, sin, sqrt, atan2

from apps.algorithms import calculate_distance


class Coordinates:
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
        created_at: datetime,
        last_updated: datetime, 
        contributors: Set[Contributor], 
        no_of_contributors: int,
        location: str,
        confidence: float, 
        name: str = "Unknown"
    ):
        self.latitude = latitude
        self.longitude = longitude
        self.speed = speed
        self.location = location
        self.created_at = created_at
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
            "location": self.location,
            "created_at": self.created_at.isoformat() if isinstance(self.created_at, datetime) else self.created_at,
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
            location=data["locations"],
            created_at=datetime.fromisoformat(data["created_at"]),
            contributors={contrib for contrib in data["contributors"]},
            last_updated=datetime.fromisoformat(data["last_updated"]),
            no_of_contributors=data["no_of_contributors"],
            confidence=data["confidence"],
            name=data.get("name", "Unknown"),
        )

class DistIndex:
        dist: float
        index: int
        previous_contributor: bool
        def __init__(self, dist: float, index: int, previous_contributor: bool):
            self.dist = dist
            self.index = index
            self.previous_contributor = previous_contributor

import json

file = open("apps/data/point_data_nitc.geojson", mode='r')
jsonFormat = json.load(file)


pointLocations = {}

for location in jsonFormat["features"]:
    try:
        if location["properties"]["name"]:
            pointLocations[Coordinates(latitude=location["geometry"]["coordinates"][1],
                        longitude=location["geometry"]["coordinates"][0])] = str(location["properties"]["name"])
    except:
        continue


file1 = open("apps/data/polygon_data_nitc.geojson", mode='r')
jsonFormat = json.load(file1)
polygonLocations = []


for building in jsonFormat["features"]:
    listOfCoordinates = []
    if str(building["geometry"]["type"]) != "Polygon":
            continue
    for coordiante in building["geometry"]["coordinates"][0]:
        listOfCoordinates.append(Coordinates(latitude=coordiante[1],longitude=coordiante[0]))
    polygonLocations.append(listOfCoordinates)



SOMS: List[Coordinates] = [
     Coordinates(11.313701390321768, 75.92981737369733),
     Coordinates(11.315017696339446, 75.9313695175483),
     Coordinates(11.313917347192696, 75.93274337460556),
     Coordinates(11.312786142727894, 75.93076124495806)
]




ChemicalBuilding: List[Coordinates] = [
    Coordinates(11.322838455948972, 75.93707398841441),
    Coordinates(11.323049025649956, 75.93818836445224),
    Coordinates(11.323857156577299, 75.93769502089383),
    Coordinates(11.323663660647595, 75.93683021865614)
]

ArchitectureBuilding: List[Coordinates] = [
    Coordinates(11.322007557778996, 75.93684182673987),
    Coordinates(11.32230349439012, 75.93739321071692),
    Coordinates(11.323060407791534, 75.93691147524223),
    Coordinates(11.322844147024009, 75.93637169934891)
]

CCC: List[Coordinates] = [
    Coordinates(11.321353481622175, 75.93373579179773),
    Coordinates(11.321619646358643, 75.93398490434353),
    Coordinates(11.321882441678381, 75.93357601616489),
    Coordinates(11.321648284321869, 75.93337500811069)
]

NLHC: List[Coordinates] = [
    Coordinates(11.321359034522976, 75.93296467400279),
    Coordinates(11.321801453297315, 75.93335609245067),
    Coordinates(11.32219223271836, 75.9328436901189),
    Coordinates(11.321816805356052, 75.93247219842837)
]

ELHC: List[Coordinates] = [
    Coordinates(11.322287136228596, 75.93375889765586),
    Coordinates(11.322691871360751, 75.93417593622033),
    Coordinates(11.32295983361603, 75.93385141474354),
    Coordinates(11.322567659605216, 75.9334656896549)
]

ITLabComplex: List[Coordinates] = [
    Coordinates(11.322656980426197, 75.93413465937873),
    Coordinates(11.322962624890756, 75.93447341425362),
    Coordinates(11.323151035699423, 75.9342129430683),
    Coordinates(11.32287330416776, 75.93392115840716)
]

LH: List[Coordinates] = [
    Coordinates(11.316584911457445, 75.92996491625425),
    Coordinates(11.31626584403574, 75.93116887242365),
    Coordinates(11.31696779189411, 75.93138913883303),
    Coordinates(11.317225499592041, 75.93026277651238)
]

MBH: List[Coordinates] = [
    Coordinates(11.316565957279074, 75.93733499148603),
    Coordinates(11.316125775281366, 75.938649654567),
    Coordinates(11.317515490426754, 75.93907932493981),
    Coordinates(11.317899075772106, 75.93781596578395)
]

MainBuildingFront: List[Coordinates] = [
    Coordinates(11.32084369351759, 75.93459623993493),
    Coordinates(11.321225849654146, 75.9348953422709),
    Coordinates(11.321877587624487, 75.93407356615589),
    Coordinates(11.321516169478805, 75.93379561246994)
]


parkingSpace: List[List[Coordinates]] = [LH, MBH, ChemicalBuilding, SOMS]

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
        if isInside(point=coordinate,polygon=area):
            return True
    return False

def isInsideBuilding(coordinate: Coordinates):
    for area in polygonLocations:
        if isInside(point= coordinate,polygon= area):
            return True
    return False

def isInsideNITC(coordinate: Coordinates):
    distance = calculate_distance(latitude1=11.319893740118783, longitude1= 75.93729064918259,latitude2=coordinate.latitude, longitude2=coordinate.longitude) 
    if distance > 1000:
        return False
    return True

map_from_coordinate_to_string = {
    Coordinates(11.321489, 75.934114): "Center Circle NITC",
    Coordinates(11.319975, 75.932740): "Main Gate NITC",
    Coordinates(11.321472, 75.934842): "CCD Building NITC",
    Coordinates(11.322502, 75.935704): "Auditorium Building",
    Coordinates(11.322880, 75.936442): "Architecture Building",
    Coordinates(11.323213, 75.937692): "Chemical Department Building",
    Coordinates(11.321055, 75.938165): "Chemical to Kattangal Road",
    Coordinates(11.318636, 75.939404): "Kattangal",
    Coordinates(11.319110, 75.938126): "Mega Boys Hostel Gate",
    Coordinates(11.317196, 75.937559): "Mega Boys Hostel",
    Coordinates(11.319507, 75.937225): "C Gate",
    Coordinates(11.319773, 75.934481): "NITC Library",
    Coordinates(11.319804, 75.932136): "Main Canteen (Swadishtam)",
    Coordinates(11.316699, 75.930633): "Ladies Hostel NITC",
    Coordinates(11.313859, 75.931000): "SOMS"
}


def find_closest_location(coordinate: Coordinates) -> str:
    def haversine(lat1, lon1, lat2, lon2):

        R = 6371.0  # Earth radius in kilometers

        dlat = radians(lat2 - lat1)
        dlon = radians(lon2 - lon1)
        a = sin(dlat / 2) ** 2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2) ** 2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))

        return R * c * 1000

    closest_location = None
    min_distance = 200

    for loc in map_from_coordinate_to_string.keys():
        distance = haversine(coordinate.latitude, coordinate.longitude, loc.latitude, loc.longitude)
        if distance < min_distance:
            min_distance = distance
            closest_location = loc
    for loc in pointLocations.keys():
        distance = haversine(coordinate.latitude, coordinate.longitude, loc.latitude, loc.longitude)
        if distance < min_distance:
            min_distance = distance
            closest_location = loc
    try:
        return map_from_coordinate_to_string[closest_location] if closest_location else "Unknown"
    except:
        return pointLocations[closest_location] if closest_location else "Unknown"

    

LHBusLandMarks = ["LH Gate","Bottom LH Hostel NIT", "Upper LH NIT hostel", "Ladies Hostel NITC", "Main Canteen (Swadishtam)", "SOMS", "Ladies Hostel", "MBA Hostel NIT", "NITC Guest House"]
MBHLandMarks = ["NITC Library", "C Gate", "Mega Boys Hostel", "Mega Boys Hostel Gate", "Kattangal", "NIT mega hostel phase 2", "Mega Hostel Boys"]

def nameResolve(coordinate: Coordinates) -> str:
    nameOfLandmark = find_closest_location(coordinate=coordinate)

    if nameOfLandmark in LHBusLandMarks:
        return "LH, SOMS"
    elif nameOfLandmark in MBHLandMarks:
        return "MBH, Boys"
    else:
        return "Unknown"
    
