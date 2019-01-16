import requests

from owgr_client.html_parsers.player_parser import OwgrPlayerHtmlParser
from owgr_client.constants import PLAYER_URL_TEMPLATE

class OwgrPlayer(object):
    def __init__(self, name, _id, stats, results, *args, **kwargs):
        self.name = name
        self.id = _id
        self.stats = stats
        self.results = results
        return super().__init__(*args, **kwargs)

    @classmethod
    def from_id(cls, player_id):
        url = PLAYER_URL_TEMPLATE.format(player_id=player_id)
        try:
            resp = requests.get(url)
            parser = OwgrPlayerHtmlParser()
            parser.feed(resp.text)

            name = parser.name
            stats = parser.stats()
            results = parser.results()
        except Exception as ex:
            print("Unable to retrieve player with id: {}".format(player_id))
            raise ex

        return OwgrPlayer(name, player_id, stats, results)