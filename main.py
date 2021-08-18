from HurricaneEnv import HurricaneEnv
from GameTreeNode import STRATEGY_1, STRATEGY_2, STRATEGY_3
import _settings
import Tests
input = input

def _setInputFunction():
    global input
    input = _settings.preferred_input


def runProgram():
    graph_number = int(input("What graph number?\t"))
    strategy = int(input("What strategy? 1/2/3\t"))
    cutoff = int(input("What is the cutoff?\t"))
    position_number_A = int(input("What is the position of agent A?\t"))
    position_number_B = int(input("What is the position of agent B?\t"))
    HurricaneEnv("tests/graph_"+str(graph_number)+".txt", cutoff, strategy,
                 position_number_A, position_number_B).run_env()


if __name__ == '__main__':
    #Tests.AutoTestAll()
    # Tests.AutoTestAll()

    ### To test a specific test, run the following
    Tests.AutoTest(test_number=6)

    ###To test the program manually, run the following
     # Tests.manualTest()

    ### To run the program, run the following:
    # runProgram()



