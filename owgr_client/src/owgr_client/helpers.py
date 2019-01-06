import re

def is_str_blank(s):
    return all([ch == " " for ch in s])

def clean_html(s):
    return s.strip().replace("\n","").replace("\r", "")

def get_id_from_player_url(player_url):
    r = re.compile("\d+")
    m = re.search(r, player_url)
    return m.group(0)

def get_id_from_url(url):
    r = re.compile("\d+")
    m = re.search(r, url)
    return m.group(0)

def is_valid_player_url(player_url):
    r = re.compile("\/en\/Ranking\/PlayerProfile.aspx\?playerID=\d+")
    if r.match(player_url):
        return True
    return False