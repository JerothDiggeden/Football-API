import requests
from icecream import ic
import streamlit as st


st.set_page_config(page_title="NUFC Stats", page_icon=":material/edit:", layout="wide",
				   initial_sidebar_state="expanded")

url_fixtures = "https://api-football-v1.p.rapidapi.com/v3/fixtures"
url_team_stats = "https://api-football-v1.p.rapidapi.com/v3/teams/statistics"


query_fixtures = {"league": "39", "season": "2024"}
query_team_stats = {"league": "39", "season": "2024", "team": "34"}

headers = {
	"x-rapidapi-key": "1b6ce2494dmshf74f9c461b4cdbbp1d3b11jsndd6ab0d8575c",
	"x-rapidapi-host": "api-football-v1.p.rapidapi.com"
}

response_fix = requests.get(url_fixtures, headers=headers, params=query_fixtures)
response_fix = response_fix.json()

response_team_stats = requests.get(url_team_stats, headers=headers, params=query_team_stats)
response_team_stats = response_team_stats.json()

# ic(response_fix)
ic(response_team_stats['response'])

logo_nufc = response_team_stats['response']['team']['logo']

for resp in response_fix['response']:
	if 'away' in resp['teams']:
		for team in response_fix['response']:
			if 'Newcastle' in team['teams']['away']['name'] or 'Newcastle' in team['teams']['home']['name']:
				teams = team['teams']
				date = team['fixture']['date']
				venue = team['fixture']['venue']

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

col1, col2, col3, col4 = st.columns([2, 3, 1.5, 1.5])

# Add content inside the first column
with col1:
	st.markdown(
		f"""
		<div class="custom-container">
			<h1><img src="{logo_nufc}" alt="NUFC" style="float:left;">Newcastle United</h1>
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
		"""
		<div class="custom-container">
			<h2>Col2</h2>
			<p>Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore 
	et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea 
	commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla 
	pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est 
	laborum. Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore 
	et dolore magna aliqua.</p>
		</div>
		""", unsafe_allow_html=True
	)

with col3:
    st.markdown(
        """
        <div class="custom-container">
            <h2>Col3</h2>
            <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore 
    et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea 
    commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla 
    pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est 
    laborum. Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore 
    et dolore magna aliqua.</p>
        </div>
        """, unsafe_allow_html=True
    )

with col4:
	st.markdown(
		"""
		<div class="custom-container">
			<h2>Col4</h2>
			<p>Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore 
	et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea 
	commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla 
	pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est 
	laborum. Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore 
	et dolore magna aliqua.</p>
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
