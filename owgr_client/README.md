# owgr_client

A client to programmatically interact with OWGR data.

## API

* `client = OwgrClient()`
* `client.get_events()`
* `client.get_events(tour="US")`
* `client.get_events(tour=OwgrTour.US)`
* `client.get_events(tour="", year="")`
* `client.get_event(Event)`
* `client.get_event_by_id(event_id)`
* `client.get_player_by_id(player_id)`

