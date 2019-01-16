import re

def is_str_blank(s):
    return all([ch == " " for ch in s])

def is_str_non_text(s):
    return all([ch in ["\r", "\n", "\t", " "] for ch in s])

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

def get_fantasy_score_for_round(score_str, low_score):
    try:
        s = int(score_str)
        c = 20 - (2 * (s - low_score) )
        if c < 0:
            return 0
        else:
            return c
    except ValueError as ex:
        return 0

def position_as_digit(pos):
    m = re.search("\d+", pos)
    if m:
        try:
            return m.group(0)
        except ValueError:
            return "X"
    return "X"

def tupelize(arr):
    num_tupes = len(arr) // 2
    if len(arr) % 2 != 0:
        raise ValueError("Unable to tupelize list of with odd length.")
    
    ret_tupes = []
    i = 0
    while i < len(arr) - 1:
        tup = (arr[i], arr[i+1])
        ret_tupes.append(tup)
        i += 2

    return ret_tupes

def has_value_for_attr(attr, attr_val, attrs):
#     attrs is a list of tuples
    for tup in attrs:
        if tup[0] == attr:
            return tup[1] == attr_val
    return False
