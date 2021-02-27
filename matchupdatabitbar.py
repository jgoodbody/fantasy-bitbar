#!/Library/Frameworks/Python.framework/Versions/3.8/bin/python3

# <bitbar.title>Fantasy BitBar</bitbar.title>
# <bitbar.version>v0.1</bitbar.version>
# <bitbar.author>Joel Goodbody</bitbar.author>
# <bitbar.author.github>jgoodbody</bitbar.author.github>
# <bitbar.desc>Displays Yahoo Fantasy Information</bitbar.desc>
# <bitbar.image>http://www.hosted-somewhere/pluginimage</bitbar.image>
# <bitbar.dependencies>python</bitbar.dependencies>
# <bitbar.abouturl>https://github.com/jgoodbody/fantasy-bitbar</bitbar.abouturl>

from yahoo_oauth import OAuth2
import yahoo_fantasy_api as yfa
import logging

oauth_logger = logging.getLogger('yahoo_oauth')
oauth_logger.disabled = True

oauth = OAuth2(None, None, from_file='/Users/jgoodbody/fun/fantasy-bitbar/oauth.json')

if not oauth.token_is_valid():
    oauth.refresh_access_token()

# Nice ANSI colors
CPURPLE = '\033[95m'
CCYAN = '\033[96m'
CDARKCYAN = '\033[36m'
CBLUE = '\033[1;34m'
CGREEN = '\033[1;32m'
CYELLOW = '\033[93m'
CRED = '\033[1;31m'
CDARKGRAY = '\033[1;30m'
CBOLD = '\033[30m'
CUNDERLINE = '\033[4m'
CEND = '\033[0m'


gm = yfa.Game(oauth, 'nhl')
game = gm.league_ids(year=2020)
lg = gm.to_league(game[0])
url = lg.settings()['url']
standings = lg.standings()
current_matchups = lg.matchups()['fantasy_content']['league'][1]['scoreboard']['0']['matchups']
team_key = lg.team_key()


for matchup in current_matchups:
    if matchup != 'count':
        for i in range(0, 2):
            if current_matchups[matchup]['matchup']['0']['teams'][str(i)]['team'][0][0]['team_key'] == team_key:
                team_idx = str(i)
                opp_idx = '1' if i == 0 else '0'
                matchup_idx = str(matchup)


def construct_team_info(matchup_index, team_index):
    team = current_matchups[matchup_index]['matchup']['0']['teams'][team_index]['team']
    name = team[0][2]['name']
    pts = team[1]['team_points']['total']
    live_proj_pts = team[1]['team_live_projected_points']['total']
    orig_proj_pts = team[1]['team_projected_points']['total']
    return name, pts, live_proj_pts, orig_proj_pts

def construct_team(matchup_index, team_index):
    team = dict()
    team_info = current_matchups[matchup_index]['matchup']['0']['teams'][team_index]['team']
    team['key'] = team_info[0][0]['team_key']
    team['id'] = team_info[0][1]['team_id']
    team['name'] = team_info[0][2]['name']
    team['pts'] = team_info[1]['team_points']['total']
    team['live_proj_pts'] = team_info[1]['team_live_projected_points']['total']
    team['orig_proj_pts'] = team_info[1]['team_projected_points']['total']
    return team


owner_team, owner_pts, owner_live_proj_pts, owner_orig_proj_pts = construct_team_info(matchup_idx, team_idx)
opp_team, opp_pts, opp_live_proj_pts, opp_orig_proj_pts = construct_team_info(matchup_idx, opp_idx)


def pts_color(pts, live, orig):
    if float(live) > float(orig):
        return CGREEN + pts + CEND
    else:
        return CRED + pts + CEND

owner_color_pts = pts_color(owner_pts, owner_live_proj_pts, owner_orig_proj_pts)
opp_color_pts = pts_color(opp_pts, opp_live_proj_pts, opp_orig_proj_pts)

print('🏒 {0} {1} vs. {2} {3}'.format(owner_team, owner_color_pts, opp_color_pts, opp_team))

print('---')
print(f'League Homepage | font=Courier size=16 href={url}')
print('---')
print(CBOLD + 'Projected Matchup' + CEND + '| font=Courier size=16')
print('Live: {0} vs. {1} | font=Courier'.format(pts_color(owner_live_proj_pts, owner_live_proj_pts, owner_orig_proj_pts), pts_color(opp_live_proj_pts, opp_live_proj_pts, opp_orig_proj_pts)))
print('Orig: {0} vs. {1} | font=Courier'.format(owner_orig_proj_pts, opp_orig_proj_pts))
print('---')
print('All Matchups | font=Courier size=16')
for matchup in current_matchups:
    if matchup != 'count':
        team_1 = construct_team(matchup, '0')
        team_2 = construct_team(matchup, '1')
        print('--{0:<21}{1:>6} vs. {2:>6}{3:>21} | font=Courier'.format(team_1['name'], team_1['pts'], team_2['pts'], team_2['name']))
print('---')
print(CBOLD + 'Standings' + CEND + '| font=Courier size=16')
table = []
for team in standings:
    if team['team_key'] == team_key:
        table.append([team['name'],
              team['outcome_totals']['wins'],
              team['outcome_totals']['losses'],
              team['outcome_totals']['ties'],
              team['points_for']])
    else:
        table.append([team['name'],
              team['outcome_totals']['wins'],
              team['outcome_totals']['losses'],
              team['outcome_totals']['ties'],
              team['points_for']])
print('{0}{1:<21}{2:>5}\t{3:>8}{4} | font=Courier'.format(CDARKGRAY,"Team Name","Record","Total Points",CEND))
for i in range(len(table)):
      print('{0:<21}{1:>2}-{2:>1}-{3:>1}\t{4:>10} | font=Courier'.format(table[i][0],table[i][1],table[i][2],table[i][3],table[i][4]))
