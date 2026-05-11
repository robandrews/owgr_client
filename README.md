# owgr_client

A Python client to programmatically interact with OWGR (Official World Golf Ranking) data.

Uses the OWGR JSON API at `apiweb.owgr.com` and server-side rendered data from
`owgr.com` for event details and player profiles.

## Installation

```bash
pip install -e .
```

## API

```python
from owgr_client import OwgrClient, OwgrTour

client = OwgrClient()

# Get all tours
tours = client.get_tours()

# Get events (defaults to all tours, current year)
events = client.get_events()

# Filter by tour (enum, tour id, or legacy string code)
events = client.get_events(tour=OwgrTour.PGATour)
events = client.get_events(tour="PGAT")
events = client.get_events(tour=23)

# Filter by year
events = client.get_events(tour=OwgrTour.PGATour, year=2024)

# Get full event details + results by event id
event = client.get_event_by_id(event_id=11292)
results = client.get_results_for_event_by_id(event_id=11292)

# Get player profile by player id
player_data = client.get_player_by_id(player_id=18417)
```

### OwgrTour Enum

The `OwgrTour` enum maps to the OWGR API's numeric `tourId` values. Legacy
string codes (e.g. `"PGAT"`, `"Eur"`, `"US"`) from the old OWGR site are still
accepted by `get_events()` for backward compatibility.
