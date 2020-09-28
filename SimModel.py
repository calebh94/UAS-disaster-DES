# Location of all Entities and the states
import numpy.random as random


class SimDES:
    def __init__(self, num_uas, num_buildings, level, maxtime):
        self.num_uas = num_uas
        self.num_buildings = num_buildings
        # init variables
        self.clock = 0.0
        self.uas_arr = []
        self.building_arr = []
        self.maxtime = maxtime
        self.jobs_arr = []
        for i in range(0, num_uas):
            name = "uas_{}".format(i)
            uas = self.UAS(name, 'rescue', level)
            self.uas_arr.append(uas)

        for j in range(0,num_buildings):
            size = 100 # change to distirbution from data
            loc = random.uniform(200, 300)
            bld = self.Structure(size, loc)
            self.building_arr.append(bld)

        self.fel = self.FEL()

        # Objective variables
        self.successes = 0
        self.searches = 0


    def run(self):
        #TODO: init task
        #TODO: sort building queue
        while (self.clock <= self.maxtime):
            print("Simulation time: {} min".format(self.clock))
            events = []
            # Managing events from entity queues:
            for struct in self.building_arr:
                for uas in self.uas_arr:
                    newevent = self.schedule_search(self.clock, struct.distance, uas)
                    self.building_arr.remove(struct)
                    self.uas_arr.remove(uas)
                    self.jobs_arr.append([uas, struct])
                    events.append(newevent)

            self.schedule_event(events)
            self.advance_time()

        print("Successful Rescues: {}".format(self.successes))
        print("Required search jobs {}".format(self.searches))
        print("Total structures for mission {}".format(self.num_buildings))

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
                print("added event {} to future event list".format(event.id))
        pass

    def update_entities(self):
        pass
        # define parameter updates when events are far out (fuel use, structure health reduction)

    ### DES STRUCTURES ###

    class Event:
        def __init__(self, id, type, time):
            self.id = id
            self.type = type
            self.time = time

    def eventHandler(self, event):
        if event.type == 0:  # default example event
            print("This is a test event!")
            self.clock = event.time
        elif event.type == "search":
            print("processing search event {}".format(event.id))
            # doing process
            self.clock = event.time
            newevent = self.schedule_rescue(self.clock, self.jobs_arr[0][1].distance, self.jobs_arr[0][0])
            self.schedule_event([newevent])
            self.searches = self.searches + 1
        elif event.type == "rescued":
            print("processing rescued event {}".format(event.id))
            self.clock = event.time
            #TODO: determine actual biulding rescued
            uas, struct = self.jobs_arr.pop(0)
            self.uas_arr.append(uas)
            self.successes = self.successes + 1
            # newevent = self.schedule_complete(self.clock, self.jobs_arr[0][0])
            # self.schedule_event([newevent])
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
            self.searchtime = 20 + random.normal(0.0, 0.5)
            if self.level == 1:
                self.speed = 20 + random.normal(0, 0.1)
                self.fueltime = 10.0
                self.skill = 0.8
            elif self.level == 2:
                self.speed = 30 + random.normal(0, 0.3)
                self.skill = 1.0
                self.fueltime = 12.0
            elif self.level == 3:
                self.speed = 50 + random.normal(0, 1.0)
                self.skill = 1.2
                self.fueltime = 13.5
            else:
                raise ValueError("UAS Level must be 1,2, or 3")

    def schedule_search(self, now, distance, uas):
        uas.mode = "searching"
        event = SimDES.Event(str(uas.name + "_search"), "search", now + distance / uas.speed + uas.searchtime)
        return event

    def schedule_rescue(self, now, distance, uas):
        # Weibull dist (https://numpy.org/doc/stable/reference/random/generated/numpy.random.weibull.html)
        r = random.uniform(0,1)
        found = False
        if r > 0.5:
            uas.mode = "returning"
            event = SimDES.Event(str(uas.name + "_rescued"), "rescued", now + distance / uas.speed)
            found = True
        else:
            uas.mode = "searching"
            event = SimDES.Event(str(uas.name + "_search"), "search", now + uas.searchtime)

        return event

    def schedule_complete(self, now, uas):
        uas.mode = "refueling"
        event = SimDES.Event(str(uas.name + "_refuel"), "refuel", now + 10) # random refuel time
        return event

    class Structure:

        def __init__(self, size, location):
            self.size = size
            self.distance = location - 0
            self.health = 100
            self.secured = False

        def locate(self):
            self.secured = True

        def fail(self):
            self.health = self.health - 0.1


if __name__ == "__main__":
    s = SimDES(2, 3, 1, 100)
    s.run()









