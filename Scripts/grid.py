from Scripts.models import Car, Driver, Team

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