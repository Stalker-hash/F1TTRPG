# Classes that will be used to create the simulation,

class Team:
    def __init__(self, name, driver, state = 0, car=None, cars=[]):
        self.name = name
        self.driver = driver
        self.state = state
        self.cars = cars
        self.car = car
        
    def __str__(self):
        return self.name
    
    def pit_stop(self, new_Tyre):
        # Change the car's Tyres
        self.car.change_Tyres(new_Tyre)


class Car():
    def __init__(self, car_name, handling, power, downforce, tyre_wear, fuel_load, tyres="C4" ):
        self.car_name = car_name
        self.handling = handling
        self.power = power
        self.downforce = downforce
        self.tyre_wear = tyre_wear
        self.fuel_load = fuel_load
        self.tyres = tyres
        
    def __str__(self):
        return self.car_name
    
    def change_Tyres(self, new_tyre):
        # Remove the current Tyre from the list of Tyres
        self.Tyres.remove(self.current_Tyre)

        # Add the new Tyre to the list of Tyres
        self.Tyres.append(new_tyre)

        # Set the current Tyre to the new Tyre
        self.current_Tyre = new_tyre   

class Driver():
    def __init__(self, car, driver_name, driver_number):
        self.name = driver_name
        self.car = car
        self.number = driver_number
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
    def __init__(self, name, grip, durability, compound, wear_rate):
        self.name = name
        self.grip = grip
        self.durability = durability
        self.compound = compound
        self.wear_rate = wear_rate

    def __str__(self):
        return self.name