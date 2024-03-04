import random
import json

def simulate_race(track, teams, num_laps, mode='race'):
    results = {}
    lap_times = {}  # Store the lap times separately
    for _ in range(num_laps):
        for team_name, team in teams.items():
            car = team.car
            driver_name = str(team.driver)  # Convert the driver to a string
            lap_time = calculate_lap_time(car, track)
            if random.uniform(0, 100) > car.reliability:
                time_penalty, failed_part = check_reliability(car)
                print(f"{driver_name} lost {time_penalty} seconds due to a {failed_part} failure.")
            results[(team_name, driver_name)] = results.get((team_name, driver_name), 0) + lap_time
            lap_times[(team_name, driver_name)] = lap_time  # Store the lap time

            # Increase tire wear and fuel load after each lap
            car.tyre_wear += 1
            car.fuel_load -= 1

        sorted_results = sorted(lap_times.items(), key=lambda x: x[1])  # Sort the lap times

        # Print the results after each lap
        print(f"After lap {_ + 1}:")
        for i, ((team_name, driver_name), time) in enumerate(sorted_results):
            if mode == 'debug':
                print(f"{i + 1}. Team: {team_name}, Driver: {driver_name}, Lap Time: {round(time, 2)}, Interval: {round(interval, 2)}, Fuel: {car.fuel_load}, Tyre Wear: {car.tyre_wear}, Grip: {car.grip}")
            else:
                if i == 0:
                    print(f"{i + 1}. Team: {team_name}, Driver: {driver_name}, Lap Time: {round(time, 2)}")
                else:
                    interval = time - sorted_results[i - 1][1]
                    print(f"{i + 1}. Team: {team_name}, Driver: {driver_name}, Lap Time: {round(time, 2)}, Interval: {round(interval, 2)}")

    return sorted(results.items(), key=lambda x: x[1])  # Return the cumulative results

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
            return time_penalty, part['category']
    print(f"{car.driver} is still running smoothly.")
    return 0, None