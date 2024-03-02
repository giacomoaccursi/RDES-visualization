class Node: 
    def __init__(self, id, neighbors, events): 
        self.id = id
        #self.position = position
        self.neighbors = neighbors
        self.events = events

class Event: 
    def __init__(self, id, node, dependencies):
        self.id = id
        self.node = node
        self.dependencies = dependencies

class ScheduledEvent: 
    def __init__(self, id, time):
         self.id = id
         self.time = time