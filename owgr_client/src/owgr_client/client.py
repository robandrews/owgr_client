import logging
import requests

from owgr_client.constants import BASE_URL
from owgr_client.constants import EVENTS_URL_TEMPLATE
from owgr_client.constants import RESULTS_FOR_EVENT_TEMPLATE

from owgr_client.helpers import clean_html, is_str_blank, get_id_from_player_url
from owgr_client.models.owgr_tour import OwgrTour
from owgr_client.html_parsers.events_parser import OwgrEventsHtmlParser
from owgr_client.html_parsers.single_event_parser import OwgrSingleEventHtmlParser

class OwgrClient(object):
    """
    A client to interact with the OWGR website.
    """

    def __init__(self):
        print("Created OWGR client, for", BASE_URL)

    def get_events(self, tour=OwgrTour.PGATour, year=2018):
        if type(tour) == OwgrTour:
            tour_str = tour.value
        elif type(tour) == str:
            tour_str = tour
        else:
            raise ValueError("OwgrClient: invalid value for `tour` parameter.")

        if year < 1980:
            raise ValueError("OwgrClient: invalid value for `year` parameter.")
        
        url = EVENTS_URL_TEMPLATE.format(tour=tour_str, year=year)
        return self._get_and_parse_events_from_url(url, html_parser=OwgrEventsHtmlParser)
    
    def get_results_for_event_by_id(event_id):
        url = RESULTS_FOR_EVENT_TEMPLATE.format(event_id=event_id)
        return self._get_and_parse_events_from_url(url, html_parser=OwgrSingleEventHtmlParser)

    def _get_and_parse_events_from_url(self, url, html_parser):
        try:
            r = requests.get(url)
            if r.status_code == 200:
                txt = clean_html(r.text)
            else:
                raise ValueError("Unable to retrieve events from url: ", url)
        except Exception as ex:
            print("Unable to retrieve events from url: ", url)
            raise ex

        p = html_parser()
        p.feed(txt)
        return p.all_rows[1:]