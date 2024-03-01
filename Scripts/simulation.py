import random
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