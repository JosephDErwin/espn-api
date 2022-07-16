import pdb

from .constant import STATS_MAP

class Matchup(object):
    '''Creates Matchup instance'''
    def __init__(self, data):
        self.home_team_live_score = None
        self.away_team_live_score = None
        self._fetch_matchup_info(data)

    def __repr__(self):
        # TODO: use final score when that's available?
        # writing this too early to see if data['home']['totalPoints'] is final score
        # it might also be used for points leagues instead of category leagues
        if not self.away_team_live_score:
            return 'Matchup(%s, %s)' % (self.home_team, self.away_team, )
        else:
            return 'Matchup(%s %s - %s %s)' % (self.home_team,
                                               str(round(self.home_team_live_score, 1)),
                                               str(round(self.away_team_live_score, 1)),
                                               self.away_team)

    def _fetch_matchup_info(self, data):

        '''Fetch info for matchup'''
        self.home_team = data['home']['teamId']
        self.away_team = data['away']['teamId']

        self.home_stats = {}
        self.away_stats= {}
        if 'cumulativeScore' in data['home'] and 'cumulativeScore' in data['away']:
            for stat in data['home']['cumulativeScore']['scoreByStat']:
                stat_name = STATS_MAP[int(stat)]
                stat_value = data['home']['cumulativeScore']['scoreByStat'][stat]['score']
                self.home_stats[stat_name] = stat_value

            for stat in data['away']['cumulativeScore']['scoreByStat']:
                stat_name = STATS_MAP[int(stat)]
                stat_value = data['away']['cumulativeScore']['scoreByStat'][stat]['score']
                self.away_stats[stat_name] = stat_value

        self.winner = data['winner']

        # if stats are available
        if 'cumulativeScore' in data['home'].keys() and data['home']['cumulativeScore']['scoreByStat']:

            self.home_team_live_score = (data['home']['cumulativeScore']['wins'] +
                                         data['home']['cumulativeScore']['ties']/2)
            self.away_team_live_score = (data['away']['cumulativeScore']['wins'] +
                                         data['away']['cumulativeScore']['ties']/2)
