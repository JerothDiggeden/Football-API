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
test = "https://api-football-v1.p.rapidapi.com/v3/teams/"

query_fixtures = {"league": "39", "season": fixture_year}
query_team_stats = {"league": "39", "season": fixture_year, "team": team_id}
query_coaches = {"team": f"{team_id}"}

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

ic(response_coaches)

logo = response_team_stats['response']['team']['logo']
team_name = response_team_stats['response']['team']['name']
coach = response_coaches['response'][0]['name']
coach_photo = response_coaches['response'][0]['photo']

for id in response_test['response']:
	if team_id in str(id['team']['id']):
		venue_img = id['venue']['image']
		break

for id in response_test['response']:
	if team_id in str(id['team']['id']):
		venue_name = id['venue']['name']
		break

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
			<h1>{venue_name}</h1>
						<p>St James' Park has been the home ground of Newcastle United since 1892 and has been used for football 
			since 1880. Throughout its history, the desire for expansion has caused conflict with local residents 
			and the local council. This has led to proposals to move at least twice in the late 1960s, and a 
			controversial 1995 proposed move to nearby Leazes Park. Reluctance to move has led to the distinctive 
			lop-sided appearance of the present-day stadium's asymmetrical stands.</p>
				<img src="{venue_img}" alt="{venue_name}"">
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
			national squad.</p><p>A centre-back during his playing career, Howe spent most of his playing career with AFC Bournemouth, coming 
			up through the youth system and spending eight years with the club, before returning for a second three-year 
			spell to end his career, and retiring from the professional game in 2007. He entered management the following 
			year, taking charge of a Bournemouth side facing relegation to the Conference National in January 2009 as the 
			youngest manager in the Football League.[3] Under his guidance, Bournemouth were able to avoid relegation during 
			his first season in charge, having started the season on minus 17 points, and were promoted to League One the 
			following campaign.</p>
		</div>
		""", unsafe_allow_html=True
	)



col7, col8, col9, col10 = st.columns([2, 1, 1, 1])

with col7:
	st.markdown(
		f"""
		<div class="custom-container">
		<h2>Col7<h2>
		<p>Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore 
	et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea 
	commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla 
	pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.
	Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla 
	pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.</p>
		</div>
		""", unsafe_allow_html=True
	)
	st.markdown("</div>", unsafe_allow_html=True)


with col8:
	st.markdown(
		"""
		<div class="custom-container">
			<h2>Col8</h2>
			<p>This container has a custom background color.</p>
		</div>
		""", unsafe_allow_html=True
	)

with col9:
	st.markdown(
		"""
		<div class="custom-container">
			<h2>Col9</h2>
			<p>This container has a custom background color.</p>
		</div>
		""", unsafe_allow_html=True
	)

with col10:
	st.markdown(
		"""
		<div class="custom-container">
			<h2>Col10</h2>
			<p>This container has a custom background color.</p>
		</div>
		""", unsafe_allow_html=True
	)


# if __name__ == "__main__":
# 	scraped = scrape(url_wikipedia)
# 	extracted = extract()
# 	ic(extracted)

