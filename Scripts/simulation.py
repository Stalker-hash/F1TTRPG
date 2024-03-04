import random
import json

def simulate_race(track, teams, num_laps, tyre_data):
    results = {}
    for lap in range(num_laps):
        for team_name, team in teams.items():
            car = team.car
            driver_name = str(team.driver)
            car.tyre.update_grip_and_life()  # Update tire grip and life
            additional_time_due_to_wear = car.tyre.calculate_effect_on_lap_time()  # Calculate additional time due to wear
            lap_time = calculate_lap_time(car, track) + additional_time_due_to_wear  # Adjust lap time based on tire condition
            if random.uniform(0, 100) > car.reliability:
                time_penalty, failed_part = check_reliability(car)
                print(f"{driver_name} lost {time_penalty} seconds due to a {failed_part} failure.")
            results[(team_name, driver_name)] = results.get((team_name, driver_name), 0) + lap_time

            car.fuel_load -= 1  # Update fuel load

        sorted_results = sorted(results.items(), key=lambda x: x[1])
        print(f"After lap {lap + 1}:")
        for i, ((team_name, driver_name), total_time) in enumerate(sorted_results):
            interval = total_time - sorted_results[0][1] if i != 0 else 0
            print(f"{i + 1}. Team: {team_name}, Driver: {driver_name}, Lap Time: {round(lap_time, 2)}, Total Time: {round(total_time, 2)} (+{round(interval, 2)}), Grip: {round(teams[team_name].car.tyre.grip, 2)}, Tyre Life: {teams[team_name].car.tyre.tyre_life}, Compound: {teams[team_name].car.tyre.compound}, Fuel load: {teams[team_name].car.fuel_load}")

    return sorted_results


def calculate_lap_time(car, track, mode='normal'):
    base_time = track.base_time
    power_factor = track.power_factor * 0.1  # Lower values mean more influence
    handling_factor = track.handling_factor * 0.2  # Lower values mean more influence
    downforce_factor = track.downforce_factor * 0.3  # Lower values mean more influence
    unpredictability_factor = 1 + random.uniform(-track.unpredictability_factor,
                                                 track.unpredictability_factor)  # Random factor for unpredictability
    # Adjust for tyre wear and fuel load
    tyre_wear_factor = car.tyre_wear * 0.05
    fuel_load_factor = car.fuel_load * 0.02
    
    # Update for dynamic tire wear effects
    additional_time_due_to_wear = car.tyre.calculate_effect_on_lap_time()
    
    if mode == 'normal':
        lap_time = base_time - (car.power * power_factor) - (car.handling * handling_factor) - (
                car.downforce * downforce_factor) + (tyre_wear_factor + fuel_load_factor) + additional_time_due_to_wear
        lap_time *= unpredictability_factor  # Apply unpredictability
    elif mode == 'qualifying':
        lap_time = base_time - (car.power * power_factor) - (car.handling * handling_factor) - (
                car.downforce * downforce_factor) + (tyre_wear_factor + fuel_load_factor) + additional_time_due_to_wear

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
            # Determine the severity of the failure
            severity_roll = random.uniform(0, 100)
            if severity_roll < 33:
                severity = 'low'
                time_penalty = 1  # Adjust this value as needed
            elif severity_roll < 66:
                severity = 'medium'
                time_penalty = 2  # Adjust this value as needed
            else:
                severity = 'high'
                time_penalty = 3  # Adjust this value as needed
            print(f"Severity of failure: {severity}")
            return time_penalty, part['category']
    print(f"{car.driver} is still running smoothly.")
    return 0, None