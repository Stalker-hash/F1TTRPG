import random
import json

def simulate_race(track, teams, num_laps):
    results = {}
    for _ in range(num_laps):
        for team_name, team in teams.items():
            car = team.car
            driver_name = str(team.driver)  # Convert the driver to a string
            lap_time = calculate_lap_time(car, track)
            check_reliability(car)
            results[(team_name, driver_name)] = results.get((team_name, driver_name), 0) + lap_time

            # Increase tire wear and fuel load after each lap
            car.tyre_wear += 1
            car.fuel_load -= 1

        sorted_results = sorted(results.items(), key=lambda x: x[1])

        # Print the results after each lap
        print(f"After lap {_ + 1}:")
        for i, ((team_name, driver_name), time) in enumerate(sorted_results):
            interval = time - sorted_results[0][1] if i != 0 else 0
            print(f"{i + 1}. Team: {team_name}, Driver: {driver_name}, Time: {round(time, 2)} (+{round(interval, 2)}), Tyre wear: {teams[team_name].car.tyre_wear}, Fuel load: {teams[team_name].car.fuel_load}")

    return sorted_results

def calculate_lap_time(car, track, mode='normal'):
    base_time = track.base_time
    power_factor = track.power_factor * 0.1  # Lower values mean more influence
    handling_factor = track.handling_factor * 0.2  # Lower values mean more influence
    downforce_factor = track.downforce_factor * 0.3  # Lower values mean more influence
    unpredictability_factor = 1 + random.uniform(-track.unpredictability_factor,
                                                 track.unpredictability_factor)  # Random factor for unpredictability
    # Add factors for tyre wear and fuel load
    tyre_wear_factor = car.tyre_wear * 0.05
    fuel_load_factor = car.fuel_load * 0.02
    
    if mode == 'normal':
        lap_time = base_time - (car.power * power_factor) - (car.handling * handling_factor) - (
                car.downforce * downforce_factor) + (tyre_wear_factor + fuel_load_factor)
        lap_time *= unpredictability_factor  # Apply unpredictability
    elif mode == 'qualifying':
        lap_time = base_time - (car.power * power_factor) - (car.handling * handling_factor) - (
                car.downforce * downforce_factor) + (tyre_wear_factor + fuel_load_factor)

    return round(lap_time, 3)



with open('Data/carpart_data.json') as f:
    carpart_data = json.load(f)


def check_reliability(car):
    # Generate a random number between 0 and 100
    random_number = random.uniform(0, 100)

    # Iterate over the car part data
    for part in carpart_data['failures']:
        # Convert the percent_cumulative to a float and check if the random number is less than it
        if random_number < float(part['percent_cumulative'].strip('%')):
            # If it is, print the part that failed and return
            print(f"{car.driver}'s {part['category']} failed!")
            return
    print(f"{car.driver} is still running smoothly.")