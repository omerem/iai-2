import numpy as np
from Vertex import Vertex


class Edge:
    def __init__(self, vertex1=None, vertex2=None, weight=None, key=None,
                 to_copy=False, old_edge=None, new_vertices=None):
        if not to_copy:
            self.vertex1 = Vertex.minimum(vertex1, vertex2)
            self.vertex2 = Vertex.maximum(vertex1, vertex2)
            self.weight = weight
            self.blocked = False
            self.key = key
        else:
            self.vertex1 = Vertex.get_vertex(new_vertices, old_edge.vertex1.key)
            self.vertex2 = Vertex.get_vertex(new_vertices, old_edge.vertex2.key)
            self.weight = old_edge.weight
            self.blocked = old_edge.blocked
            self.key = old_edge.key

    def copyEdges(new_vertices, old_edges_list):
        new_edges = []
        for old_edge in old_edges_list:
            new_edges.append(Edge(to_copy=True, old_edge=old_edge, new_vertices=new_vertices))
        return new_edges



    def get_key(self):
        return self.key

    def occurs_in_vertex_key(self, vertex_number):
        return self.vertex1.key == vertex_number or self.vertex2.key == vertex_number

    def occurs_in_vertices_keys(self, v1, v2):
        return self.vertex1.key == np.minimum(v1, v2) and self.vertex2.key == np.maximum(v1, v2)

    def occurs_in_vertex_element(self, vertex_element):
        return self.vertex1.key == vertex_element.key or self.vertex2.key == vertex_element.key

    def occurs_in_vertices_elements(self, v1, v2):
        return self.vertex1.key == Vertex.minimum(v1, v2).key and self.vertex2.key == Vertex.maximum(v1, v2).key

    def get_other_end(self, vertex):
        if self.vertex1.key == vertex.key:
            return self.vertex2
        if self.vertex2.key == vertex.key:
            return self.vertex1

    def is_same_edge(self, edge2):
        if not self.vertex1.is_same_vertex(edge2.vertex1): return False
        if not self.vertex2.is_same_vertex(edge2.vertex2): return False
        if self.weight != edge2.weight: return False
        if self.blocked != edge2.blocked: return False
        if self.key != edge2.key: return False
        return True

    def to_print(self):
        pr = "W{}: ({}, {}) weight {}".format(self.key, self.vertex1.key, self.vertex2.key, self.weight)
        if self.blocked:
            pr += " (BLOCKED)"
        return pr
