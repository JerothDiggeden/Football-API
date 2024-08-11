import requests
from icecream import ic
import streamlit as st
import selectorlib



st.set_page_config(page_title="NUFC Stats", page_icon=":material/edit:", layout="wide",
				   initial_sidebar_state="expanded")

team_id = '34'
fixture_year = '2024'

url_fixtures = "https://api-football-v1.p.rapidapi.com/v3/fixtures"
url_team_stats = "https://api-football-v1.p.rapidapi.com/v3/teams/statistics"
url_coaches = "https://api-football-v1.p.rapidapi.com/v3/coachs"
url_players = "https://api-football-v1.p.rapidapi.com/v3/players"
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

ic(response_players)

logo = response_team_stats['response']['team']['logo']
team_name = response_team_stats['response']['team']['name']
coach = response_coaches['response'][0]['name']
coach_photo = response_coaches['response'][0]['photo']
players = {}

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
				ic(name, photo)
				players[name] = photo
				continue
			else:
				ic("FAIL")

ic(players)
players_lst = list(players.keys())
photo_lst = list(players.values())

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
			<h1><img src="{photo_lst[0]}" alt="{players_lst[0]}" style="float:left;width:200px;height:160px">{players_lst[0]}</h1>
			<p>
			
			
			
			</p>
		</div>
		""", unsafe_allow_html=True
	)
	st.markdown("</div>", unsafe_allow_html=True)


with col8:
	st.markdown(
		f"""
		<div class="custom-container">
			<h2>{players[1]}</h2>
			<p>This container has a custom background color.</p>
		</div>
		""", unsafe_allow_html=True
	)

with col9:
	st.markdown(
		f"""
		<div class="custom-container">
			<h2>{players[2]}</h2>
			<p>This container has a custom background color.</p>
		</div>
		""", unsafe_allow_html=True
	)

with col10:
	st.markdown(
		f"""
		<div class="custom-container">
			<h2>{players[3]}</h2>
			<p>This container has a custom background color.</p>
		</div>
		""", unsafe_allow_html=True
	)



# if __name__ == "__main__":
# 	scraped = scrape(url_wikipedia)
# 	extracted = extract()
# 	ic(extracted)

