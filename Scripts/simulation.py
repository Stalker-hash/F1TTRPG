import random
import json

def simulate_race(track, teams, num_laps):
    results = {}
    for _ in range(num_laps):
        for team_name, team in teams.items():
            car = team.car
            driver_name = str(team.driver)  # Convert the driver to a string
            lap_time = calculate_lap_time(car, track)
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

def reliability_check(car, driver):
    seviaritiy_roll = random.randint(0, 100)
    if seviaritiy_roll > 60:
        return "low", None
    if 60 < seviaritiy_roll > 90:
        return "medium", None
    if 90 < seviaritiy_roll > 100:
        return "major", None
    with open('Data/carpart_data.json') as f:
        data = json.load(f)
    failures = data['failures']

    # Calculate total occurrences of all failures
    total_occurrences = sum(f['reported_occurrences'] for f in failures)

    # Generate a random number between 0 and total_occurrences
    rand_num = random.randint(0, total_occurrences)

    # Determine which failure category the random number falls into
    cumulative = 0
    for failure in failures:
        cumulative += failure['reported_occurrences']
        if rand_num <= cumulative:
            # If the failure category matches a car part, return the failure category and the failed part
            if failure['category'].lower() in data:
                print(f"Driver {driver.name} had a failure in part: {failure['part']}")
                return failure['category'], failure['part']
            break
    return None, None

    # If no matching failure category was found, the car passed the reliability check
    return True

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
    if random.randint(0, 100) > car.reliability:
        reliability_check(car, car.driver)
    if mode == 'normal':
        lap_time = base_time - (car.power * power_factor) - (car.handling * handling_factor) - (
                car.downforce * downforce_factor) + (tyre_wear_factor + fuel_load_factor)
        lap_time *= unpredictability_factor  # Apply unpredictability
    elif mode == 'qualifying':
        lap_time = base_time - (car.power * power_factor) - (car.handling * handling_factor) - (
                car.downforce * downforce_factor) + (tyre_wear_factor + fuel_load_factor)

    return round(lap_time, 3)
