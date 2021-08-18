stdin = input
preferred_input = None

def makeInputAuto(user_input_file):
    global stdin
    global preferred_input
    def auto_input(message=""):
        print(message)
        p = next(user_input_file)
        print(p)
        if p[-1] == '\n':
            p = p[0:-1]
        return p
    preferred_input = auto_input

def makeInputManual():
    global stdin
    global preferred_input
    preferred_input = stdin