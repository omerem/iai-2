class Vertex:
    def __init__(self, key, number_of_people):
        self.key = key
        self.number_of_people = number_of_people

    def set_number_of_people(self, number_of_people_in):
        self.number_of_people = number_of_people_in

    def get_key(self):
        return self.key

    def minimum(vertex1, vertex2):
        if vertex1.key <= vertex2.key:
            return vertex1
        return vertex2

    def maximum (vertex1, vertex2):
        if vertex1.key >= vertex2.key:
            return vertex1
        return vertex2

    def get_vertex(vertices, key):
        for vertex in vertices:
            if vertex.key == key:
                return vertex
        print("No vertex found")
        return None

    def is_same_vertex(self, vertex2):
        if self == vertex2: return True
        if self == None and vertex2 != None: return False
        if self != None and vertex2 == None: return False
        if self.key != vertex2.key or self.number_of_people != vertex2.number_of_people:
            return False
        return True

    def to_print(self):
        return "{0}, ({1} people)".format(self.key, self.number_of_people)
