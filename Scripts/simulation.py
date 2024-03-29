import random
import json
from .models import Tyre
from .helper import format_lap_time
import time


def simulate_race(track, teams, num_laps, tyre_data, mode='debug'):
    results = {}
    positions = {}
    lap_times = {}
    race_results = []
    battle_triggered = False

    positions = simulate_qualifying(track, teams)

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

            individual_lap_time = calculate_lap_time(track, car, driver=driver) + additional_time_due_to_wear

            if random.uniform(0, 80) > car.reliability:
                time_penalty, failed_part = check_reliability(car)
                print(f"{driver_name} lost {time_penalty} seconds due to a {failed_part} failure.")
                individual_lap_time += time_penalty
            results[(team_name, driver_name)] = results.get((team_name, driver_name), 0) + individual_lap_time
            lap_times[(team_name, driver_name, lap)] = individual_lap_time

            car.fuel_load -= 1
            car.tyre.tyre_life -= 2

            # Calculate the distance to the next car and update DRS status
            next_car_time = next((time for team, time in results.items() if time > results[(team_name, driver_name)]),
                                 None)
            if next_car_time is not None:
                car.distance_to_next_car = next_car_time - results[(team_name, driver_name)]
            car.drs_active = car.distance_to_next_car is not None and car.distance_to_next_car < 1

        # Battle for position
        for team_name, team in teams.items():
            for other_team_name, other_team in teams.items():
                if team_name != other_team_name:  # A car cannot overtake itself
                    battle_triggered = battle_for_position(team, other_team, results, positions)

        # Sort the results dictionary after the overtaking logic
        results = dict(sorted(results.items(), key=lambda x: x[1]))

        # Update the positions dictionary based on the updated results only if a battle was not triggered
        if not battle_triggered:
            for i, ((team_name, driver_name), _) in enumerate(sorted(results.items(), key=lambda x: x[1])):
                positions[(team_name, driver_name)] = i + 1
        race_results.append(sorted(results.items(), key=lambda x: x[1]))  # Return the cumulative results

        print(f"After lap {lap + 1}:")
        sorted_results = sorted(results.items(), key=lambda x: x[1])
        for i, ((team_name, driver_name), total_time) in enumerate(sorted(results.items(), key=lambda x: x[1])):
            interval = total_time - sorted_results[0][1] if i != 0 else 0
            if mode == 'debug':
                print(
                    f"{i + 1}. Team: {team_name}, Driver: {driver_name}, Lap Time: {format_lap_time(lap_times[(team_name, driver_name, lap)])}, Total Time: {format_lap_time(total_time)} (+{format_lap_time(interval)}), Grip: {round(teams[team_name].car.tyre.grip, 2)}, Tyre Life: {teams[team_name].car.tyre.tyre_life}, Compound: {teams[team_name].car.tyre.compound}, Fuel load: {teams[team_name].car.fuel_load}")
            elif mode == "print":
                print(
                    f"{i + 1}. Team: {team_name}, Driver: {driver_name}, Lap Time: {format_lap_time(lap_times[(team_name, driver_name, lap)])}, Total Time: {round(total_time, 2)} (+{round(interval, 2)})")

                time.sleep(sorted_results[0][1] / 10)  # Simulate a delay in the

    if team_name in results:
        next_car_time = next((time for team, time in results.items() if time > results[team_name]), None)
        if next_car_time is not None:
            car.distance_to_next_car = next_car_time - results[team_name]
    car.drs_active = car.distance_to_next_car is not None and car.distance_to_next_car < 1

    return race_results


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


def calculate_lap_time(track, car, driver):
    lap_time = 0
    attribute_factors = {
        "straights_km": car.power * 0.4 * (
            car.drs_factor if car.drs_active else 1) - car.downforce * 0.2 + driver.breaking * 0.2 ,
        "high_speed_km": car.power * 0.3 + car.handling * 0.4 + car.downforce * 0.3 + driver.cornering * 0.2,
        "medium_speed_km": car.handling * 0.5 + car.downforce * 0.4 + driver.cornering * 0.4 + driver.adaptability * 0.2,
        "low_speed_km": car.downforce * 0.5 + car.handling * 0.3 + driver.cornering * 0.4,
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
            ers_multiplier = 1 + (car.battery_level / 100) * 0.1  # Adjust this value as needed
            car.use_ers(ers_mode, segment)

            # Calculate the segment time
            base_time = track.segments[segment] * 3  # Increase the base time for each segment
            normalized_attribute = attribute / 220  # Normalize the attribute value to a range between 0 and 1
            segment_time = base_time * (1 - normalized_attribute) * ers_multiplier
            segment_time *= 1 + track.unpredictability_factor / 50

            # Add a random factor to represent the natural variability in a driver's performance
            random_factor = random.gauss(0, 0.01)  # Adjust this range as needed
            segment_time *= 1 + random_factor

            lap_time += segment_time
            lap_time *= 1 - (driver.consistency * 0.0001)
    return round(lap_time, 6)


def battle_for_position(team1, team2, results, positions):
    # Prevent the first car from overtaking the last car
    if positions[(team1.name, str(team1.driver))] == 1 and positions[(team2.name, str(team2.driver))] == len(positions):
        return

    # Ensure that team1 is behind team2 and the total time of team1 is less than or equal to the total time of team2
    if positions[(team1.name, str(team1.driver))] > positions[(team2.name, str(team2.driver))] and results[
        (team1.name, str(team1.driver))] <= results[(team2.name, str(team2.driver))]:
        time_difference = abs(results[(team1.name, str(team1.driver))] - results[(team2.name, str(team2.driver))])
        if time_difference <= 1:  # A car can only overtake if it's within a 1-second window
            overtaking_probability = round((team1.car.power + team1.car.handling + team1.driver.overtaking +
                                            team1.car.drs_factor) / 300, 2)  # Normalize to a value between 0 and 1
            overtaking_probability += round(random.uniform(-0.05, 0.05), 3)  # Add a random factor
            team2_defence = team2.driver.defence_probability + round(random.uniform(-0.05, 0.05), 3) # Add a random factor
            print(f"Overtaking probability: {round(overtaking_probability, 4)}")
            print(f"Defence probability: {round(team2_defence, 3)}")
            if team2_defence< overtaking_probability:  # If the overtaking car is successful
                # Only allow team1 to overtake team2 if their total time is less than team2's total time
                if results[(team1.name, str(team1.driver))] < results[(team2.name, str(team2.driver))]:
                    positions[(team1.name, str(team1.driver))], positions[(team2.name, str(team2.driver))] = positions[
                        (team2.name, str(team2.driver))], positions[(team1.name, str(team1.driver))]
                    print(f"{team1.driver} has overtaken {team2.driver}!")
                    return True  # Return True if a battle was triggered and team1 overtook team2
    return False  # Return False if a battle was not triggered or team1 did not overtake team2


def simulate_qualifying(track, teams):
    qualifying_parts = ['Q1', 'Q2', 'Q3']
    eliminated_per_part = 5
    results = {}
    positions = {}

    for part in qualifying_parts:
        for team_name, team in teams.items():
            best_lap_time = float('inf')

            for _ in range(3):  # Each driver can make 3 laps
                lap_time = calculate_lap_time(track, team.car, team.driver)
                best_lap_time = min(best_lap_time, lap_time)

            results[(team_name, str(team.driver))] = best_lap_time

        # Sort the results dictionary by lap time
        results = dict(sorted(results.items(), key=lambda x: x[1]))

        # Update the positions dictionary based on the sorted results
        for i, ((team_name, driver_name), _) in enumerate(results.items()):
            positions[(team_name, driver_name)] = i + 1

        # Print the qualifying results
        print(f"{part} results:")
        for i, ((team_name, driver_name), lap_time) in enumerate(results.items()):
            print(f"{i + 1}. Team: {team_name}, Driver: {driver_name}, Best Lap Time: {format_lap_time(lap_time)}")

        # Eliminate the slowest 5 teams only if there are more than 5 teams
        if len(teams) > eliminated_per_part:
            eliminated_teams = list(results.keys())[-eliminated_per_part:]
            for team in eliminated_teams:
                del results[team]
                del teams[team[0]]
                del positions[team]  # Also remove the team from the positions dictionary

    return positions

