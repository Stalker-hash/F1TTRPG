# Classes that will be used to create the simulation,

class Team:
    def __init__(self, name, driver, state = 0, car=None, cars=[]):
        self.name = name
        self.driver = driver
        self.state = state
        self.cars = cars
        self.car = car


class Car():
    def __init__(self, car_name, handling, power, downforce, ):
        self.car_name = car_name
        self.handling = handling
        self.power = power
        self.downforce = downforce


class Driver():
    def __init__(self, car, driver_name, driver_number):
        self.name = driver_name
        self.car = car
        self.number = driver_number


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