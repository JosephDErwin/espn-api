from .constant import POSITION_MAP, PRO_TEAM_MAP, STATS_MAP, BREAKDOWN_MAP
from .utils import json_parsing
import pdb
from datetime import datetime


class Player(object):
    '''Player are part of team'''

    def __init__(self, data, year):
        self.name = json_parsing(data, 'fullName')
        self.playerId = json_parsing(data, 'id')
        self.position = POSITION_MAP[json_parsing(data, 'defaultPositionId') - 1]
        self.lineupSlot = POSITION_MAP.get(data.get('lineupSlotId'), '')
        self.eligibleSlots = [POSITION_MAP.get(pos, pos) for pos in json_parsing(data,
                                                                                 'eligibleSlots')]  # if position isn't in position map, just use the position id number
        self.acquisitionType = json_parsing(data, 'acquisitionType')
        self.proTeam = PRO_TEAM_MAP[json_parsing(data, 'proTeamId')]
        self.injuryStatus = json_parsing(data, 'injuryStatus')
        self.stats = {}

        # add available stats
        player = data.get('playerPoolEntry', {}).get('player') or data['player']
        self.injuryStatus = player.get('injuryStatus', self.injuryStatus)
        self.injured = player.get('injured', False)

        self.draft_value = player['ownership']['auctionValueAverage']

        self.started = player['ownership']['percentStarted'] / 100
        self.rostered = player['ownership']['percentOwned'] / 100

        player_stats = player.get('stats', [])
        for stats in player_stats:
            if stats.get('seasonId') != year:
                continue
            stats_breakdown = stats.get('stats') or stats.get('appliedStats', {})
            breakdown = {STATS_MAP.get(int(k), k): v for (k, v) in stats_breakdown.items()}
            points = round(stats.get('appliedTotal', 0), 2)
            scoring_period = stats.get('scoringPeriodId')
            stat_source = stats.get('statSourceId')
            stat_split = stats.get('statSplitTypeId')
            (points_type, breakdown_type) = ('points', BREAKDOWN_MAP[stat_source][stat_split])

                #if stat_source == 0 else ('projected_points', 'projected_breakdown')
            if self.stats.get(scoring_period):
                self.stats[scoring_period][points_type] = points
                self.stats[scoring_period][breakdown_type] = breakdown
            else:
                self.stats[scoring_period] = {points_type: points, breakdown_type: breakdown}
        self.total_points = self.stats.get(0, {}).get('points', 0)
        self.projected_total_points = self.stats.get(0, {}).get('projected_points', 0)

        self.starter_status = {}
        for game_id in player['starterStatusByProGame']:
            self.starter_status[game_id] = player['starterStatusByProGame'][game_id]

    def __repr__(self):
        return 'Player(%s)' % (self.name,)
