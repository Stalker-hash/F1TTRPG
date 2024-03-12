from Scripts.models import Car, Driver, Team, Tyre
import random


def create_grid(team_data, car_data, driver_data, tyre_data):
    teams_dict = {}
    available_compounds = ['C1', 'C2', 'C3', 'K1', 'K2', 'K3']  # Assuming these are the available compounds

    for team_info in team_data["teams"]:
        car_info = next((car for car in car_data["cars"] if car["name"] == team_info["car"]), None)
        driver_info = next((driver for driver in driver_data["drivers"] if driver["name"] == team_info["driver"]), None)

        # Randomly select a tyre compound for each car
        random_compound = random.choice(available_compounds)
        tyre_info = next((tyre for tyre in tyre_data["tyres"] if tyre["compound"] == random_compound), None)

        if car_info and driver_info and tyre_info:
            tyre = Tyre(compound=tyre_info["compound"], grip=tyre_info["grip"], tyre_life=tyre_info["tyre_life"],
                        wear_rate=tyre_info["wear_rate"])

            car = Car(car_name=car_info["name"],
                      handling=car_info["handling"],
                      power=car_info["power"],
                      downforce=car_info["downforce"],
                      tyre_wear=car_info["tyre_wear"],
                      fuel_load=car_info["fuel_load"],
                      reliability=car_info["reliability"],
                      driver=driver_info["name"],
                      tyre=tyre,
                      drs=car_info["drs_effect"]
                      )

            driver = Driver(car=car,
                            driver_name=driver_info["name"],
                            driver_number=driver_info["number"],
                            overtaking=driver_info["overtaking"],
                            breaking=driver_info["breaking"],
                            consistency=driver_info["consistency"],
                            adaptability=driver_info["adaptability"],
                            smoothness=driver_info["smoothness"],
                            defence=driver_info["defence"],
                            cornering=driver_info["cornering"])

            team = Team(name=team_info["name"], car=car, driver=driver)

            teams_dict[team.name] = team

    return teams_dict


def find_team_index(team_name, teams):
    for i, team in enumerate(teams):
        if team.name == team_name:
            return i
    return -1
