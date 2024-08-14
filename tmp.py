import requests
from icecream import ic



fixture_year_counter = 2023
url_team_stats = "https://api-football-v1.p.rapidapi.com/v3/teams/statistics"
tmp_dict = {}

for i in range(1):
    headers = {
        "x-rapidapi-key": "1b6ce2494dmshf74f9c461b4cdbbp1d3b11jsndd6ab0d8575c",
        "x-rapidapi-host": "api-football-v1.p.rapidapi.com"
    }
    query_team_stats_goals = {"league": "39", "season": fixture_year_counter, "team": 34}
    response_team_stats_goals = requests.get(url_team_stats, headers=headers, params=query_team_stats_goals)
    response_team_stats_goals = response_team_stats_goals.json()

    for key, value in response_team_stats_goals.items():
        ic(key, value)
        if 'response' in key:
            for key2, value2 in response_team_stats_goals.items():
                if 'parameters' in key2:
                    ic(value)
                    value_goals = value['goals']['for']['total']['total']
                    tmp_dict[fixture_year_counter] = value_goals
        else:
            continue


ic(tmp_dict)