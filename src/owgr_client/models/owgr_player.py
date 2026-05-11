class OwgrPlayer(object):
    """Represents an OWGR player profile."""

    def __init__(self, name, _id, stats, results, years=None):
        self.name = name
        self.id = _id
        self.stats = stats
        self.results = results
        self.years = years or []

    @classmethod
    def from_api_data(cls, player_data):
        """Construct from OwgrClient.get_player_by_id() data."""
        profile = player_data.get("profile", {})
        player_info = profile.get("player", {})
        name = player_info.get("fullName", "")
        player_id = player_info.get("id")

        stats = {
            "currentOWGRRank": profile.get("currentOWGRRank"),
            "bestOWGRRank": profile.get("bestOWGRRank"),
            "lastOWGRRank": profile.get("lastOWGRRank"),
            "pointsAverage": profile.get("pointsAverage"),
            "pointsTotal": profile.get("pointsTotal"),
            "divisorActual": profile.get("divisorActual"),
            "divisorApplied": profile.get("divisorApplied"),
            "country": player_info.get("country"),
        }

        results = player_data.get("events", [])
        years = player_data.get("years", [])

        return cls(name, player_id, stats, results, years=years)
