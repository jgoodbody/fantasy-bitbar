#!/Library/Frameworks/Python.framework/Versions/3.8/bin/python3

from yahoo_oauth import OAuth2
import yahoo_fantasy_api as yfa
import logging

oauth_logger = logging.getLogger('yahoo_oauth')
oauth_logger.disabled = True

oauth = OAuth2(None, None, from_file='/Users/jgoodbody/fun/fantasy-bitbar/oauth.json')

if not oauth.token_is_valid():
    oauth.refresh_access_token()

class color:
   PURPLE = '\033[95m'
   CYAN = '\033[96m'
   DARKCYAN = '\033[36m'
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   YELLOW = '\033[93m'
   RED = '\033[1;31m'
   BOLD = '\033[1;30m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'

gm = yfa.Game(oauth, 'nhl')
game = gm.league_ids(year=2020)
lg = gm.to_league(game[0])
standings = lg.standings()
current_matchups = lg.matchups()['fantasy_content']['league'][1]['scoreboard']['0']['matchups']
team_key = lg.team_key()

for matchup in current_matchups:
    if matchup != 'count':
        for i in range(0,2):
            if current_matchups[matchup]['matchup']['0']['teams'][str(i)]['team'][0][0]['team_key'] == team_key:
                team_idx = str(i)
                opp_idx = '1' if i == 0 else '0'
                matchup_idx = str(matchup)

owner_points = current_matchups[matchup_idx]['matchup']['0']['teams'][team_idx]['team'][1]['team_points']['total']
owner_proj_points = current_matchups[matchup_idx]['matchup']['0']['teams'][team_idx]['team'][1]['team_live_projected_points']['total']

opp_points = current_matchups[matchup_idx]['matchup']['0']['teams'][opp_idx]['team'][1]['team_points']['total']
opp_proj_points = current_matchups[matchup_idx]['matchup']['0']['teams'][opp_idx]['team'][1]['team_live_projected_points']['total']

#print('You vs. opponent')
if owner_points > opp_points:
    print('{0} vs. {1}'.format(owner_points, opp_points))
else:
    print('{0} vs. {1}'.format(owner_points, opp_points))

print('---')

for team in standings:
    if team['team_key'] == team_key:
        print(color.BOLD + team['name'],'\t',
              team['outcome_totals']['wins'],'-',
              team['outcome_totals']['losses'],'-',
              team['outcome_totals']['ties'],'\t',
              team['points_for'],
             color.END)
    else:
        print(team['name'],'\t',
              team['outcome_totals']['wins'],'-',
              team['outcome_totals']['losses'],'-',
              team['outcome_totals']['ties'],'\t',
              team['points_for'])