# Classes that will be used to create the simulation,
import json
import random
class Team:
    def __init__(self, name, driver, state = 0, car=None, cars=[]):
        self.name = name
        self.driver = driver
        self.state = state
        self.cars = cars
        self.car = car
        
    def __str__(self):
        return self.name
    
    def pit_stop(self, new_tyre):
        pit_time, narration = self.car.perform_pit_stop()
        print(f"{narration} for {self.name}.")
        return pit_time


class Car:
    def __init__(self, car_name, handling, power, downforce, tyre_wear, fuel_load, reliability, driver, tyre):
        self.car_name = car_name
        self.handling = handling
        self.power = power
        self.downforce = downforce
        self.tyre_wear = tyre_wear
        self.fuel_load = fuel_load
        self.reliability = reliability
        self.driver = driver
        self.tyre = tyre  
        with open('Data/carpart_data.json') as f:
            self.car_parts = json.load(f)

    def __str__(self):
        return self.car_name
    

class Driver():
    def __init__(self, car, driver_name, driver_number, overtaking, breaking, consistency, adaptability, smoothness, defence, cornering):
        self.name = driver_name
        self.car = car
        self.number = driver_number
        self.overtaking = overtaking
        self.breaking  = breaking
        self.consistency = consistency
        self.adaptability = adaptability
        self.smoothness = smoothness
        self.defence = defence
        self.cornering = cornering
    def __str__(self):
        return self.name
    


class Track:
    def __init__(self, name, length, turns, downforce_factor, handling_factor, power_factor, unpredictability_factor,
                 base_time):
        self.name = name
        self.length = length
        self.turns = turns
        self.downforce_factor = downforce_factor
        self.handling_factor = handling_factor
        self.power_factor = power_factor
        self.unpredictability_factor = unpredictability_factor
        self.base_time = base_time


class Tyre:
    def __init__(self, compound, grip, durability):
        self.compound = compound  # 1 (Hard), 2 (Medium), 3 (Soft)
        self.initial_grip = grip
        self.current_grip = grip
        self.durability = durability  # Max laps tyre can last before significant performance drop
        self.wear_rate = self._calculate_wear_rate()

    def _calculate_wear_rate(self):
        if self.compound == 1:  # Hard
            return 1 / 35
        elif self.compound == 2:  # Medium
            return 1 / 25
        else:  # Soft
            return 1 / 12

    def update_grip(self):
        self.current_grip -= self.wear_rate
        if self.current_grip < 0:
            self.current_grip = 0

    def calculate_effect_on_lap_time(self):
        # Assuming grip directly correlates with lap time improvement per lap,
        # with 0.1 seconds added per lap for every 1% grip lost
        grip_loss_percentage = (self.initial_grip - self.current_grip) / self.initial_grip
        additional_time_per_lap = grip_loss_percentage * 0.1
        return additional_time_per_lap