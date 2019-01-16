from owgr_client.helpers import get_id_from_player_url
from owgr_client.helpers import get_fantasy_score_for_round
from owgr_client.helpers import position_as_digit

ROUNDS = ["R1", "R2", "R3", "R4"]
F_SCORE_SUFFIX = "_fscore"

BONUS_POINTS = {"1": 40, "2": 20, "3": 10}

class OwgrLeaderboard(object):
    def __init__(self, results_list=[]):
        self.results = results_list
        self.fantasy_points = None
        self.low_rounds = [99,99,99,99]
        self._calculate_fantasy_points()
        self._extract_player_ids()

    def fantasy_leaderboard(self, as_df=False):
        for result in self.results:
            total_f_points = 0
            f_point_keys = [el+F_SCORE_SUFFIX for el in ROUNDS]
            for k in f_point_keys:
                total_f_points += result[k]
            result["round_f_points"] = total_f_points
            bonus = BONUS_POINTS.get(position_as_digit(result["Pos"]), 0)
            result["total_f_points"] = total_f_points + bonus

        return self.results

    def _extract_player_ids(self):
        for result in self.results:
            result["player_id"] = get_id_from_player_url(result["PlayerUrl"])

    def _calculate_fantasy_points(self):
        if self.fantasy_points:
            return self.fantasy_points
        else:
            # calculate and set points
            self._calculate_row_rounds()
            for result in self.results:
                for idx, r in enumerate(ROUNDS):
                    fscore = get_fantasy_score_for_round(result[r], self.low_rounds[idx])
                    result[r+F_SCORE_SUFFIX] = fscore
        
        return self.results

    def _calculate_row_rounds(self):
        if len(self.results) is 0:
            print("No results to use.")
            return None
        
        for el in self.results:
            for idx, r in enumerate(ROUNDS):
                try:
                    score = int(el[r])
                    if score < self.low_rounds[idx]:
                        self.low_rounds[idx] = score
                except ValueError as ex:
                    # we expect a certain amount of bad ints like '-'
                    pass

        return self.low_rounds


