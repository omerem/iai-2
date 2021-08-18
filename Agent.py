from Position import Position

class Agent:
    def __init__(self, observations=None, vertex_position=None, key=None,
                 to_copy=False, old_agent=None, graph=None): # observations = [graph]
        if not to_copy:
            self.actions_counter = 0
            self.score = 0
            self.is_terminated = False
            self.graph = observations[0]
            self.position = Position(self.graph, vertex_position)
            self.in_calculation = False

            self.score += self.position.start.number_of_people
            self.position.start.number_of_people = 0
            self.key = key
        else:
            self.actions_counter = old_agent.actions_counter
            self.score = old_agent.score
            self.is_terminated = old_agent.is_terminated
            self.graph = graph
            self.in_calculation = old_agent.in_calculation
            self.position = Position(graph,to_copy=True, old_position=old_agent.position)
            self.key = old_agent.key

    def terminate(self):
        self.is_terminated = True

    def agent_in_vertex(self):
        if self.position.in_vertex():
            self.score += self.position.start.number_of_people
            self.position.start.number_of_people = 0

    def agent_move(self, destination=None):
        self.actions_counter += 1
        self.agent_in_vertex()
        if not self.position.in_vertex():
            self.position.position_move()
        else:
            self.position.position_move(self.graph, destination)
        self.agent_in_vertex()

    def agent_terminate(self):
        self.is_terminated = True

    def agent_block(self, edge):
        self.graph.block(edge)
        self.actions_counter += 1

    def to_print(self, color_name):
        pr = ""
        # pr += type(self).__name__ + "\n"
        # pr += "actions_counter: " + str(self.actions_counter) + "\n"
        pr += "score: " + str(self.score) + "\n"
        # pr += "is_terminated: " + str(self.is_terminated) + "\n"
        pr += "position:\n"
        poistion_str = self.position.to_print(color_name)
        lines = poistion_str.splitlines()
        for i, line in enumerate(lines):
            pr += "\t" + line
        pr += "\nIn a calculation: {}".format(self.in_calculation)
        return pr