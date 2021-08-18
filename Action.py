TRAVERSE = 1
TERMINATE = 2
NO_OP=3
BLOCK = 4

class Action:
    def __init__(self, action_type, argument=None): #argument is a vertx or an edge
        self.action_type=action_type
        self.argument = argument
