from Graph import Graph
from Vertex import Vertex
from Edge import Edge
from Action import Action, TRAVERSE, TERMINATE, NO_OP, BLOCK
from GameTreeNode import STRATEGY_1, STRATEGY_2, STRATEGY_3
from GameTree import GameTree
from Agent import Agent
import numpy as np
from GameTreeNode import GameTreeNode
from GameTree import GameTree
from Color import COLOR

class HurricaneEnv:
    def __init__(self, graph_input_file_name,
                 cutoff, strategy,
                 position_number_A, position_number_B):
        # self.deadline = None
        self.strategy = strategy

        self.epoch = 0
        self.total_rescued = 0

        self.number_of_vertices = None
        self.read_graph_from_file(graph_input_file_name)

        agentA = Agent([self.graph], position_number_A, key=1)
        agentB = Agent([self.graph], position_number_B, key=2)
        self.agents = [agentA, agentB]      #[agent1, agent2]

        self.gameTree = GameTree(self.graph, agentA, agentB, strategy, cutoff)



    def read_graph_from_file(self, file_name):
        file = open(file_name, "r")
        vertices = []
        edges = []
        for line in file:
            words = line.split()
            if not words:  # if the list is empty
                continue
            first_word = words[0]
            if first_word[0] == ';':
                continue
            if first_word[1] == 'N':
                self.number_of_vertices = int(words[1])
                continue
            if first_word[1] == 'D':
                self.deadline = float(words[1])
                continue
            if first_word[1] == 'V':
                key = int(first_word[2:])
                if len(words) > 1:
                    second_word = words[1]
                    if second_word[0] == ';':
                        number_of_people = 0
                    else:
                        number_of_people = int(second_word[1:])
                else:
                    number_of_people = 0
                vertex = Vertex(key, number_of_people)
                vertices.append(vertex)
                continue
            if first_word[1] == 'E':
                key = int(first_word[2:])
                second_word = words[1]
                third_word = words[2]
                fourth_word = words[3][1:]
                vertex1 = Vertex.get_vertex(vertices, int(second_word))
                vertex2 = Vertex.get_vertex(vertices, int(third_word))
                weight = int(fourth_word)
                edge = Edge(vertex1, vertex2, weight, key)
                edges.append(edge)
        self.graph = Graph(vertices, edges)

    def end(self):
        if not self.graph.more_people():
            print("All people rescued")
            return True
        # for i, agent in enumerate(self.agents):
        #     if not agent.is_terminated:
        #         break
        #     if i == len(self.agents) - 1:
        #         print("All agents terminated")
        #         return True
        # if self.epoch >= np.floor(self.deadline):
        #     print("Deadline")
        #     return True
        return False

    def run_env(self):
        print(self.to_print())
        while not self.end():
            action = self.gameTree.get_Action()
            if action.action_type == TERMINATE:
                continue
            if action.action_type == TRAVERSE:
                self.gameTree.root.makeMove(self.gameTree.root.agent, action.argument, not self.gameTree.root.A_turn)
                # self.gameTree.root.makeMove(action.argument)

            self.epoch += 1
            self.calc_score()
            print(self.to_print())

    def calc_score(self):
        self.total_rescued = 0
        for agent in self.agents:
            self.total_rescued += agent.score
        return

    def to_print(self, include_graph=True):
        color_name=['GREEN', 'YELLOW']
        turn_of_color = 'PURPLE'

        if self.epoch == 0:
            pr = "ENV STATE: EPOCH 0 (initial state)____________\n"
        else:
            pr = "ENV STATE: EPOCH {} ___________________________\n".format(str(self.epoch))
        # pr += "\tdeadline:\t" + str(self.deadline) + "\n"
        if self.gameTree.root.A_turn:
            turn_str = "A"
        else:
            turn_str = "B"
        pr += "\tnext turn of: " +COLOR[turn_of_color]+ COLOR['BOLD']+"agent "+turn_str+COLOR['END'] +"\n"
        if include_graph:
            pr += "\tgraph:\n"
            if self.epoch == 0:
                graph_str = self.graph.to_print(with_unblocked_edges=True)
            else:
                graph_str = self.graph.to_print(with_unblocked_edges=False)
            lines = graph_str.splitlines()
            for i, line in enumerate(lines):
                pr += "\t\t" + line + "\n"
        pr += "\tTotal number people rescued: {}\n".format(self.total_rescued)
        pr += "\tAgents:\n"
        for i, agent in enumerate(self.agents):
            agent_str = agent.to_print(color_name[i])
            lines = agent_str.splitlines()
            if i==0:
                pr += COLOR[color_name[i]]+COLOR['BOLD']+"\t\t Agent A\n"+COLOR['END']
            if i==1:
                pr += COLOR[color_name[i]]+COLOR['BOLD']+"\t\t Agent B\n"+COLOR['END']
            for i, line in enumerate(lines):
                pr += "\t\t\t" + line + "\n"
        pr += COLOR['BOLD']+"__________________________________________________"+COLOR['END']
        return pr