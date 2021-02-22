#!/Library/Frameworks/Python.framework/Versions/3.8/bin/python3

from yahoo_oauth import OAuth2
import yahoo_fantasy_api as yfa
import json
import logging
from colors import *

oauth_logger = logging.getLogger('yahoo_oauth')
oauth_logger.disabled = True

oauth = OAuth2(None, None, from_file='/Users/jgoodbody/fun/fantasy-bitbar/oauth.json')

if not oauth.token_is_valid():
    oauth.refresh_access_token()

gm = yfa.Game(oauth, 'nhl')
game = gm.league_ids(year=2020)
lg = gm.to_league(game[0])
matchups = lg.matchups()['fantasy_content']['league'][1]['scoreboard']['0']['matchups']
team = lg.team_key()

for matchup in matchups:
    if matchup != 'count':
        for i in range(0,2):
            if matchups[matchup]['matchup']['0']['teams'][str(i)]['team'][0][0]['team_key'] == team:
                team_idx = str(i)
                opp_idx = '1' if i == 0 else '0'
                matchup_idx = str(matchup)

owner_points = matchups[matchup_idx]['matchup']['0']['teams'][team_idx]['team'][1]['team_points']['total']
owner_proj_points = matchups[matchup_idx]['matchup']['0']['teams'][team_idx]['team'][1]['team_live_projected_points']['total']

opp_points = matchups[matchup_idx]['matchup']['0']['teams'][opp_idx]['team'][1]['team_points']['total']
opp_proj_points = matchups[matchup_idx]['matchup']['0']['teams'][opp_idx]['team'][1]['team_live_projected_points']['total']

green = '${color green}'
red = '${color red}'

#print('You vs. opponent')
if owner_points > opp_points:
    print(color('{0} vs. {1}'.format(owner_points, opp_points), fg='green'))    
else:
    print(color('{0} vs. {1}'.format(owner_points, opp_points), fg='red'))    

