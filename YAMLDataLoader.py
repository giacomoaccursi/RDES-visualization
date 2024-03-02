import yaml
from Model import Node, Event, ScheduledEvent

class YAMLDataLoader:
    def __init__(self, file_path):
        self.file_path = file_path
        self.data = self._load_data()
        self.time = self._get_time()
        self.step = self._get_step()
        self.nodes = self._get_nodes()
        self.events = self._get_all_events()
        self.event_list = self._get_event_list()

    def _load_data(self):
        with open(self.file_path, 'r') as stream:
            try:
                return yaml.safe_load(stream)
            except yaml.YAMLError as exc:
                print(exc)

    def _get_time(self):
        return self.data["time"]

    def _get_step(self):
        return self.data["step"]

    def _get_nodes(self):
        nodes_data = self.data["nodes"]
        neighborhoods_data = self.data.get("neighborhoods", {})
        nodes = []
        for node_id in nodes_data:  
            neighbors = neighborhoods_data.get(node_id, [])
            events = [event["id"] for event in self.data["events"] if event["node"] == node_id]
            nodes.append(Node(node_id, neighbors, events))
        return nodes
    
    def _get_all_events(self): 
        events_data = self.data["events"]
        return [Event(event["id"], event["node"], event["dependencies"]) for event in events_data]

    def _get_event_list(self):
        event_list_data = self.data["event_list"]
        return [ScheduledEvent(event["id"], event["time"]) for event in event_list_data]