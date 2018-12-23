import re

def is_str_blank(s):
    return all([ch == " " for ch in s])

def clean_html(s):
    return s.strip().replace("\n","").replace("\r", "")

def get_id_from_player_url(player_url):
    r = re.compile("\d+")
    m = re.search(r, player_url)
    return m.group(0)