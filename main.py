import requests
from icecream import ic
import streamlit as st
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw, ImageOps
from bs4 import BeautifulSoup




st.set_page_config(page_title="NUFC Web App", page_icon=":material/edit:", layout="wide",
				   initial_sidebar_state="expanded")

fixture_year = '2024'

headers = {
	"x-rapidapi-key": "1b6ce2494dmshf74f9c461b4cdbbp1d3b11jsndd6ab0d8575c",
	"x-rapidapi-host": "api-football-v1.p.rapidapi.com"
}


test = "https://api-football-v1.p.rapidapi.com/v3/teams/"

query_fixtures = {"league": "39", "season": fixture_year}


response_test = requests.get(test, headers=headers, params=query_fixtures)
response_test = response_test.json()

team_id_dict = {'33': '0', '34': '0', '35': '0', '36': '0', '37': '0', '38': '0', '39': '0', '40': '0', '41': '0', '42': '0',
		   '43': '0', '44': '0', '45': '0', '46': '0', '47': '0', '48': '0', '49': '0', '50': '0', '51': '0', '52': '0', '53': '0',
				'54': '0', '55': '0', '56': '0', '57': '0', '58':  '0', '59': '0', '60': '0', '61': '0', '62': '0', '63': '0', '64'
				: '0', '65': '0', '66': '0'}


for id, value in team_id_dict.items():
	if id in id:
		for t_id in response_test['response']:
			if id in str(t_id['team']['id']):
				if 'team' in t_id:
					team_id_dict[id] = t_id['team']['name']


for k, v in team_id_dict.copy().items():
	if '0' in v:
		team_id_dict.pop(k)

team_id_lst = list(team_id_dict.values())

select_team = st.selectbox('Team', team_id_lst)

for k, v in team_id_dict.items():
	if select_team in v:
		select_team = k


team_id = select_team

url_fixtures = "https://api-football-v1.p.rapidapi.com/v3/fixtures"
url_team_stats = "https://api-football-v1.p.rapidapi.com/v3/teams/statistics"
url_coaches = "https://api-football-v1.p.rapidapi.com/v3/coachs"
url_players = "https://api-football-v1.p.rapidapi.com/v3/players"
url_standings = "https://api-football-v1.p.rapidapi.com/v3/standings"
test = "https://api-football-v1.p.rapidapi.com/v3/teams/"

query_fixtures = {"league": "39", "season": fixture_year}
query_team_stats = {"league": "39", "season": fixture_year, "team": team_id}
query_coaches = {"team": team_id}
query_players = {"league": "39", "season": fixture_year, "team": team_id}

def replace_none(obj):
	if isinstance(obj, dict):
		return {k: replace_none(v) for k, v in obj.items()}
	elif isinstance(obj, list):
		return [replace_none(item) for item in obj]
	elif obj is None:
		return "None"
	else:
		return obj

response_fix = requests.get(url_fixtures, headers=headers, params=query_fixtures)
response_fix = response_fix.json()
response_fix = replace_none(response_fix)

response_team_stats = requests.get(url_team_stats, headers=headers, params=query_team_stats)
response_team_stats = response_team_stats.json()

response_test = requests.get(test, headers=headers, params=query_fixtures)
response_test = response_test.json()

response_coaches = requests.get(url_coaches, headers=headers, params=query_coaches)
response_coaches = response_coaches.json()

response_players = requests.get(url_players, headers=headers, params=query_players)
response_players = response_players.json()

standings_dict = {}

tmp_lst = []
ic(response_team_stats)

url_epl = f"https://en.wikipedia.org/wiki/English Premier League"
response_epl = requests.get(url_epl)
soup_team = BeautifulSoup(response_epl.content, 'html.parser')
paragraphs_epl = soup_team.find_all('p')

# Filter out only the first two non-empty paragraphs
first_two_paragraphs_epl = [p.get_text() for p in paragraphs_epl if p.get_text().strip()][:2]
par_1_epl = first_two_paragraphs_epl[0]

st.sidebar.markdown(
		"""
		<style>
		.custom-container {
			background-color: white;  /* Set your desired background color */
			font-family: Arial, Helvetica, sans-serif;
			h2 {
				  color: black;
				}
			h1 {
				  color: black;
				}
			p {
				  color: black;
				}
			padding: 20px;
			border-radius: 10px;
			margin: 10px 0;
		}
		</style>
		""", unsafe_allow_html=True
	)

st.sidebar.title("English Premier League")
st.sidebar.markdown(
			f"""
					<div class="custom-container">
						<h1 style="text-align: center;"><img src="{response_team_stats['response']['league']['logo']}" style="float:left">
						<p><b>{par_1_epl}</b></p>
					</div>
					""", unsafe_allow_html=True
		)

for value in response_coaches['response']:
	tmp_lst.append(value['team']['name'])

global response_standings, season
season = 2010

def stand():
	global response_standings, season
	query_standings = {"season": str(season), "team": str(team_id)}
	response_standings = requests.get(url_standings, headers=headers, params=query_standings)
	response_standings = response_standings.json()
	return response_standings

def make_dict(replaced_stand):
	global season
	for place in replaced_stand['response']:
		if 'Premier League' not in place['league']['name']:
			ic('RELEGATED')
			ic(replaced_stand['parameters']['season'])
			standings_name = place['league']['name']
			return standings_name
			continue
		else:
			league = place.get('league', {})
			standings = league.get('standings', [])
			if 'standings' in league and 'Premier League' in standings[0][0].get('group', ''):
				standings_dict[season] = standings[0][0].get('rank', 'Unknown')
				season += 1
			else:
				break


def add_rounded_corners(image, radius):
	# Create a mask with the same size as the image, filled with 0 (black)
	mask = Image.new('L', image.size, 0)

	# Create a white (255) rounded rectangle on the mask
	draw = ImageDraw.Draw(mask)
	draw.rounded_rectangle([(0, 0), image.size], radius=radius, fill=255)

	# Apply the rounded mask to the image
	rounded_image = ImageOps.fit(image, mask.size, centering=(0.5, 0.5))
	rounded_image.putalpha(mask)

	return rounded_image


season = 2010
progress_bar = st.progress(0)
total_iterations_stand = 14
for i in range(total_iterations_stand):
	percent_complete = int((i + 1) / total_iterations_stand * 100)
	progress_bar.progress(percent_complete)
	query_standings = {"season": str(season), "team": str(team_id)}
	response_standings = requests.get(url_standings, headers=headers, params=query_standings)
	response_standings = response_standings.json()

	for place in response_standings['response']:
		if 'Premier League' not in place['league']['name']:
			season += 1
			break
		else:
			league = place['league'].get('name', {})
			standings = place.get('league', {})
			standings = standings.get('standings', [])
			standings_dict[season] = standings[0][0].get('rank', 'Unknown')
			season += 1
			break


team_name = response_team_stats['response']['team']['name']
coach = response_coaches['response'][0]['name']
coach_photo = response_coaches['response'][0]['photo']

players = {}
fixture_next = {}
fixtures_dict = {}
logo_dict = {}
logo_last_dict = {}
players_lst = []
photo_lst = []
logo_count = 0
logo_last_count = 0
fix_count = 0
index = 0
logo = response_team_stats['response']['team']['logo']

# for i in range(367):
# 	for k, v in response_fix['response'][i].items():
# 		if 'goals' in k:
# 			if 'None' in str(v['away']):
# 				for t, i in response_fix['response'][i].items():
# 					if 'teams' in t:
# 						if team_name in i['away']['name'] or team_name in i['home']['name']:
# 							if team_name in i['away']['name']:
# 								logo_dict[logo_count] = i['away']['logo']
# 								logo_count += 1
# 							else:
# 								logo_dict[logo_count] = i['home']['logo']
# 								logo_count += 1
# 						else:
# 							continue
# 			else:
# 				for first, last in response_fix['response'][i].items():
# 					if 'teams' in first:
# 						if team_name in last['away']['name'] or team_name in last['home']['name']:
# 							if team_name in last['away']['name']:
# 								logo_last_dict[logo_count] = last['home']['logo']
# 								logo_count += 1
# 							else:
# 								logo_last_dict[logo_count] = last['away']['logo']
# 								logo_count += 1

for i in range(367):
	for k, v in response_fix['response'][i].items():
		if 'goals' in k:
			if 'None' in str(v['away']):
				for k, v in response_fix['response'][i].items():
					if 'teams' in k:
						if team_name in v['away']['name'] or team_name in v['home']['name']:
							if team_name in v['away']['name']:
								logo_dict[logo_count] = v['home']['logo']
								logo_count += 1
							else:
								logo_dict[logo_count] = v['away']['logo']
								logo_count += 1
						else:
							continue
			else:
				for k, v in response_fix['response'][i].items():
					if 'teams' in k:
						if team_name in v['away']['name'] or team_name in v['home']['name']:
							if team_name in v['away']['name']:
								logo_last_dict[logo_count] = v['home']['logo']
							else:
								logo_last_dict[logo_count] = v['away']['logo']

				for k, v in response_fix['response'][i].items():
					if 'score' in k:
						for t, y in response_fix['response'][i].items():
							if 'teams' in t:
								if team_name in y['away']['name'] or team_name in y['home']['name']:
									if team_name in y['away']['name']:
										goals_for = str(v['fulltime']['away'])
										goals_against = str(v['fulltime']['home'])
									else:
										goals_for = str(v['fulltime']['home'])
										goals_against = str(v['fulltime']['away'])

				for k, v in response_fix['response'][i].items():
					if 'score' in k:
						for t, i in response_fix['response'][i].items():
							if 'teams' in t:
								ic('teams')
								if team_name in i['away']['name'] or team_name in i['home']['name']:
									ic('Team Name', team_name)
									if team_name in i['away']['name']:
										ic('None')
										if 'None' in k['score']['fulltime']['away']:
											goals_for = '0'
											goals_against = '0'
									else:
										goals_for = str(v['fulltime']['away'])
										goals_against = str(v['fulltime']['home'])
								else:
									goals_for = str(v['fulltime']['home'])
									goals_against = str(v['fulltime']['away'])

				logo_last_count += 1
				continue

ic(logo_last_dict)

for i in range(367):
	for k, v in response_fix['response'][i - 1].items():
		if 'goals' in k:
			if 'None' in str(v['away']):
				for k, v in response_fix['response'][i - 1].items():
					if 'teams' in k:
						if team_name in v['away']['name'] or team_name in v['home']['name']:
							fixture_next[i] = v
						else:
							continue
			else:
				fixtures_dict[i] = v
				fix_count += 1

for id in response_test['response']:
	if team_id in str(id['team']['id']):
		venue_img = id['venue']['image']
		break


for id in response_test['response']:
	if team_id in str(id['team']['id']):
		venue_name = id['venue']['name']
		break

for image in response_players['response']:
	if "name" in image['player'] and "photo" in image['player']:
		photo = image['player']['photo']
		name = image['player']['name']
		players[name] = photo
		players_lst.append(name)
		photo_lst.append(photo)
		continue
	else:
		ic("FAIL")


sorted(players)
players_lst = players.keys()
players_lst = sorted(players_lst)
url_wikipedia = f"https://en.wikipedia.org/wiki/{venue_name}"


for team in response_fix['response']:
	if team_name in team['teams']['away']['name'] or 'Newcastle' in team['teams']['home']['name']:
		teams = team['teams']
		date = team['fixture']['date']
		venue = team['fixture']['venue']

team = response_team_stats['response']['team']['name']

if 'Newcastle' in team_name:
	team_name = team_name + " " + 'United'

tab1, tab2 = st.tabs(["About", "Stats"])

with tab1:

	st.markdown(
		"""
		<style>
		.custom-container {
			background-color: white;  /* Set your desired background color */
			font-family: Arial, Helvetica, sans-serif;
			h2 {
				  color: black;
				}
			h1 {
				  color: black;
				}
			p {
				  color: black;
				}
			padding: 20px;
			border-radius: 10px;
			margin: 10px 0;
		}
		</style>
		""", unsafe_allow_html=True
	)
	st.header("Club")
	col1, col2, col3 = st.columns([3, 3, 2])


	# Add content inside the first column
	with col1:
		coach_full_name = response_coaches['response'][0]['firstname'] + " " + response_coaches['response'][0]['lastname']
		url_stadium = f"https://en.wikipedia.org/wiki/{venue_name}"
		url_coach = f"https://en.wikipedia.org/wiki/{coach_full_name}"
		url_team = f"https://en.wikipedia.org/wiki/{team_name}"


		# Send a GET request to fetch the page content
		response_stadium = requests.get(url_stadium)
		response_coach = requests.get(url_coach)
		response_team = requests.get(url_team)

		# Parse the HTML content using BeautifulSoup
		soup_stadium = BeautifulSoup(response_stadium.content, 'html.parser')
		soup_coach = BeautifulSoup(response_coach.content, 'html.parser')
		soup_team = BeautifulSoup(response_team.content, 'html.parser')

		# Find all paragraph tags within the main content area
		paragraphs_stadium = soup_stadium.find_all('p')
		paragraphs_coach = soup_coach.find_all('p')
		paragraphs_team = soup_team.find_all('p')

		# Filter out only the first two non-empty paragraphs
		first_two_paragraphs_stadium = [p.get_text() for p in paragraphs_stadium if p.get_text().strip()][:2]
		par_1_stadium = first_two_paragraphs_stadium[0]
		par_2_stadium = first_two_paragraphs_stadium[1]

		first_two_paragraphs_coach = [p.get_text() for p in paragraphs_coach if p.get_text().strip()][:2]
		par_1_coach = first_two_paragraphs_coach[0]

		first_two_paragraphs_team = [p.get_text() for p in paragraphs_team if p.get_text().strip()][:2]
		par_1_team = first_two_paragraphs_team[0]

		st.markdown(
			f"""
			<div class="custom-container">
				<h1><img src="{logo}" alt="{team_name}" style="float:left;">{team_name}</h1>
				<p>{par_1_team}</p>
			</div>
			""", unsafe_allow_html=True
		)
		st.markdown("</div>", unsafe_allow_html=True)



	with col2:
		st.markdown(
			f"""
			<div class="custom-container">
				<h1><img src="{venue_img}" alt="{venue_name}" style="float:left;width:200px;height:160px">{venue_name}</h1>
				<p>{par_1_stadium}</p>
				<p>{par_2_stadium}</p>
			</div>
			""", unsafe_allow_html=True
		)

	with col3:
		st.markdown(
			f"""
			<div class="custom-container">
				<h1><img src="{coach_photo}" alt="{coach}" style="float:left;">{coach}</h1>
				<p>{par_1_coach}</p>
			</div>
			""", unsafe_allow_html=True
		)

	st.header("Players")
	col7, col8, col9, col10 = st.columns([1, 1, 1, 1])

	with col7:
		st.markdown(
			f"""
			<div class="custom-container">
				<h1><img src="{players[players_lst[0]]}" alt="{players_lst[0]}" style="float:left;width:200px;height:160px">{players_lst[0]}</h1>
				<h1>
				</h1>
			</div>
			""", unsafe_allow_html=True
		)


	with col8:
		st.markdown(
			f"""
			<div class="custom-container">
				<h1><img src="{players[players_lst[1]]}" alt="{players_lst[1]}" style="float:left;width:200px;height:160px">{players_lst[1]}</h1>
				<h1>
				</h1>
			</div>
			""", unsafe_allow_html=True
		)

	with col9:
		st.markdown(
			f"""
			<div class="custom-container">
				<h1><img src="{players[players_lst[2]]}" alt="{players_lst[2]}" style="float:left;width:200px;height:160px">{players_lst[2]}</h1>
				<h1>
				</h1>
			</div>
			""", unsafe_allow_html=True
		)

	with col10:
		st.markdown(
			f"""
			<div class="custom-container">
				<h1><img src="{players[players_lst[3]]}" alt="{players_lst[3]}" style="float:left;width:200px;height:160px">{players_lst[3]}</h1>
				<h1>
				</h1>
			</div>
			""", unsafe_allow_html=True
		)

	col11, col12, col13, col14 = st.columns([1, 1, 1, 1])

	with col11:
		st.markdown(
			f"""
			<div class="custom-container">
				<h1><img src="{players[players_lst[4]]}" alt="{players_lst[4]}" style="float:left;width:200px;height:160px">{players_lst[4]}</h1>
				<h1>
				</h1>
			</div>
			""", unsafe_allow_html=True
		)


	with col12:
		st.markdown(
			f"""
			<div class="custom-container">
				<h1><img src="{players[players_lst[5]]}" alt="{players_lst[5]}" style="float:left;width:200px;height:160px">{players_lst[5]}</h1>
				<h1>
				</h1>
			</div>
			""", unsafe_allow_html=True
		)

	with col13:
		st.markdown(
			f"""
			<div class="custom-container">
				<h1><img src="{players[players_lst[6]]}" alt="{players_lst[6]}" style="float:left;width:200px;height:160px">{players_lst[6]}</h1>
				<h1>
				</h1>
			</div>
			""", unsafe_allow_html=True
		)

	with col14:
		st.markdown(
			f"""
			<div class="custom-container">
				<h1><img src="{players[players_lst[7]]}" alt="{players_lst[7]}" style="float:left;width:200px;height:160px">{players_lst[7]}</h1>
				<h1>
				</h1>
			</div>
			""", unsafe_allow_html=True
		)


	col15, col16, col17, col18 = st.columns([1, 1, 1, 1])

	with col15:
		st.markdown(
			f"""
			<div class="custom-container">
				<h1><img src="{players[players_lst[8]]}" alt="{players_lst[8]}" style="float:left;width:200px;height:160px">{players_lst[8]}</h1>
				<h1>
				</h1>
			</div>
			""", unsafe_allow_html=True
		)


	with col16:
		st.markdown(
			f"""
			<div class="custom-container">
				<h1><img src="{players[players_lst[9]]}" alt="{players_lst[9]}" style="float:left;width:200px;height:160px">{players_lst[9]}</h1>
				<h1>
				</h1>
			</div>
			""", unsafe_allow_html=True
		)

	with col17:
		st.markdown(
			f"""
			<div class="custom-container">
				<h1><img src="{players[players_lst[10]]}" alt="{players_lst[10]}" style="float:left;width:200px;height:160px">{players_lst[10]}</h1>
				<h1>
				</h1>
			</div>
			""", unsafe_allow_html=True
		)

	with col18:
		st.markdown(
			f"""
			<div class="custom-container">
				<h1><img src="{players[players_lst[11]]}" alt="{players_lst[11]}" style="float:left;width:200px;height:160px">{players_lst[11]}</h1>
				<h1>
				</h1>
			</div>
			""", unsafe_allow_html=True
		)


	col19, col20, col21, col22 = st.columns([1, 1, 1, 1])

	with col19:
		st.markdown(
			f"""
			<div class="custom-container">
				<h1><img src="{players[players_lst[12]]}" alt="{players_lst[12]}" style="float:left;width:200px;height:160px">{players_lst[12]}</h1>
				<h1>
				</h1>
			</div>
			""", unsafe_allow_html=True
		)


	with col20:
		st.markdown(
			f"""
			<div class="custom-container">
				<h1><img src="{players[players_lst[13]]}" alt="{players_lst[13]}" style="float:left;width:200px;height:160px">{players_lst[13]}</h1>
				<h1>
				</h1>
			</div>
			""", unsafe_allow_html=True
		)

	with col21:
		st.markdown(
			f"""
			<div class="custom-container">
				<h1><img src="{players[players_lst[14]]}" alt="{players_lst[14]}" style="float:left;width:200px;height:160px">{players_lst[14]}</h1>
				<h1>
				</h1>
			</div>
			""", unsafe_allow_html=True
		)

	with col22:
		st.markdown(
			f"""
			<div class="custom-container">
				<h1><img src="{players[players_lst[15]]}" alt="{players_lst[15]}" style="float:left;width:200px;height:160px">{players_lst[15]}</h1>
				<h1>
				</h1>
			</div>
			""", unsafe_allow_html=True
		)


	col23, col24, col25, col26 = st.columns([1, 1, 1, 1])

	with col23:
		st.markdown(
			f"""
			<div class="custom-container">
				<h1><img src="{players[players_lst[16]]}" alt="{players_lst[16]}" style="float:left;width:200px;height:160px">{players_lst[16]}</h1>
				<h1>
				</h1>
			</div>
			""", unsafe_allow_html=True
		)


	with col24:
		st.markdown(
			f"""
			<div class="custom-container">
				<h1><img src="{players[players_lst[17]]}" alt="{players_lst[17]}" style="float:left;width:200px;height:160px">{players_lst[17]}</h1>
				<h1>
				</h1>
			</div>
			""", unsafe_allow_html=True
		)

	with col25:
		st.markdown(
			f"""
			<div class="custom-container">
				<h1><img src="{players[players_lst[18]]}" alt="{players_lst[18]}" style="float:left;width:200px;height:160px">{players_lst[18]}</h1>
				<h1>
				</h1>
			</div>
			""", unsafe_allow_html=True
		)

	with col26:
		st.markdown(
			f"""
			<div class="custom-container">
				<h1><img src="{players[players_lst[19]]}" alt="{players_lst[19]}" style="float:left;width:200px;height:160px">{players_lst[19]}</h1>
				<h1>
				</h1>
			</div>
			""", unsafe_allow_html=True
		)


with tab2:
	st.markdown(
		"""
		<style>
		.custom-container {
			background-color: white;  /* Set your desired background color */
			font-family: Arial, Helvetica, sans-serif;
			h2 {
				  color: black;
				}
			h1 {
				  color: black;
				}
			p {
				  color: black;
				}
			padding: 20px;
			border-radius: 10px;
			margin: 10px 0;
		}
		</style>
		""", unsafe_allow_html=True
	)

	st.header("Statistics")
	st.header("Current")

	col1, col2 = st.columns([1, 1])

	with col1:

		st.markdown(
			f"""
					<div class="custom-container">
					<h1>Last Fixture</h1>
						<h1 style="text-align: center;"><img src="{logo}" style="float:left">{goals_for} - {goals_against}<img src="{list(logo_last_dict.values())[-1]}" style="float:right"></h1>
						<h1>
						</h1>
					</div>
					""", unsafe_allow_html=True
		)

	with col2:
		st.markdown(
			f"""
					<div class="custom-container">
						<h1>Next Fixture</h1>
						<h1 style="text-align: center;"><img src="{logo}" style="float:left">{'0'} - {'0'}<img src="{logo_dict[0]}" style="float:right"></h1>
						<h1>
						</h1>
					</div>
					""", unsafe_allow_html=True
		)

	col3, col4, col5 = st.columns([1, 1, 1])

	with col3:
		st.markdown(
			f"""
							<div class="custom-container">
								<h1>Current Rank</h1>
								<h1>
								</h1>
							</div>
							""", unsafe_allow_html=True
		)

	with col4:
		st.markdown(
			f"""
							<div class="custom-container">
								<h1>Goals for, against, and gd</h1>
								<h1>
								</h1>
							</div>
							""", unsafe_allow_html=True
		)

	with col5:
		st.markdown(
			f"""
									<div class="custom-container">
										<h1>Bar Chart Striker Goals</h1>
										<h1>
										</h1>
									</div>
									""", unsafe_allow_html=True
		)

	st.header("Historical")

	col6, col7, col8 = st.columns([1, 1, 1])

	x = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]
	rank = list(standings_dict.values())
	years = list(standings_dict.keys())
	colours = ['#000000', '#3d3d3d', '#8a8a8a']
	labelx = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]


	with col6:
		try:
			plt.style.use('grayscale')
		except KeyError:
			ic('Key Error')
		plt.plot(years, rank, marker='o')
		for i in range(len(years)):
			plt.text(years[i], rank[i], str(rank[i]), fontsize=12, va='bottom', ha='left', wrap=True, color='red')
		plt.yticks(range(int(min(rank)), int(max(rank)) + 1))
		plt.gca().invert_yaxis()
		plt.xlabel('Years')
		plt.ylabel('Rank')
		plt.title(f'{team} Standings by Year')
		plt.savefig('data/plot.png')
		plt_rank_time = 'data/plot.png'
		image = Image.open(plt_rank_time)
		radius = 20
		rounded_image = add_rounded_corners(image, radius)
		st.image(rounded_image)
		plt.close()

	with col7:

		try:
			plt.style.use('grayscale')
		except KeyError:
			ic('Key Error')
		home_win = []
		home_draw = []
		home_lose = []
		away_win = []
		away_draw = []
		away_lose = []
		results_home = []
		results_away = []
		legend_home = ['Win', 'Draw', 'Lose']
		legend_away = ['Win', 'Draw', 'Lose']
		standings_lst = list(standings_dict.keys())

		for v in response_standings['response']:
			if 'Premier League' in v['league']['name']:
				for a in response_standings['response']:
					if 'standings' in a['league']:
						home_win.append(a['league']['standings'][0][0]['home']['win'])
						home_draw.append(a['league']['standings'][0][0]['home']['draw'])
						home_lose.append(a['league']['standings'][0][0]['home']['lose'])

		hme_win_len, hme_draw_len, hme_lose_len = len(home_win), len(home_draw), len(home_lose)
		total_results = sum(home_win) + sum(home_draw) + sum(home_lose)

		hme_win_perc = (sum(home_win) / total_results) * 100
		hme_draw_perc = (sum(home_draw) / total_results) * 100
		hme_lose_perc = (sum(home_lose) / total_results) * 100
		results_home.append(hme_win_perc)
		results_home.append(hme_draw_perc)
		results_home.append(hme_lose_perc)

		plt.pie(results_home, textprops={'color': 'white', 'fontsize': 14}, autopct='%1.1f%%', startangle=140, colors=colours)
		plt.legend(legend_home, loc='best')
		plt.xlabel('')
		plt.ylabel('')
		plt.title(f'{team} Home Results {standings_lst[0]} - {standings_lst[len(standings_lst) - 1]}')
		plt.savefig('data/plot_home_results.png')
		plt_home_time = 'data/plot_home_results.png'
		image = Image.open(plt_home_time)
		# Add rounded corners to the image
		radius = 20  # Adjust the radius for the corners
		rounded_image = add_rounded_corners(image, radius)
		# Display the image with rounded corners using Matplotlib
		st.image(rounded_image)
		plt.close()

	with col8:
		try:
			plt.style.use('grayscale')
		except KeyError:
			ic('Key Error')
		for v in response_standings['response']:
			if 'Premier League' in v['league']['name']:
				for a in response_standings['response']:
					if 'standings' in a['league']:
						away_win.append(a['league']['standings'][0][0]['away']['win'])
						away_draw.append(a['league']['standings'][0][0]['away']['draw'])
						away_lose.append(a['league']['standings'][0][0]['away']['lose'])

		away_win_len, away_draw_len, away_lose_len = len(away_win), len(away_draw), len(away_lose)
		total_results = sum(away_win) + sum(away_draw) + sum(away_lose)
		away_win_perc = (sum(away_win) / total_results) * 100
		away_draw_perc = (sum(away_draw) / total_results) * 100
		away_lose_perc = (sum(away_lose) / total_results) * 100
		results_away.append(away_win_perc)
		results_away.append(away_draw_perc)
		results_away.append(away_lose_perc)

		plt.pie(results_away, textprops={'color': 'white', 'fontsize': 14}, autopct='%1.1f%%', startangle=140, colors=colours)
		plt.legend(legend_away, loc='best')
		plt.title(f'{team} Away Results {standings_lst[0]} - {standings_lst[len(standings_lst) - 1]}')
		plt.savefig('data/plot_away_results.png')
		plt_away_time = 'data/plot_away_results.png'
		image = Image.open(plt_away_time)
		radius = 20
		rounded_image = add_rounded_corners(image, radius)
		st.image(rounded_image)
		plt.close()

	col7, col8, col9 = st.columns([1, 1, 1])

	with col7:
		goals_for_hme = {}
		goals_for_awa = {}
		fixture_year_counter = 2010
		progress_bar = st.progress(0)
		total_iterations = 15
		for i in range(total_iterations):
			percent_complete = int((i + 1) / total_iterations * 100)
			progress_bar.progress(percent_complete)
			query_team_stats_goals = {"league": "39", "season": fixture_year_counter, "team": {team_id}}
			response_team_stats_goals = requests.get(url_team_stats, headers=headers, params=query_team_stats_goals)
			response_team_stats_goals = response_team_stats_goals.json()

			for key, value in response_team_stats_goals.items():
				if 'response' in key:
					for key2, value2 in response_team_stats_goals.items():
						if 'parameters' in key2:
							value_goals_for = value['goals']['for']['total']['total']
							value_goals_against = value['goals']['against']['total']['total']
							goals_for_hme[fixture_year_counter] = value_goals_for
							goals_for_awa[fixture_year_counter] = value_goals_against
							fixture_year_counter += 1
				else:
					continue
		dates = list(goals_for_hme.keys())
		goals_for_hme_lst = list(goals_for_hme.values())
		goals_for_awa_lst = list(goals_for_awa.values())
		try:
			plt.style.use('grayscale')
		except KeyError:
			ic('Key Error')
		plt.plot(dates, goals_for_hme_lst, marker='o')
		plt.plot(dates, goals_for_awa_lst, marker='o')
		plt.legend(['Home', 'Away'], loc='best')
		# plt.yticks(range(int(min(goals_for_hme_lst)), int(max(goals_for_hme_lst)) + 1))
		plt.yticks(range(int(min(goals_for_awa_lst)), int(max(goals_for_hme_lst)), 10))
		plt.xlabel('Years')
		plt.ylabel('Goals')
		plt.title(f'{team} Goals {dates[0]} - {dates[-1]}')
		plt.savefig('data/plot_goals.png')
		plt_rank_time = 'data/plot_goals.png'
		image = Image.open(plt_rank_time)
		radius = 20
		rounded_image = add_rounded_corners(image, radius)
		st.image(rounded_image)
		plt.close()

plt.close()
