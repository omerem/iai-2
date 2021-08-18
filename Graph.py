from Vertex import Vertex
from Edge import Edge
from copy import deepcopy


class Graph:
    def __init__(self, vertices=[], edges=[], to_copy=False, old_graph=None):
        if not to_copy:
            self.vertices = vertices
            self.vertices.sort(key=Vertex.get_key)
            self.edges = edges
            self.edges.sort(key=Vertex.get_key)
            self.blocked_edges = []
        else:
            self.vertices = deepcopy(old_graph.vertices)
            self.edges = Edge.copyEdges(self.vertices, old_graph.edges)
            self.blocked_edges = Edge.copyEdges(self.vertices, old_graph.blocked_edges)

    def is_same_graph(self, graph2):
        vertices2 = graph2.vertices
        edges2 = graph2.edges
        blocked_edges2 = graph2.blocked_edges
        if len(self.vertices) != len(vertices2): return False
        if len(self.edges) != len(edges2): return False
        if len(self.blocked_edges) != len(blocked_edges2): return False
        for i in range(len(self.vertices)):
            if not Vertex.is_same_vertex(self.vertices[i], vertices2[i]): return False
        for i in range(len(self.edges)):
            if not Edge.is_same_edge(self.edges[i], edges2[i]): return False
        for i in range(len(self.blocked_edges)):
            if not Edge.is_same_edge(self.blocked_edges[i], blocked_edges2[i]): return False
        return True

    def input_from_text(self, file):
        pass

    def has_vertex(self, vertex):
        return vertex in self.vertices

    def are_connected(self, v1, v2):
        for edge in self.edges:
            if edge.occurs_in_vertices_keys(v1, v2):
                return True
            return False

    def to_print(self, with_unblocked_edges):
        pr = "Vertices:\n"
        for vertex in self.vertices:
            pr += "\t" + vertex.to_print() + "\n"
        if with_unblocked_edges:
            pr += "Edges:\n"
            for e in self.edges:
                pr += "\t" + e.to_print() + "\n"
        for e in self.blocked_edges:
            pr += "\t" + e.to_print() + "\n"
        return pr

    def get_vertex(self, vertex_number):
        for vertex in self.vertices:
            if vertex.key == vertex_number:
                return vertex
        print("No vertex found.")
        return None

    def find_distance(self, vertex1, vertex2):
        for edge in self.edges:
            if edge.occurs_in_vertices_elements(vertex1, vertex2):
                return edge.weight

    def neighbours_of(self, vertex):
        neighbours = []
        for edge in self.edges:
            if edge.occurs_in_vertex_element(vertex):
                neighbours.append(edge.get_other_end(vertex))
        return neighbours

    def Dijkstra(self, start, end):
        length = len(self.vertices)
        visited = [False] * length
        dist = [float("inf")] * length
        prev = [None] * length
        dist[self.vertices.index(start)] = 0
        while not all(visited):
            v_idx = min([i for i, x in enumerate(visited) if not x], key=dist.__getitem__)

            v = self.vertices[v_idx]
            if v == end:
                break
            if dist[v_idx] == float("inf"):  # there is no path from start to end
                return None
            visited[v_idx] = True
            neighbours = self.neighbours_of(v)
            for neighbour in neighbours:
                neig_idx = self.vertices.index(neighbour)
                if visited[neig_idx]:
                    continue
                alt = dist[v_idx] + self.find_distance(v, neighbour)
                if alt < dist[neig_idx]:
                    dist[neig_idx] = alt
                    prev[neig_idx] = v
        path = [end]
        vertex = end
        while vertex != start:
            ancestor = prev[self.vertices.index(vertex)]
            path = [ancestor] + path
            vertex = ancestor
        return path

    def get_adjacent_edges(self, vertex):
        adjacent_edges = []
        for edge in self.edges:
            if edge.occurs_in_vertex_element(vertex):
                adjacent_edges.append(edge)
        return adjacent_edges

    def block(self, edge):
        self.edges.remove(edge)
        self.blocked_edges.append(edge)
        edge.blocked = True
        self.blocked_edges.sort(key=Vertex.get_key)

    def more_people(self):
        for vertex in self.vertices:
            if vertex.number_of_people > 0: return True
        return False










