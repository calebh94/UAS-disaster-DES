# Location of all Entities and the states
import numpy.random as random

# from EventHandlers import Event, FEL


class Event:
    def __init__(self, id, type, time):
        self.id = id
        self.type = type
        self.time = time
        # self.end = end


class SimDES:
    ### CORE ###
    def __init__(self, num_uas, num_buildings, level, maxtime):

        # init variables
        self.clock = 0.0
        self.uas_arr = []
        self.building_arr = []
        self.maxtime = maxtime
        # need to initialize arrays of entities
        for i in range(1, num_uas):
            name = "uas_{}".format(i)
            uas = self.UAS(name, 'rescue', level)
            self.uas_arr.append(uas)
        for j in range(1,num_buildings):
            size = 100 # change to distirbution from data
            loc = random.uniform(1000, 25000)
            bld = self.Structure(size, loc)
            self.building_arr.append(bld)
            #   need to organize buildign array into  a Priority Queue to go to closest first

        self.fel = self.FEL()

        test_event = Event("test_event", 0, 27)
        self.fel.insert(test_event)

    def run(self):
        while (self.clock <= self.maxtime):
            print("Simulation time: {} min".format(self.clock))
            self.advance_time()

    def advance_time(self):
        # check FEL for next event (if more than 15 min then jump 15 and check conditions)
        if (self.fel.isEmpty() is False and self.fel.queue[0].time <= self.clock+15):
            event = self.fel.process()
            self.eventHandler(event)
        else:
            self.clock = self.clock + 15
            self.update_entities()

    def schedule_event(self, events):
        if len(events) == 0:
            print("no events in list, simulation will continue")
        else:
            for event in events:
                self.fel.insert(event)
                print("added event %s to future event list".format(event.id))
        pass

    def update_entities(self):
        pass
        # define parameter updates when events are far out (fuel use, structure health reduction)

    ### DES STRUCTURES ###

    # class Event:
    #     def __init__(self, id, type, time):
    #         self.id = id
    #         self.type = type
    #         self.time = time
    #         # self.end = end

    def eventHandler(self, event):
        if event.type == 0:  # default example event
            print("This is a test event!")
            self.clock = event.time

        else:
            print("No event of this type exists...skipping!")

    class FEL:

        def __init__(self):
            self.queue = []

        def print(self):
            printlist = []
            for item in self.queue:
                printlist.append((item.id, item.time))
            print(printlist)

        def isEmpty(self):
            if len(self.queue) == 0:
                return True
            else:
                return False

        def insert(self, event):
            self.queue.append(event)
            self.sort()

        def sort(self):
            self.queue.sort(key=lambda item: item.time)

        def delete(self, id=None):
            if id is None:
                # delete first item
                self.queue.pop(0)
            else:
                ind = 0
                for item in self.queue:
                    if item.id == id:
                        self.queue.pop(ind)
                        return 0
                    ind = ind + 1
                print("WARNING: ID given to delete function, but ID not found in queue")

        def process(self):
            return self.queue.pop(0)

    ### ENTITIES ###

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
            event = Event(str(self.name + "_search"), "search", now, now + distance / self.speed)
            return event
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


if __name__ == "__main__":
    s = SimDES(2, 3, 1, 100)
    s.run()









