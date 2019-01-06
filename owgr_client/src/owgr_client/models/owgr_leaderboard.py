

class OwgrLeaderboard(object):
    def __init__(self, results_list=[]):
        self.results = results_list
        self.fantasy_points = None

    def calculate_fantasy_points(self):
        if self.fantasy_points:
            return self.fantasy_points
        else:
            # calculate and set points
            pass

