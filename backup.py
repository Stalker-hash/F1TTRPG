import json
import random



teams_dict = {}
car_class = []


# load json data from file and return it as a dictionary
def load_json_data(file_path):
    with open(file_path) as f:
        data = json.load(f)
    return data


team_data = load_json_data("Data/teams_data.json")
driver_data = load_json_data("Data/drivers_data.json")
car_data = load_json_data("Data/cars_data.json")

# Classes that will be used to create the objects for the teams, drivers and cars
class Team:
    def __init__(self, name, driver, state = 0, car=None, cars=[]):
        self.name = name
        self.driver = driver
        self.state = state
        self.cars = cars
        self.car = car


class Car():
    def __init__(self, car_name, handling, power, downforce, ):
        self.car_name = car_name
        self.handling = handling
        self.power = power
        self.downforce = downforce


class Driver():
    def __init__(self, car, driver_name, driver_number):
        self.name = driver_name
        self.car = car
        self.number = driver_number


class Track:
    def __init__(self, name, length, turns, downforce_factor, handling_factor, power_factor, unpredictability_factor,
                 base_time):
        self.name = name
        self.length = length
        self.turns = turns
        self.downforce_factor = downforce_factor
        self.handling_factor = handling_factor
        self.power_factor = power_factor
        self.unpredictability_factor = unpredictability_factor
        self.base_time = base_time


def create_team_objects():
    teams_dict = {}
    for i in range(len(team_data["teams"])):
        team = Team(team_data["teams"][i]["name"], team_data["teams"][i]["driver"], [team_data["teams"][i]["state"]])
        teams_dict[team.name] = team
    return teams_dict


def assign_car_to_team(teams_dict, car_data, driver_data):
    for team in teams_dict.values():
        # Find the car and driver data for this team
        car_info = next((car for car in car_data["cars"] if car["name"] == team.name), None)
        driver_info = next((driver for driver in driver_data["drivers"] if driver["name"] == team.name), None)

        if car_info and driver_info:
            # Create the Car and Driver objects and assign them to the team
            car = Car(car_name=car_info["name"], handling=car_info["handling"], power=car_info["power"],
                      downforce=car_info["downforce"])
            driver = Driver(car=car, driver_name=driver_info["name"], driver_number=driver_info["number"])
            team.driver = driver
            team.car = car


def calculate_lap_time(car, track):
    base_time = track.base_time
    power_factor = track.power_factor * 0.1  # Lower values mean more influence
    handling_factor = track.handling_factor * 0.2  # Lower values mean more influence
    downforce_factor = track.downforce_factor * 0.3  # Lower values mean more influence
    unpredictability_factor = 1 + random.uniform(-track.unpredictability_factor,
                                                 track.unpredictability_factor)  # Random factor for unpredictability

    lap_time = base_time - (car.power * power_factor) - (car.handling * handling_factor) - (
                car.downforce * downforce_factor)
    lap_time *= unpredictability_factor  # Apply unpredictability

    return round(lap_time, 3)


def simulate_race(track, teams, num_laps):
    results = {}
    lap_times = {(team.name, team.driver.name): [] for team in teams.values()}

    for _ in range(num_laps):
        for team_name, team in teams.items():
            lap_time = calculate_lap_time(team.car, track)  # Pass the 'car' attribute of the 'team' object
            lap_times[(team.name, team.driver.name)].append(lap_time)

            total_time = sum(lap_times[(team.name, team.driver.name)])
            results[(team.name, team.driver.name)] = round(total_time, 3)

        # Sort the results by time in ascending order
        sorted_results = sorted(results.items(), key=lambda x: x[1])

        # Print the results after each lap
        print(f"After lap {_ + 1}:")
        for i, ((team, driver), time) in enumerate(sorted_results):
            interval = time - sorted_results[0][1] if i != 0 else 0
            print(f"{i + 1}. Team: {team}, Driver: {driver}, Time: {time} (+{round(interval, 3)})")

    return sorted_results


def create_grid(team_data, car_data, driver_data):
    teams_dict = {}

    for team_info in team_data["teams"]:
        # Find the car and driver data for this team
        car_info = next((car for car in car_data["cars"] if car["name"] == team_info["car"]), None)
        driver_info = next((driver for driver in driver_data["drivers"] if driver["name"] == team_info["driver"]), None)

        if car_info and driver_info:
            # Create the Car and Driver objects
            car = Car(car_name=car_info["name"], handling=car_info["handling"], power=car_info["power"],
                      downforce=car_info["downforce"])
            driver = Driver(car=car, driver_name=driver_info["name"], driver_number=driver_info["number"])

            # Create the Team object and assign the Car and Driver objects to it
            team = Team(name=team_info["name"], car=car, driver=driver)

            # Add the Team object to the dictionary
            teams_dict[team.name] = team

    return teams_dict


def find_team_index(team_name, teams):
    for i, team in enumerate(teams):
        if team.name == team_name:
            return i
    return -1


teams_dict = create_grid(team_data, car_data, driver_data)
Ferrari = teams_dict["Ferrari"]
track = Track("Silverstone", 5.891, 18, 0.5, 0.5, 0.5, 0.1, 90)
laptime = calculate_lap_time(Ferrari.car, track)
race = simulate_race(track, teams_dict, 5)

print(laptime)
print(race)



