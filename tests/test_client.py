"""Integration tests for the OWGR client against the live API."""
import pytest

from owgr_client.client import OwgrClient
from owgr_client.models.owgr_tour import OwgrTour, LEGACY_TOUR_CODE_MAP
from owgr_client.models.owgr_player import OwgrPlayer


@pytest.fixture(scope="module")
def client():
    return OwgrClient()


class TestGetTours:
    def test_returns_nonempty_list(self, client):
        tours = client.get_tours()
        assert isinstance(tours, list)
        assert len(tours) > 0

    def test_tour_has_expected_fields(self, client):
        tour = client.get_tours()[0]
        assert "tourId" in tour
        assert "name" in tour
        assert "code" in tour

    def test_tours_are_cached(self, client):
        t1 = client.get_tours()
        t2 = client.get_tours()
        assert t1 is t2


class TestResolveTourId:
    def test_enum(self, client):
        assert client._resolve_tour_id(OwgrTour.PGATour) == 23

    def test_int(self, client):
        assert client._resolve_tour_id(23) == 23

    def test_legacy_code(self, client):
        assert client._resolve_tour_id("PGAT") == 23

    def test_api_code(self, client):
        assert client._resolve_tour_id("DPWT") == 13

    def test_unknown_code_raises(self, client):
        with pytest.raises(ValueError):
            client._resolve_tour_id("NONEXISTENT_TOUR_XYZ")

    def test_invalid_type_raises(self, client):
        with pytest.raises(TypeError):
            client._resolve_tour_id(3.14)


class TestGetEvents:
    def test_returns_events_dict(self, client):
        result = client.get_events(tour=OwgrTour.PGATour, year=2025)
        assert "eventsList" in result
        assert "totalNumberOfEvents" in result
        assert isinstance(result["eventsList"], list)
        assert result["totalNumberOfEvents"] > 0

    def test_event_has_expected_fields(self, client):
        result = client.get_events(tour=OwgrTour.PGATour, year=2025, page_size=1)
        event = result["eventsList"][0]
        assert "id" in event
        assert "name" in event
        assert "tours" in event
        assert "winners" in event

    def test_legacy_string_code(self, client):
        result = client.get_events(tour="PGAT", year=2025)
        assert result["totalNumberOfEvents"] > 0

    def test_all_tours(self, client):
        result = client.get_events(tour=OwgrTour.ALL, year=2025, page_size=5)
        assert len(result["eventsList"]) > 0


class TestGetEventById:
    def test_returns_event_details(self, client):
        events = client.get_events(tour=OwgrTour.MajorChampionships, year=2025, page_size=1)
        event_id = events["eventsList"][0]["id"]
        event = client.get_event_by_id(event_id)
        assert "name" in event
        assert "results" in event
        assert "tours" in event

    def test_results_have_player_data(self, client):
        events = client.get_events(tour=OwgrTour.MajorChampionships, year=2025, page_size=1)
        event_id = events["eventsList"][0]["id"]
        results = client.get_results_for_event_by_id(event_id)
        assert len(results) > 0
        result = results[0]
        assert "player" in result
        assert "fullName" in result["player"]
        assert "pointsAwarded" in result


class TestGetPlayerById:
    def test_returns_player_data(self, client):
        data = client.get_player_by_id(18417)
        assert "profile" in data
        assert "events" in data
        assert "years" in data
        assert data["profile"]["player"]["fullName"] == "Scottie Scheffler"

    def test_owgr_player_from_api_data(self, client):
        data = client.get_player_by_id(18417)
        player = OwgrPlayer.from_api_data(data)
        assert player.name == "Scottie Scheffler"
        assert player.id == 18417
        assert isinstance(player.stats, dict)
        assert isinstance(player.results, list)
        assert isinstance(player.years, list)
