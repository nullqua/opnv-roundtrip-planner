import csv
import logging
import shutil
import tempfile
import zipfile
from pathlib import Path
from typing import List, Set

import requests

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

GTFS_FEED_URL = "https://download.gtfs.de/germany/nv_free/latest.zip"
OUTPUT_DIR = Path(__file__).resolve().parent / "../data/gtfs"

RELEVANT_FILES = [
    "stops.txt",
    "stop_times.txt",
    "calendar.txt",
    "trips.txt",
    "routes.txt",
    "agency.txt"
]

BIELEFELD_PREFIXES = [
     "Bielefeld Hbf,",
     "Bielefeld,",
     "Bi-Altenhagen,",
     "Bi-Babenhausen,",
     "Bi-Brackwede,",
     "Bi-Brake,",
     "Bi-Brönninghsn,",
     "Bi-Dalbke,",
     "Bi-Eckardtsh.,",
     "Bi-Eckardtsheim,",
     "Bi-Gadderbaum,",
     "Bi-Gellersh.,",
     "Bi-Gellershagen,",
     "Bi-Großdornberg,",
     "Bi-Heepen,",
     "Bi-Heideblümchen,",
     "Bi-Hilleg,",
     "Bi-Hillegossen,",
     "Bi-Hob/Uerent,",
     "Bi-Holtkamp,",
     "Bi-Jöllenbeck,",
     "Bi-Kirchdornberg,",
     "Bi-Lämershagen,",
     "Bi-Milse,",
     "Bi-Oldentrup,",
     "Bi-Quelle,",
     "Bi-Schild,",
     "Bi-Schildesche,",
     "Bi-Schröttinghausen,",
     "Bi-Schröttinghsn,",
     "Bi-Senne,",
     "Bi-Sennest,",
     "Bi-Sennestadt,",
     "Bi-Sieker,",
     "Bi-Stieghorst,",
     "Bi-Theesen,",
     "Bi-Ubbedissen,",
     "Bi-Ummeln,",
     "Bi-Vilsensdorf,",
     "Bi-Windelsbleiche,",
     "Bi-Windflöte,"
]


def download_feed(url: str, dest_path: Path) -> None:
    """Downloads the GTFS feed from the given URL to the destination path."""
    logger.info(f"Downloading GTFS feed from {url}")
    try:
        with requests.get(url, stream=True) as response:
            response.raise_for_status()
            with open(dest_path, "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
        logger.info("Download complete.")
    except requests.RequestException as e:
        logger.error(f"Failed to download feed: {e}")
        raise


def extract_files(zip_path: Path, extract_to: Path, files: List[str]) -> None:
    """Extracts relevant files from the zip archive."""
    logger.info("Extracting files...")
    try:
        with zipfile.ZipFile(zip_path) as zf:
            for filename in files:
                try:
                    zf.extract(filename, extract_to)
                    logger.debug(f"Extracted {filename}")
                except KeyError:
                    logger.warning(f"File {filename} not found in zip archive.")
    except zipfile.BadZipFile as e:
        logger.error(f"Invalid zip file: {e}")
        raise


def filter_stops(input_path: Path, output_path: Path, prefixes: List[str]) -> Set[str]:
    """Filters stops based on prefixes and returns a set of stop_ids."""
    logger.info("Filtering stops...")
    stop_ids = set()
    
    if not input_path.exists():
        logger.warning(f"{input_path} does not exist. Skipping stops filter.")
        return stop_ids

    with open(input_path, "r", encoding="utf-8") as infile, \
         open(output_path, "w", encoding="utf-8", newline="") as outfile:
        
        reader = csv.DictReader(infile)
        if not reader.fieldnames:
             logger.error("stops.txt is empty or malformed.")
             return stop_ids
             
        writer = csv.DictWriter(outfile, fieldnames=reader.fieldnames)
        writer.writeheader()

        count = 0
        for row in reader:
            stop_name = row.get("stop_name", "")
            if any(stop_name.startswith(prefix) for prefix in prefixes):
                writer.writerow(row)
                stop_ids.add(row["stop_id"])
                count += 1
    
    logger.info(f"Found {count} stops matching prefixes.")
    return stop_ids


def filter_stop_times(input_path: Path, output_path: Path, stop_ids: Set[str]) -> Set[str]:
    """Filters stop_times based on stop_ids and returns a set of trip_ids."""
    logger.info("Filtering stop_times...")
    trip_ids = set()

    if not input_path.exists():
        logger.warning(f"{input_path} does not exist. Skipping stop_times filter.")
        return trip_ids

    with open(input_path, "r", encoding="utf-8") as infile, \
         open(output_path, "w", encoding="utf-8", newline="") as outfile:
        
        reader = csv.DictReader(infile)
        if not reader.fieldnames:
             logger.error("stop_times.txt is empty or malformed.")
             return trip_ids

        writer = csv.DictWriter(outfile, fieldnames=reader.fieldnames)
        writer.writeheader()

        count = 0
        for row in reader:
            if row["stop_id"] in stop_ids:
                writer.writerow(row)
                trip_ids.add(row["trip_id"])
                count += 1
                
    logger.info(f"Found {len(trip_ids)} trips from filtered stop_times.")
    return trip_ids


def filter_trips(input_path: Path, output_path: Path, trip_ids: Set[str]) -> Set[str]:
    """Filters trips based on trip_ids and returns a set of route_ids."""
    logger.info("Filtering trips...")
    route_ids = set()

    if not input_path.exists():
        logger.warning(f"{input_path} does not exist. Skipping trips filter.")
        return route_ids

    with open(input_path, "r", encoding="utf-8") as infile, \
         open(output_path, "w", encoding="utf-8", newline="") as outfile:
        
        reader = csv.DictReader(infile)
        if not reader.fieldnames:
             logger.error("trips.txt is empty or malformed.")
             return route_ids

        writer = csv.DictWriter(outfile, fieldnames=reader.fieldnames)
        writer.writeheader()

        count = 0
        for row in reader:
            if row["trip_id"] in trip_ids:
                writer.writerow(row)
                route_ids.add(row["route_id"])
                count += 1

    logger.info(f"Found {len(route_ids)} routes from filtered trips.")
    return route_ids


def filter_routes(input_path: Path, output_path: Path, route_ids: Set[str]) -> None:
    """Filters routes based on route_ids."""
    logger.info("Filtering routes...")
    
    if not input_path.exists():
        logger.warning(f"{input_path} does not exist. Skipping routes filter.")
        return

    with open(input_path, "r", encoding="utf-8") as infile, \
         open(output_path, "w", encoding="utf-8", newline="") as outfile:
        
        reader = csv.DictReader(infile)
        if not reader.fieldnames:
             logger.error("routes.txt is empty or malformed.")
             return

        writer = csv.DictWriter(outfile, fieldnames=reader.fieldnames)
        writer.writeheader()

        count = 0
        for row in reader:
            if row["route_id"] in route_ids:
                writer.writerow(row)
                count += 1
    
    logger.info(f"Filtered down to {count} routes.")


def copy_file(input_path: Path, output_path: Path) -> None:
    """Copies a file from input to output if it exists."""
    if input_path.exists():
        shutil.copy(input_path, output_path)
        logger.info(f"Copied {input_path.name}")
    else:
        logger.warning(f"File {input_path} does not exist, skipping copy.")


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        zip_path = temp_path / "latest.zip"
        
        try:
            download_feed(GTFS_FEED_URL, zip_path)
            extract_files(zip_path, temp_path, RELEVANT_FILES)
            
            stop_ids = filter_stops(temp_path / "stops.txt", OUTPUT_DIR / "stops.txt", BIELEFELD_PREFIXES)
            
            trip_ids = filter_stop_times(temp_path / "stop_times.txt", OUTPUT_DIR / "stop_times.txt", stop_ids)
            
            route_ids = filter_trips(temp_path / "trips.txt", OUTPUT_DIR / "trips.txt", trip_ids)
            
            filter_routes(temp_path / "routes.txt", OUTPUT_DIR / "routes.txt", route_ids)
            
            copy_file(temp_path / "calendar.txt", OUTPUT_DIR / "calendar.txt")
            copy_file(temp_path / "agency.txt", OUTPUT_DIR / "agency.txt")

            logger.info("GTFS data processing complete.")

        except Exception as e:
            logger.error(f"An error occurred: {e}")
            raise

if __name__ == "__main__":
    main()
