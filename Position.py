from Vertex import Vertex
from Color import COLOR


class Position:
    def __init__(self, graph, vertex_number = None,
                 to_copy = False, old_position=None):
        if not to_copy:
            self.graph = graph
            start_vertex = graph.get_vertex(vertex_number)
            self.start = start_vertex
            self.end = self.start
            self.distance_to_destination = 0
        else:
            self.graph = graph
            start_vertex = graph.get_vertex(old_position.start.key)
            self.start = start_vertex
            self.end = graph.get_vertex(old_position.end.key)
            self.distance_to_destination = old_position.distance_to_destination

    def is_same_position(self, position2):
        if not Vertex.is_same_vertex(self.start, position2.start):
            return False
        if not Vertex.is_same_vertex(self.end, position2.end):
            return False
        if self.distance_to_destination != position2.distance_to_destination:
            return False
        return True

    def in_vertex(self):
        return self.distance_to_destination == 0

    def position_move(self, graph=None, destination=None):
        if not self.in_vertex():
            self.distance_to_destination -= 1
            if self.distance_to_destination == 0:
                self.start = self.end
#                self.end = None
            return
        self.end = destination
        self.distance_to_destination = graph.find_distance(self.start, self.end)
        self.distance_to_destination -= 1
        if self.distance_to_destination == 0:
            self.start = self.end
#            self.end = None

    def to_print(self, color_name):
        if self.in_vertex():
            return COLOR[color_name]+COLOR['BOLD']+"vertex: "+str(self.start.key)+COLOR['END']
        return "From {} to {}. Distance to destination: {}".format(self.start.key, self.end.key,
                                                                   self.distance_to_destination)
