from html.parser import HTMLParser

from owgr_client.helpers import is_str_non_text
from owgr_client.helpers import has_value_for_attr
from owgr_client.helpers import tupelize
PLAYER_COLS = ["EventUrl", "Event", "Tour", "Week", "Year", "Finish", "RankPoints", "Weight", "AdjPoints", "RankAfter"]

class OwgrPlayerHtmlParser(HTMLParser):
    def __init__(self):
        self.at_stats = False
        self.at_name = False
        self.at_table = False
        self.at_table_body = False
        
        self._stats = []
        self._table_rows = []
        self._current_row = []
        self.name = None
        super().__init__()
    
    def handle_starttag(self, tag, attrs):
        if tag == "ul" and has_value_for_attr("class", "stats", attrs):
            self.at_stats = True
        if tag == "span" and has_value_for_attr("class", "name", attrs):
            self.at_name = True
        if tag == "div" and has_value_for_attr("class", "table_container", attrs):
            self.at_table = True
        if self.at_table and tag == "tr":
            self._current_row = []
        if self.at_table and tag == "a":
            self._current_row.append(attrs[0][1])
            
    def handle_endtag(self, tag):
        if self.at_stats and tag == "ul":
            self.at_stats = False

        if self.at_name and tag == "span":
            self.at_name = False
        
        if self.at_table and tag == "table":
            self.at_table = False
            
        if self.at_table and tag == "tr":
            self._table_rows.append(self._current_row)
     
    def handle_data(self, data):
        if self.at_stats == True:
            s = data.strip()
            if not is_str_non_text(s):
                self._stats.append(s)
        if self.at_name == True:
            s = data.strip()
            self.name = s        
        if self.at_table == True:
            if not is_str_non_text(data):
                self._current_row.append(data)

    def stats(self):
        tup_arr = tupelize(self._stats)
        tup_arr = [(el[0].replace(":", "").replace(" ", "_").lower(), el[1]) for el in tup_arr]
        return {t[0]:t[1] for t in tup_arr}
    
    def results(self):
        rows = self._table_rows[1:]
        return [dict(zip(PLAYER_COLS, row)) for row in rows]
