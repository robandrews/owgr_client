import json
import logging
import re
from datetime import datetime, timezone

import requests

from owgr_client.constants import (
    API_BASE_URL,
    EVENTS_URL,
    TOURS_URL,
    PLAYER_PROFILE_URL,
    PLAYER_YEARS_URL,
)
from owgr_client.models.owgr_tour import OwgrTour, LEGACY_TOUR_CODE_MAP

logger = logging.getLogger(__name__)


class OwgrClient(object):
    """
    A client to interact with the OWGR JSON API at apiweb.owgr.com.
    """

    def __init__(self):
        self._session = requests.Session()
        self._tours_cache = None
        logger.info("Created OWGR client, using API at %s", API_BASE_URL)

    def _get_json(self, url, params=None):
        resp = self._session.get(url, params=params, timeout=30)
        resp.raise_for_status()
        return resp.json()

    def get_tours(self):
        """Return the list of all tours from the API."""
        if self._tours_cache is None:
            self._tours_cache = self._get_json(TOURS_URL)
        return self._tours_cache

    def _resolve_tour_id(self, tour):
        """Resolve a tour parameter to a numeric tourId for the API.

        Accepts an OwgrTour enum, an int (tourId), or a legacy string code.
        """
        if isinstance(tour, OwgrTour):
            return tour.value
        if isinstance(tour, int):
            return tour
        if isinstance(tour, str):
            if tour in LEGACY_TOUR_CODE_MAP:
                return LEGACY_TOUR_CODE_MAP[tour].value
            try:
                return int(tour)
            except ValueError:
                pass
            tours = self.get_tours()
            for t in tours:
                if t["code"] == tour:
                    return t["tourId"]
            raise ValueError(f"Unknown tour code: {tour!r}")
        raise TypeError(f"Invalid tour type: {type(tour)}")

    def get_events(
        self,
        tour=OwgrTour.ALL,
        year=None,
        page_size=0,
        page_number=1,
        sort_string="WeekNumber DESC, "
                    "Winners[0].PointsAwarded DESC",
    ):
        """Fetch events-to-date from the OWGR API.

        Args:
            tour: OwgrTour enum, int tourId, or string code.
            year: Year to query. Defaults to current UTC year.
            page_size: Number of results per page (0 = all).
            page_number: Page number (1-based).
            sort_string: Sort expression for the API.

        Returns:
            A dict with keys ``eventsList``, ``totalNumberOfEvents``,
            ``totalNumberOfPages``.
        """
        if year is None:
            year = datetime.now(timezone.utc).year

        tour_id = self._resolve_tour_id(tour)

        params = {
            "year": year,
            "pageSize": page_size,
            "pageNumber": page_number,
            "tourId": tour_id,
            "sortString": sort_string,
        }
        logger.debug("Fetching events: %s", params)
        return self._get_json(EVENTS_URL, params=params)

    def get_event_by_id(self, event_id):
        """Fetch full details (including results) for a single event.

        The OWGR site embeds event data as server-side-rendered JSON in
        ``__NEXT_DATA__``.  We scrape that to avoid needing a browser.
        """
        slug = self._event_slug(event_id)
        url = f"https://www.owgr.com/events/{slug}"
        resp = self._session.get(url, timeout=30)
        resp.raise_for_status()

        m = re.search(r'__NEXT_DATA__[^>]*>(.*?)</script>', resp.text)
        if not m:
            raise ValueError(
                "Could not find __NEXT_DATA__ on event "
                f"page for id {event_id}"
            )
        data = json.loads(m.group(1))
        page_props = data["props"]["pageProps"]
        event_data = page_props.get("eventDetailsData", {})
        event_details = event_data.get("eventDetails")
        if event_details is None:
            raise ValueError(f"No event details found for id {event_id}")
        return event_details

    def get_results_for_event_by_id(self, event_id):
        """Return the results list for a single event."""
        event = self.get_event_by_id(event_id)
        return event.get("results", [])

    def get_player_by_id(self, player_id, year=-1, counting_events=52):
        """Fetch player profile information.

        Returns a dict with keys ``profile`` (from __NEXT_DATA__) and
        ``events`` (from the events-table API).
        """
        profile = self._get_player_profile_ssr(player_id)
        events = self._get_json(PLAYER_PROFILE_URL, params={
            "playerId": player_id,
            "year": year,
            "countingEventsNumber": counting_events,
        })
        years = self._get_json(PLAYER_YEARS_URL, params={
            "playerId": player_id,
            "id": player_id,
        })
        return {
            "profile": profile,
            "events": events,
            "years": years,
        }

    def _get_player_profile_ssr(self, player_id):
        """Scrape player profile data from the SSR __NEXT_DATA__ blob."""
        url = f"https://www.owgr.com/playerprofile/{player_id}"
        resp = self._session.get(url, timeout=30)
        resp.raise_for_status()

        m = re.search(r'__NEXT_DATA__[^>]*>(.*?)</script>', resp.text)
        if not m:
            raise ValueError(
                "Could not find __NEXT_DATA__ on player "
                f"page for id {player_id}"
            )
        data = json.loads(m.group(1))
        page_props = data["props"]["pageProps"]
        profile_wrapper = page_props.get(
            "playerProfileData", {}
        )
        if (isinstance(profile_wrapper, dict)
                and "playerProfileData" in profile_wrapper):
            return profile_wrapper["playerProfileData"]
        return profile_wrapper

    def _event_slug(self, event_id):
        """Build an event page slug from the event id.

        The OWGR site uses slugs like ``the-masters-tournament-11292``.
        We fetch the events list to find the name, or fall back to a
        direct numeric slug which the site also accepts.
        """
        try:
            year = datetime.now(timezone.utc).year
            for yr in [year, year - 1]:
                data = self.get_events(year=yr, page_size=0)
                for ev in data.get("eventsList", []):
                    if ev["id"] == event_id:
                        name_slug = ev["name"].lower()
                        name_slug = "".join(
                            c if c.isalnum() or c == " "
                            else ""
                            for c in name_slug
                        )
                        name_slug = "-".join(name_slug.split())
                        return f"{name_slug}-{event_id}"
        except Exception:
            pass
        return str(event_id)
