from dataclasses import dataclass
from datetime import date, time


@dataclass
class Stop:
    """Represents a transit stop with location data. 
    
    Attributes:
        id: Unique identifier for the stop
        name: Human-readable name of the stop
        lat: Latitude coordinate
        lon: Longitude coordinate
    """
    id: str
    name: str
    lat: float
    lon: float


@dataclass
class StopTime:
    """Represents a scheduled stop on a trip. 
    
    Note:  GTFS allows times >= 24:00:00 for trips crossing midnight.
    For this MVP, we normalize to 0-23 hours since night buses are 
    out of scope for the route planning feature.
    
    Attributes:
        trip_id: Reference to the Trip this stop belongs to
        arrival:  Scheduled arrival time at this stop
        departure: Scheduled departure time from this stop
        stop_id:  Reference to the Stop
        stop_sequence: Order of this stop in the trip (0-based)
    """
    trip_id: str
    arrival: time
    departure: time
    stop_id: str
    stop_sequence: int


@dataclass
class Trip:
    """Represents a single trip (vehicle journey) on a route.
    
    A trip is one specific instance of a vehicle traveling along a route,
    with defined stop times and service schedule.
    
    Attributes:
        route_id: Reference to the Route this trip belongs to
        service_id: Reference to the Calendar defining when this trip runs
        trip_id:  Unique identifier for this trip
    """
    route_id: str
    service_id: str
    trip_id: str


@dataclass
class Route:
    """Represents a transit route (line).
    
    A route is a group of trips that are displayed to riders as a single
    service (e.g., "Line 4" or "Bus 27").
    
    Attributes:
        id: Unique identifier for the route (GTFS route_id)
        name: Short name of the route (e.g., "4", "27")
        agency: Agency operating this route
        type: Type of transportation (0=Tram, 1=Subway, 3=Bus, etc.)
    """
    id: str
    name: str
    agency: str
    type: int


@dataclass
class Calendar:
    """Defines service availability for a set of dates.
    
    Specifies which days of the week a service runs, and the date range
    for which this schedule is valid.
    
    Attributes:
        monday: True if service runs on Mondays
        tuesday: True if service runs on Tuesdays
        wednesday:  True if service runs on Wednesdays
        thursday: True if service runs on Thursdays
        friday: True if service runs on Fridays
        saturday: True if service runs on Saturdays
        sunday: True if service runs on Sundays
        start_date: Start date of the service period
        end_date: End date of the service period
        service_id:  Unique identifier for this service schedule
    """
    service_id: str
    monday: bool
    tuesday: bool
    wednesday: bool
    thursday: bool
    friday: bool
    saturday: bool
    sunday: bool
    start_date: date
    end_date: date
