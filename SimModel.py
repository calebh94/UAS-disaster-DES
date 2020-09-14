# Location of all Entities and the states
import numpy.random as random

from EventHandlers import Event

class UAS:
    # Simplify and make them all Searching UAS
    def __init__(self, name, type, level):
        self.mode = "waiting"
        self.name = name
        self.type = type
        self.level = level
        if self.level == 1:
            self.speed = 20
            self.fueltime = 10.0
            self.skill = 0.8
        elif self.level == 2:
            self.speed = 30
            self.skill = 1.0
            self.fueltime = 12.0
        elif self.level == 3:
            self.speed = 50
            self.skill = 1.2
            self.fueltime = 13.5
        else:
            raise ValueError("UAS Level must be 1,2, or 3")

    def search(self, now, distance):
        self.mode = "searching"
        return Event(str(self.name + "_search"), "search", now, now + distance / self.speed)
    #
    # def find(self):
    #     # Weibull dist (https://numpy.org/doc/stable/reference/random/generated/numpy.random.weibull.html)
    #

class Structure:

    def __init__(self, size, location):
        self.size = size
        self.location = location
        self.health = 100
        self.secured = False

    def locate(self):
        self.secured = True

    def fail(self):
        self.health = self.health - 0.1








