from GameTreeNode import GameTreeNode
from GameTreeNode import STRATEGY_2, STRATEGY_3
from Action import Action
from Action import TRAVERSE, TERMINATE
from Vertex import Vertex


class GameTree():
    def __init__(self, graph, agentA, agentB, strategy, cutoff):
        self.root = GameTreeNode(graph, agentA, agentB, A_turn=True, depth=0,
                                 strategy=strategy)
        self.cutoff = cutoff  # assume cutoff > 0
        self.strategy = strategy

    def get_Action(self):
        maximum_score_node = GameTree.getBestNode(self)
        if maximum_score_node == None:
            return Action(TERMINATE)
        if self.root.A_turn:
            destination = self.root.graph.get_vertex(maximum_score_node.agentA.position.end.key)
        else:
            destination = self.root.graph.get_vertex(maximum_score_node.agentB.position.end.key)
        if destination is None:
            return Action(TERMINATE)
        else:
            return Action(TRAVERSE, destination)

    def getBestNode(self):
        if self.strategy == 1:
            return self.getMinimax(self.root, self.cutoff, alpha=-float('inf'), beta=float('inf'))
        if self.strategy == 2 or self.strategy == 3:
            return GameTree.getMaxScoreNode(self.root, self.cutoff, self.strategy)

    @staticmethod
    def getMinusInfinity(strategy):
        if strategy == STRATEGY_2:
            return [-float('inf'), -float('inf')]
        if strategy == STRATEGY_3:
            return -float('inf')

    @staticmethod
    def getMaxScoreNode(root, cutoff, strategy):
        if root.depth >= cutoff:
            root.score = root.static_score
            return
        root.expand()
        if not root.children and root.depth == 0:
            return None
        if not root.children and root.depth != 0:
            root.score = root.static_score
            return
        cur_max_score = GameTree.getMinusInfinity(strategy)
        maximum_score_node = None
        for child in root.children:
            GameTree.getMaxScoreNode(child, cutoff, strategy)
            child_score = GameTree.reverse(child.score, strategy)
            if child_score > cur_max_score:
                maximum_score_node = child
                cur_max_score = child.score
        root.score = cur_max_score

        if root.depth == 0:
            return max(root.children, key=GameTreeNode.getScore)

    @staticmethod
    def reverse(score, strategy):
        if strategy == STRATEGY_2:
            new_score = score.copy()
            new_score.reverse()
            return new_score
        if strategy == STRATEGY_3:
            return score

    @staticmethod
    def getMinimax(root, cutoff, alpha, beta):
        if root.depth >= cutoff:
            root.score = root.static_score
            return
        root.expand()
        if not root.children:
            root.score = root.static_score
            return
        if root.A_turn:  ######### we play for agent not for agent A
            cur_max_score = -float('inf')
            for child in root.children:
                GameTree.getMinimax(child, cutoff, alpha, beta)
                if child.score > cur_max_score:
                    maximum_score_node = child
                    cur_max_score = child.score
                alpha = max(alpha, cur_max_score)
                if beta <= alpha:
                    break
            root.score = maximum_score_node.score
            return maximum_score_node
        else:
            cur_min_score = float('inf')
            for child in root.children:
                GameTree.getMinimax(child, cutoff, alpha, beta)
                if child.score < cur_min_score:
                    minimum_score_node = child
                    cur_min_score = child.score
                beta = min(beta, cur_min_score)
                if beta <= alpha:
                    break
            root.score = minimum_score_node.score
            return minimum_score_node
