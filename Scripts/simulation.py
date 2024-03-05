import random
import json
from .models import Tyre
from .data import format_lap_time

def simulate_race(track, teams, num_laps, tyre_data, mode='debug'):
    results = {}
    lap_times = {}  

    for lap in range(num_laps):
        for team_name, team in teams.items():
            car = team.car
            driver_name = str(team.driver)
            car.tyre.update_grip_and_life()  
            additional_time_due_to_wear = car.tyre.calculate_effect_on_lap_time()  
            
            # Check for pit stop
            tyre_life_remaining = car.tyre.tyre_life
            if tyre_life_remaining <= 15 and (tyre_life_remaining == 1 or random.random() < 0.1):
                pit_time = pit_stop(car, tyre_data)
                print(f"{driver_name} making a pit stop, losing {pit_time} seconds.")
                additional_time_due_to_wear += pit_time
            
            individual_lap_time = calculate_segments(track, car)+ additional_time_due_to_wear
              
            if random.uniform(0, 80) > car.reliability:
                time_penalty, failed_part = check_reliability(car)
                print(f"{driver_name} lost {time_penalty} seconds due to a {failed_part} failure.")
                individual_lap_time += time_penalty  
            results[(team_name, driver_name)] = results.get((team_name, driver_name), 0) + individual_lap_time
            lap_times[(team_name, driver_name, lap)] = individual_lap_time  

            car.fuel_load -= 1  

        sorted_results = sorted(results.items(), key=lambda x: x[1])
        print(f"After lap {lap + 1}:")
        for i, ((team_name, driver_name), total_time) in enumerate(sorted_results):
            interval = total_time - sorted_results[0][1] if i != 0 else 0
            if mode == 'debug':
                print(f"{i + 1}. Team: {team_name}, Driver: {driver_name}, Lap Time: {format_lap_time(lap_times[(team_name, driver_name, lap)])}, Total Time: {format_lap_time(total_time)} (+{format_lap_time(interval)}), Grip: {round(teams[team_name].car.tyre.grip, 2)}, Tyre Life: {teams[team_name].car.tyre.tyre_life}, Compound: {teams[team_name].car.tyre.compound}, Fuel load: {teams[team_name].car.fuel_load}")
            else:
                print(f"{i + 1}. Team: {team_name}, Driver: {driver_name}, Lap Time: {format_lap_time(lap_times[(team_name, driver_name, lap)], 2)}, Total Time: {round(total_time, 2)} (+{round(interval, 2)})")

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

def pit_stop(car, tyre_data):
    pit_lane_time = 20  # Fixed time for entering and exiting the pit lane
    pit_stop_duration = random.randint(2, 5)  # Random time for tyre replacement
    total_pit_time = pit_lane_time + pit_stop_duration  # Total time spent in pit

    # Identify the tyre's constructor prefix ('C' for Pirelli, 'K' for Bridgestone)
    constructor_prefix = car.tyre.compound[0]

    # Filter tyre choices that match the constructor and are not the current compound
    compatible_tyres = [tyre for tyre in tyre_data['tyres'] if tyre['compound'].startswith(constructor_prefix) and tyre['compound'] != car.tyre.compound]

    # Randomly select a new tyre from the compatible options
    if compatible_tyres:
        new_tyre = random.choice(compatible_tyres)
        car.tyre = Tyre(compound=new_tyre['compound'], grip=new_tyre['grip'], tyre_life=new_tyre['tyre_life'], wear_rate=new_tyre['wear_rate'])
        print(f"Pit stop for {car.driver}: Total pit time {total_pit_time} seconds, including {pit_stop_duration} seconds for tyre replacement, changed to {new_tyre['compound']} tyres.")

    return total_pit_time

def calculate_segments(track, car):
    base_time = track.base_time
    power_factor = track.power_factor
    handling_factor = track.handling_factor
    downforce_factor = track.downforce_factor
    unpredictability_factor = track.unpredictability_factor
    segments = track.segments
    segment_time = 0
    lap_time = 0  
    for segment in segments:
        if segment == "straights_km":
            segment_time = (car.power / power_factor * downforce_factor) * track.segments[segment]
            print(segment_time)
        elif segment == "high_speed_km":
            segment_time = (car.power * power_factor * downforce_factor) * ((100- car.handling) / 10 * handling_factor) * track.segments[segment] / 5
        
        elif segment == "medium_speed_km":
            segment_time = (car.handling / handling_factor) / 2 * (car.downforce / downforce_factor)* 2 * track.segments[segment] / 5
        
        elif segment == "low_speed_km":
            segment_time = (car.handling / handling_factor) * (car.downforce / downforce_factor) * track.segments[segment] / 5

    # Add the segment time to the total lap time
    lap_time += segment_time

    # Return the total lap time
    return lap_time