import requests
from icecream import ic
import streamlit as st


st.set_page_config(page_title="NUFC Stats", page_icon=":material/edit:", layout="wide",
                   initial_sidebar_state="expanded")

col1, col2, col3, col4, col5 = st.columns([3, 1, 1, 1, 1])

url = "https://api-football-v1.p.rapidapi.com/v3/fixtures"

querystring = {"league": "39", "season": "2024"}

headers = {
	"x-rapidapi-key": "1b6ce2494dmshf74f9c461b4cdbbp1d3b11jsndd6ab0d8575c",
	"x-rapidapi-host": "api-football-v1.p.rapidapi.com"
}

response = requests.get(url, headers=headers, params=querystring)
response = response.json()

ic(response)

for resp in response['response']:
	if 'away' in resp['teams']:
		for team in response['response']:
			if 'Newcastle' in team['teams']['away']['name']:
				teams = team['teams'], team['fixture']['date'], team['fixture']['venue']
			if 'Newcastle' in team['teams']['home']['name']:
				venue = team['teams'], team['fixture']['date'], team['fixture']['venue']

st.markdown(
    """
    <style>
    .custom-container {
        background-color: white;  /* Set your desired background color */
        font-family: Arial, Helvetica, sans-serif;
        h2 {
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

# Add content inside the first column
with col1:
    st.markdown(
        """
        <div class="custom-container">
            <h2>Custom Container</h2>
            <p>This container has a custom background color.</p>
        </div>
        """, unsafe_allow_html=True
    )

with col2:
    st.markdown(
        """
        <div class="custom-container">
            <h2>Custom Container</h2>
            <p>This container has a custom background color.</p>
        </div>
        """, unsafe_allow_html=True
    )

with col3:
    st.markdown(
        """
        <div class="custom-container">
            <h2>Custom Container</h2>
            <p>This container has a custom background color.</p>
        </div>
        """, unsafe_allow_html=True
    )

with col4:
    st.markdown(
        """
        <div class="custom-container">
            <h2>Custom Container</h2>
            <p>This container has a custom background color.</p>
        </div>
        """, unsafe_allow_html=True
    )



with col5:
    st.markdown(
        """
        <div class="custom-container">
            <h2>Custom Container</h2>
            <p>This container has a custom background color.</p>
        </div>
        """, unsafe_allow_html=True
    )
