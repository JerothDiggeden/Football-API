import requests
from icecream import ic
import streamlit as st
import selectorlib
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker




st.set_page_config(page_title="NUFC Stats", page_icon=":material/edit:", layout="wide",
				   initial_sidebar_state="expanded")

team_id = '34'
fixture_year = '2024'

url_fixtures = "https://api-football-v1.p.rapidapi.com/v3/fixtures"
url_team_stats = "https://api-football-v1.p.rapidapi.com/v3/teams/statistics"
url_coaches = "https://api-football-v1.p.rapidapi.com/v3/coachs"
url_players = "https://api-football-v1.p.rapidapi.com/v3/players"
url_standings = "https://api-football-v1.p.rapidapi.com/v3/standings"
test = "https://api-football-v1.p.rapidapi.com/v3/teams/"

query_fixtures = {"league": "39", "season": fixture_year}
query_team_stats = {"league": "39", "season": fixture_year, "team": team_id}
query_coaches = {"team": f"{team_id}"}
query_players = {"league": "39", "season": fixture_year, "team": f"{team_id}"}


headers = {
	"x-rapidapi-key": "1b6ce2494dmshf74f9c461b4cdbbp1d3b11jsndd6ab0d8575c",
	"x-rapidapi-host": "api-football-v1.p.rapidapi.com"
}

response_fix = requests.get(url_fixtures, headers=headers, params=query_fixtures)
response_fix = response_fix.json()

response_team_stats = requests.get(url_team_stats, headers=headers, params=query_team_stats)
response_team_stats = response_team_stats.json()

response_test = requests.get(test, headers=headers, params=query_fixtures)
response_test = response_test.json()

response_coaches = requests.get(url_coaches, headers=headers, params=query_coaches)
response_coaches = response_coaches.json()

response_players = requests.get(url_players, headers=headers, params=query_players)
response_players = response_players.json()

standings_dict = {}


global response_standings, season
season = 2010

def stand():
	global response_standings, season
	query_standings = {"season": str(season), "team": str(team_id)}
	response_standings = requests.get(url_standings, headers=headers, params=query_standings)
	response_standings = response_standings.json()
	return response_standings

def make_dict():
	global response_standings, season
	for place in response_standings['response']:
		if 'Premier League' not in place['league']['name']:
			ic('RELEGATED')
			ic(response_standings['parameters']['season'])
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

def replace_none_in_json(data, replace_with='N/A'):
	if isinstance(data, dict):
		return {k: replace_none_in_json(v, replace_with) for k, v in data.items()}
	elif isinstance(data, list):
		return [replace_none_in_json(v, replace_with) for v in data]
	elif data is None:
		return replace_with
	else:
		return data


for i in range(14):
	standings_dict_tmp = stand()
	replace_none_in_json(standings_dict_tmp)
	make_dict()

# for i in range(14):
# 	query_standings = {"season": str(season), "team": str(team_id)}
# 	response_standings = requests.get(url_standings, headers=headers, params=query_standings)
# 	response_standings = response_standings.json()
#
# 	for place in response_standings.get('response', []):
# 		if 'Premier League' not in response_standings['response'][0]['league']['name']:
# 			ic('RELEGATED')
# 			continue
# 		else:
# 			league = place.get('league', {})
# 			standings = league.get('standings', [])
# 			if 'standings' in league and 'Premier League' in standings[0][0].get('group', ''):
# 				standings_dict[season] = standings[0][0].get('rank', 'Unknown')
# 				season += 1
# 			else:
# 				break

ic(standings_dict)

logo = response_team_stats['response']['team']['logo']
team_name = response_team_stats['response']['team']['name']
coach = response_coaches['response'][0]['name']
coach_photo = response_coaches['response'][0]['photo']

players = {}
players_lst = []
photo_lst = []

for id in response_test['response']:
	if team_id in str(id['team']['id']):
		venue_img = id['venue']['image']
		break

for id in response_test['response']:
	if team_id in str(id['team']['id']):
		venue_name = id['venue']['name']
		break

for player in response_players['response']:
	if "player" in player:
		for image in response_players['response']:
			if "name" in image['player'] and "photo" in image['player']:
				photo = player['player']['photo']
				name = player['player']['name']
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

for resp in response_fix['response']:
	if 'away' in resp['teams']:
		for team in response_fix['response']:
			if 'Newcastle' in team['teams']['away']['name'] or 'Newcastle' in team['teams']['home']['name']:
				teams = team['teams']
				date = team['fixture']['date']
				venue = team['fixture']['venue']

# def scrape(url):
# 	response_scrape = requests.get(url)
# 	source = response_scrape.text
# 	return source
#
#
# source = scrape(url_wikipedia)
#
# def extract():
# 	extractor = selectorlib.Extractor.from_yaml_string(source)
# 	value = extractor.extract(extractor)
# 	return value

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
		st.markdown(
			f"""
			<div class="custom-container">
				<h1><img src="{logo}" alt="NUFC" style="float:left;">{team_name}</h1>
				<p>Newcastle United Football Club is a professional association football club based in Newcastle upon Tyne, 
				Tyne and Wear, England. The club compete in the Premier League, the top tier of English football. Since the 
				formation of the club in 1892, when Newcastle East End absorbed the assets of Newcastle West End to become 
				Newcastle United, the club has played its home matches at St James' Park. Located in the centre of Newcastle, 
				it currently has a capacity of 52,374. The club has been a member of the Premier League for all but three years 
				of the competition's history, spending 92 seasons in the top flight as of May 2024, and has never dropped below 
				English football's second tier since joining the Football League in 1893. Newcastle have won four League titles, 
				six FA Cups and an FA Charity Shield, as well as the 1968–69 Inter-Cities Fairs Cup, the ninth-highest total of 
				trophies won by an English club.</p>
			</div>
			""", unsafe_allow_html=True
		)
		st.markdown("</div>", unsafe_allow_html=True)



	with col2:
		st.markdown(
			f"""
			<div class="custom-container">
				<h1><img src="{venue_img}" alt="{venue_name}" style="float:left;width:200px;height:160px">{venue_name}</h1>
				<p>St James' Park has been the home ground of Newcastle United since 1892 and has been used for football 
				since 1880. Throughout its history, the desire for expansion has caused conflict with local residents 
				and the local council. This has led to proposals to move at least twice in the late 1960s, and a 
				controversial 1995 proposed move to nearby Leazes Park. Reluctance to move has led to the distinctive 
				lop-sided appearance of the present-day stadium's asymmetrical stands.</p>
			</div>
			""", unsafe_allow_html=True
		)

	with col3:
		st.markdown(
			f"""
			<div class="custom-container">
				<h1><img src="{coach_photo}" alt="{coach}" style="float:left;">{coach}</h1>
				<p>Edward John Frank Howe (born 29 November 1977) is an English professional football manager and former 
				player. He is the manager of Premier League club Newcastle United and could potentially manage the England 
				national squad.</p>
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

	col1, col2, col3 = st.columns([3, 3, 2])

	x = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]
	rank = list(standings_dict.values())
	years = list(standings_dict.keys())
	years.pop(15)
	years.pop(14)
	years.pop(13)
	rank.pop(15)
	rank.pop(14)
	rank.pop(13)
	ic(years)
	ic(rank)
	labelx = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]




	with col1:
		st.write('Col1')
		# plt.style.use('grayscale')
		plt.plot(years, rank, marker='o')
		for i in range(len(years)):
			plt.text(years[i], rank[i], str(rank[i]), fontsize=12, va='bottom', ha='left', wrap=True, color='blue')
		# plt.xticks(x, labelx)
		plt.yticks(range(int(min(rank)), int(max(rank)) + 1))
		# plt.gca().set_xticklabels(labelx)  # Set the tick labels
		plt.gca().yaxis.set_major_formatter(ticker.FuncFormatter(lambda rank, _: int(rank)))
		plt.xlabel('Years')
		plt.ylabel('Rank')
		plt.title('Newcastle Standings by Year')
		plt.savefig('data/plot.png')
		st.image('data/plot.png')

	with col2:
		st.write('Col2')

	with col3:
		st.write('Col3')
	# if __name__ == "__main__":
	# 	scraped = scrape(url_wikipedia)
	# 	extracted = extract()
	# 	ic(extracted)

