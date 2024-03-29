from Scripts.cli import run_cli
from Scripts.helper import load_json_data
from Scripts.grid import create_grid
from Scripts.models import Track
from Scripts.simulation import simulate_race

DEV_MODE = True

# Load the data
team_data = load_json_data('Data/teams_data.json')
car_data = load_json_data('Data/cars_data.json')
driver_data = load_json_data('Data/drivers_data.json')
tyre_data = load_json_data('Data/tyres_data.json')
carparts_data = load_json_data('Data/carpart_data.json')
track_data = load_json_data('Data/tracks_data.json')

# Create the grid
teams_dict = create_grid(team_data, car_data, driver_data, tyre_data)

if not DEV_MODE:
    # Ask the user to input the name of the track
    track_name = input("Enter the name of the track: ")

    # Find the track data
    track_data_item = next((track for track in track_data if track['name'] == track_name), None)

    # Check if the track data was found
    if track_data_item is not None:
        # Create the Track object
        track = Track(track_data_item['name'], track_data_item['length'], track_data_item['turns'],
                      track_data_item['downforce_factor'], track_data_item['handling_factor'],
                      track_data_item['power_factor'], track_data_item['unpredictability_factor'],
                      track_data_item['base_time'], segments=track_data_item['segments'])
    else:
        print(f"Track data for {track_name} not found.")
else:
    track_data_item = next((track for track in track_data if track['name'] == 'Monza'), None)
    track = Track(track_data_item['name'], track_data_item['length'], track_data_item['turns'],
                  track_data_item['downforce_factor'], track_data_item['handling_factor'],
                  track_data_item['power_factor'], track_data_item['unpredictability_factor'],
                  track_data_item['base_time'], segments=track_data_item['segments'])

race = simulate_race(track=track, teams=teams_dict, num_laps=5, tyre_data=tyre_data, mode='debug')

