from rugby_tipping.models import Match, Pick, Tipper
from django.contrib.auth.models import User

import json
import requests
from collections import namedtuple
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv('API_KEY')

def custom_data_decoder(dataDict):
    return namedtuple('X', dataDict.keys())(*dataDict.values())

def request_api(parameters):
    uri = 'https://api.football-data.org/v4/competitions/PL/matches'
    print(api_key)
    headers = { 'X-Auth-Token': api_key }

    response = requests.get(uri, headers=headers)
    data = response.text
    data_as_json = json.loads(data, object_hook=custom_data_decoder)
    return data_as_json


def convert_get_parameters_to_string(parameters):
    get_string = "?"
    for parameter in parameters:
        get_string += str(parameter[0]) + "=" + str(parameter[1]) + "&"
    return get_string

league_id = "4328"


def add_all_games_from_season():
    parameters = [["id", league_id], ["s", "2024-2025"]]
    data = request_api(parameters)
    #print(data)
    for match in data.matches:
        new_match = Match()
        update_match(new_match, match)
    

def update_match(match_from_db: Match, match_from_api):
    # Extract team names and IDs
    match_from_db.home_team = match_from_api.homeTeam.shortName
    match_from_db.away_team = match_from_api.awayTeam.shortName
    match_from_db.home_api_sports_id = match_from_api.homeTeam.id
    match_from_db.away_api_sports_id = match_from_api.awayTeam.id

    # Extract scores
    match_from_db.home_score = match_from_api.score.fullTime.home
    match_from_db.away_score = match_from_api.score.fullTime.away

    # Determine if the match is complete
    match_from_db.complete = match_from_api.status == 'FINISHED'

    # Extract match round and date
    match_from_db.match_round = match_from_api.matchday
    match_from_db.date = match_from_api.utcDate[:10]  # Extract the date portion (YYYY-MM-DD)

    # Extract API sports ID
    match_from_db.api_sports_id = match_from_api.id

    # Save the updated match to the database
    match_from_db.save()

def delete_duplicates():
    # parameters = [["league", league_id], ["season", "2022"]]
    # data = request_api("games", parameters)
    # print(data)
    # for match in data.response:
    for row in Match.objects.all().reverse():
        if Match.objects.filter(api_sports_id=row.api_sports_id).count() > 1:
            row.delete()
            
            
def update_all_matches():
    parameters = [["id", league_id], ["s", "2024-2025"]]
    data = request_api(parameters)
    print(data)
    print(api_key)
    # for match in data.matches:
        # print(match)
        # match_from_db=Match.objects.get(api_sports_id=match.id)            
        # update_match(match_from_db, match)
    print('All matches updated')


def calculate_points(match: Match):
    print(match.pick_set)
    

def calculate_points_for_user(tipper: Tipper):
    tipper_points = 0
    for pick in tipper.user.pick_set:
        tipper_points += pick.get_points() 
    print(tipper_points)
       
       
def calculate_points_for_all_users():
    tippers = Tipper.objects.all()
    for tipper in tippers:
        tipper.calculate_points() 
    print("All points successfully calculated")
# calculate_points(Match.objects.all()[0])
#  #update_all_matches()
# add_all_games_from_season()
# delete_duplicates()
# calculate_points_for_all_users()