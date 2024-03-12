import random
import json
from .models import Tyre
from .data import format_lap_time


def simulate_race(track, teams, num_laps, tyre_data, ers, mode='debug'):
    results = {}
    lap_times = {}

    for lap in range(num_laps):
        for team_name, team in teams.items():
            car = team.car
            driver_name = str(team.driver)
            driver = team.driver
            additional_time_due_to_wear = car.tyre.calculate_effect_on_lap_time()

            # Check for pit stop
            tyre_life_remaining = car.tyre.tyre_life
            if tyre_life_remaining <= 15 and (tyre_life_remaining == 1 or random.random() < 0.1):
                pit_time = pit_stop(car, tyre_data)
                print(f"{driver_name} making a pit stop, losing {pit_time} seconds.")
                additional_time_due_to_wear += pit_time

            individual_lap_time = calculate_lap_time(track, car, ers=ers, driver=driver) + additional_time_due_to_wear

            if random.uniform(0, 80) > car.reliability:
                time_penalty, failed_part = check_reliability(car)
                print(f"{driver_name} lost {time_penalty} seconds due to a {failed_part} failure.")
                individual_lap_time += time_penalty
            results[(team_name, driver_name)] = results.get((team_name, driver_name), 0) + individual_lap_time
            lap_times[(team_name, driver_name, lap)] = individual_lap_time

            car.fuel_load -= 1
            car.tyre.tyre_life -= 2

        sorted_results = sorted(results.items(), key=lambda x: x[1])
        print(f"After lap {lap + 1}:")
        for i, ((team_name, driver_name), total_time) in enumerate(sorted_results):
            interval = total_time - sorted_results[0][1] if i != 0 else 0
            if mode == 'debug':
                print(
                    f"{i + 1}. Team: {team_name}, Driver: {driver_name}, Lap Time: {format_lap_time(lap_times[(team_name, driver_name, lap)])}, Total Time: {format_lap_time(total_time)} (+{format_lap_time(interval)}), Grip: {round(teams[team_name].car.tyre.grip, 2)}, Tyre Life: {teams[team_name].car.tyre.tyre_life}, Compound: {teams[team_name].car.tyre.compound}, Fuel load: {teams[team_name].car.fuel_load}")
            else:
                print(
                    f"{i + 1}. Team: {team_name}, Driver: {driver_name}, Lap Time: {format_lap_time(lap_times[(team_name, driver_name, lap)])}, Total Time: {round(total_time, 2)} (+{round(interval, 2)})")

    if team_name in results:
        next_car_time = next((time for team, time in results.items() if time > results[team_name]), None)
        if next_car_time is not None:
            car.distance_to_next_car = next_car_time - results[team_name]
    car.drs_active = car.distance_to_next_car is not None and car.distance_to_next_car < 1
    return sorted(results.items(), key=lambda x: x[1])  # Return the cumulative results


def check_reliability(car):
    with open('Data/carpart_data.json') as f:
        carpart_data = json.load(f)
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


def pit_stop(car, tyre_data):
    pit_lane_time = 20  # Fixed time for entering and exiting the pit lane
    pit_stop_duration = random.randint(2, 5)  # Random time for tyre replacement
    total_pit_time = pit_lane_time + pit_stop_duration  # Total time spent in pit

    # Identify the tyre's constructor prefix ('C' for Pirelli, 'K' for Bridgestone)
    constructor_prefix = car.tyre.compound[0]

    # Filter tyre choices that match the constructor and are not the current compound
    compatible_tyres = [tyre for tyre in tyre_data['tyres'] if
                        tyre['compound'].startswith(constructor_prefix) and tyre['compound'] != car.tyre.compound]

    # Randomly select a new tyre from the compatible options
    if compatible_tyres:
        new_tyre = random.choice(compatible_tyres)
        car.tyre = Tyre(compound=new_tyre['compound'], grip=new_tyre['grip'], tyre_life=new_tyre['tyre_life'],
                        wear_rate=new_tyre['wear_rate'])
        print(
            f"Pit stop for {car.driver}: Total pit time {total_pit_time} seconds, including {pit_stop_duration} seconds for tyre replacement, changed to {new_tyre['compound']} tyres.")

    return total_pit_time


def calculate_lap_time(track, car, ers, driver):
    lap_time = 0
    attribute_factors = {
        "straights_km": car.power * 0.5 * (car.drs_factor if car.drs_active else 1) - car.downforce * 0.3 + driver.breaking * 0.2,
        "high_speed_km": car.power * 0.3 + car.handling * 0.4 + car.downforce * 0.3 + driver.cornering * 0.2,
        "medium_speed_km": car.handling * 0.5 + car.downforce * 0.4 + driver.cornering * 0.4 + driver.adaptability * 0.2,
        "low_speed_km": car.downforce * 0.6 + car.handling * 0.4 + driver.cornering * 0.5,
    }

    for segment, attribute in attribute_factors.items():
        if segment in track.segments:
            # Determine the ERS mode for the segment
            if segment == "straights_km":
                ers_mode = "PUSH"
            elif segment == "high_speed_km":
                ers_mode = "NATURAL"
            else:
                ers_mode = "RECHARGE"

            # Use the ERS
            ers_multiplier = 1 + (ers.battery_level / 100) * 0.1  # Adjust this value as needed
            car.use_ers(ers_mode, segment)

            # Calculate the segment time
            base_time = track.segments[segment] * 1.5  # Increase the base time for each segment
            segment_time = base_time * (attribute / 100) * ers_multiplier
            segment_time *= 1 + track.unpredictability_factor / 50

            # Add a random factor to represent the natural variability in a driver's performance
            random_factor = random.gauss(0, 0.03)  # Adjust this range as needed
            segment_time *= 1 + random_factor

            lap_time += segment_time
            lap_time *= 1 + (driver.consistency * 0.001)
    return lap_time
