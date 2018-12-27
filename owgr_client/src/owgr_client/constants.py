from enum import Enum

BASE_URL = "http://www.owgr.com"
EVENTS_URL_TEMPLATE = "http://www.owgr.com/events?pageSize=400&tour={tour}&year={year}"
RESULTS_FOR_EVENT_TEMPLATE = "http://www.owgr.com/en/Events/EventResult.aspx?eventid={event_id}"

EVENT_COLUMNS = ["Week", "Year", "Tour", "EventUrl", "EventName", "PlayerUrl", "Winner", "WinnerPoints", "WorldRating", "HomeRating", "SoF"]

EVENT_COLS = ['Pos', 'PlayerUrl', 'Name', 'R1', 'R2', 'R3', 'R4', 'Agg', 'Ranking Points']

