#!/usr/bin/python3

from yahoo_oauth import OAuth2
import yahoo_fantasy_api as yfa
import json

sc = OAuth2(None, None, from_file='/home/joel/fun/yahoo/oauth2.json')

gm = yfa.Game(sc, 'nhl')
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

print('  You vs. opponent')
if owner_points > opp_points:
    print('{0} {1} vs. {2} {3}'.format(green, owner_points, red, opp_points))    
else:
    print('{0} {1} vs. {2} {3}'.format(red, owner_points, green, opp_points))    

