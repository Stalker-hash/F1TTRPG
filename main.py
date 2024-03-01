from Scripts.data import load_json_data
from Scripts.models import Car, Driver, Team, Track
from Scripts.simulation import calculate_lap_time, simulate_race
from Scripts.grid import create_grid, find_team_index

# Load the data
team_data = load_json_data('Data/teams_data.json')
car_data = load_json_data('Data/cars_data.json')
driver_data = load_json_data('Data/drivers_data.json')

# Create the grid
teams_dict = create_grid(team_data, car_data, driver_data)

# Run the simulation
Ferrari = teams_dict["Ferrari"]
track = Track("Silverstone", 5.891, 18, 0.5, 0.5, 0.5, 0.1, 90)
laptime = calculate_lap_time(Ferrari.car, track)
race = simulate_race(track, teams_dict, 5)

# Print the results
print(laptime)
print(race)