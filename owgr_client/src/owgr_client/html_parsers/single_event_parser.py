from html.parser import HTMLParser

from owgr_client.constants import EVENT_COLS
from owgr_client.helpers import is_str_blank
from owgr_client.helpers import get_id_from_player_url
from owgr_client.helpers import clean_html

class OwgrSingleEventHtmlParser(HTMLParser):
    def __init__(self):
        self.at_table = False
        self.row = None
        self.all_rows = []
        self.debug = False
        
        super().__init__()
    
    def handle_starttag(self, tag, attrs):
        if not self.at_table and tag == "table":
            if self.debug:
                print("Starting table")
            self.at_table = True
        
        if self.at_table:
            if tag == "tr":
                if self.debug:
                    print("starting new row")
                self.row = []
            
            if self.row is not None and tag == "a":
                self.row.append(attrs[0][1])

    def handle_endtag(self, tag):
        if self.at_table and tag == "table":
            if self.debug:
                print("Leaving the table :", tag)
            self.at_table = False

        if tag == "tr":
            r = [el.strip() for el in self.row]
            if self.debug:
                print(r)
                print("Leaving the row :", tag)
            if len(r) > 0:
                d = dict(zip(EVENT_COLS, self.row))
                self.all_rows.append(d)
            self.row = None

    def handle_data(self, data):
        if self.at_table and self.row is not None:
            if not is_str_blank(data):
                self.row.append(data)