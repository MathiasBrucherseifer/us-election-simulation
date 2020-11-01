from rcp import get_polls  # , get_poll_data
import re
import pandas as pd


# Parse RCP result string into a spread
def parse_rcp_spread(result: str) -> int:
    biden_score = int(re.search('Biden [0-9]{1,2}', result).group(0).replace('Biden ', ''))
    trump_score = int(re.search('Trump [0-9]{1,2}', result).group(0).replace('Trump ', ''))
    return biden_score - trump_score


def get_state_polls():
    # Get all polls from RCP
    trump_polls = get_polls(candidate="Trump")
    # Filter on polls for a specific state
    state_polls = []
    for poll in trump_polls:
        if (': Trump vs. Biden' in poll['title'] and 'General Election' not in poll['title']):
            poll_copy = poll
            poll_copy['state'] = poll_copy['title'].replace(': Trump vs. Biden', '')
            state_polls.append(poll_copy)
    return state_polls


def get_last_election_data() -> pd.DataFrame:
    # Load static data: with 2016 forcast and results
    return pd.read_csv("us_elections_static_data.csv")
