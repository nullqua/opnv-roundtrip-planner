# GTFS Download Script

Downloads and filters GTFS data for Bielefeld (moBiel) from the Germany-wide feed.

## Output

Filtered GTFS files will be saved to `backend/data/gtfs/`:
- `stops.txt` - Bielefeld stops only (~800 stops)
- `stop_times.txt` - Stop times for Bielefeld trips
- `trips.txt` - Trips serving Bielefeld
- `routes.txt` - Routes/lines in Bielefeld
- `calendar.txt` - Service calendar
- `agency.txt` - Agency information

## Data Source

- **Feed:** https://gtfs.de/de/feeds/de_full/
- **License:** CC BY 4.0

## Filtering Logic

1. Filter stops by name prefix (e.g., "Bielefeld,", "Bi-Heepen,")
2. Filter stop_times by filtered stop IDs
3. Filter trips by filtered trip IDs
4. Filter routes by filtered route IDs