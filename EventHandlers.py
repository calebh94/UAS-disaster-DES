


def testEventHandler():
    print("Inside Test Event Handler!")


class Event:
    def __init__(self, id, type, time, end):
        self.id = id
        self.type = type
        self.time = time
        self.end = end

    def eventHandler(self):
        if self.type == 0: # default example event
            print("This is a test event!")

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

#
# fel = FEL()
# event1 = Event('t1', 0, 2, 3)
# event2 = Event('t2', 0, 4, 6)
# event3 = Event('t3', 1, 1, 9)
#
# fel.insert(event1)
# fel.print()
# fel.insert(event2)
# fel.insert(event3)
# fel.print()
# fel.delete()
# fel.delete(id="t2")
# fel.print()
# eve = fel.process()
# fel.print()
# print(eve.id)
# eve.eventHandler()






