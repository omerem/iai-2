from Position import Position
from Agent import Agent
from Graph import Graph


STRATEGY_1 = 1
STRATEGY_2 = 2
STRATEGY_3 = 3


class GameTreeNode():
    def __init__(self, graph, agentA, agentB, A_turn, depth, strategy):
        self.graph = graph
        self.agentA = agentA
        self.agentB = agentB
        self.depth = depth
        self.strategy = strategy

        self.resetNode(A_turn)

    def resetNode(self, A_turn):
        self.children = None
        self.score = None
        self.are_terminated = self.agentA.is_terminated and self.agentB.is_terminated

        # if not graph.more_people():
        if A_turn:
            if not self.agentA.is_terminated:
                self.A_turn = True
            else:
                self.A_turn = False
        if not A_turn:
            if not self.agentB.is_terminated:
                self.A_turn = False
            else:
                self.A_turn = True

        if self.A_turn:
            self.agent = self.agentA
            self.opponent = self.agentB
        else:
            self.agent = self.agentB
            self.opponent = self.agentA

        if self.strategy == STRATEGY_1:
            self.static_score = self.agentA.score - self.agentB.score
        if self.strategy == STRATEGY_2:
            self.static_score = [self.agent.score, self.opponent.score]
        if self.strategy == STRATEGY_3:
            self.static_score = self.agent.score + self.opponent.score

    def getScore(self):
        return self.score

    def getStaticScore(self):
        return self.static_score

    def makeNode(self):
        new_graph = Graph(to_copy=True, old_graph=self.graph)
        return GameTreeNode(new_graph,
                            Agent(to_copy=True, old_agent=self.agentA, graph=new_graph),
                            Agent(to_copy=True, old_agent=self.agentB, graph=new_graph),
                            A_turn=not self.A_turn,
                            depth=self.depth+1,
                            strategy=self.strategy)

    def expand(self):
        if not self.agent.position.in_vertex():
            child = self.makeNode()
            child.opponent.agent_move()
            self.children = [child]
            return

        self.children = []
        neighbours = self.graph.neighbours_of(self.agent.position.start)
        for vertex in neighbours:
            child = self.makeNode()
            child.makeMove(child.opponent, child.graph.get_vertex(vertex.key), child.A_turn)
            # child.opponent.agent_move(destination=)
            self.children.append(child)

        self.children.sort(key = GameTreeNode.getStaticScore)
        self.children.reverse()

    def makeMove(self, agent, vertex, turn):
        agent.agent_move(vertex)
        self.resetNode(turn)