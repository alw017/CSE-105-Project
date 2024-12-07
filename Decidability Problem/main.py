import sys
import re

class Lexer:
    def __init__(self, string):
        self.string = string.replace('\n','').replace('\r','').replace(' ', '')
        self.line = 0
        self.index = 0
    
    def readToken(self):
        startIndex = self.index
        while (not self.atEnd() and self.next() != ";" and self.string[startIndex:self.index+1] != "END_SECTION"):
            self.index = self.index + 1
        out = self.string[startIndex:self.index + 1]
        if out == "END_SECTION":
            self.index = self.index + 1
        else:
            self.index = self.index + 2
        if (self.atEnd() and not out == "END_SECTION"): return "EOF"
        return out

    def atEnd(self):
        return self.index + 1 >= len(self.string)

    def next(self):
        if not self.atEnd():
            return self.string[self.index + 1]
        else:
            return "EOF"

    def run(self):
        token = self.readToken()
        out = []
        while (token != "EOF"):
            out.append(token)
            token = self.readToken()
        return out

def run(file):
    lex = Lexer(file.read())
    tokens = lex.run()
    state = 1
    definedStates = set()
    stateTransitions = {}
    alphabet = set()
    start = ""
    acceptStates = set()
    for token in tokens:
        if (token == "END_SECTION"): 
            state = state + 1
            continue
        match state:
            case 1: # defining states
                definedStates.add(token)
                stateTransitions[token] = {}
            case 2: # defining alphabet
                alphabet = set(token)
            case 3: # defining state transitions
                transition = re.split('-|,', token)
                if (len(transition) != 3):
                    raise Exception("Error! Transition token had incorrect format "+ token)
                else:
                    if transition[0] in definedStates and transition[1] in definedStates and transition[2] in alphabet:
                        stateTransitions[transition[0]][transition[2]] = transition[1]
                    else:
                        raise Exception("Error! Transition token tried to specify a transition using an undefined state or invalid input character")
            case 4: # defining start state
                if len(start) != 0:
                    raise Exception("Error! More than one start state defined")
                    continue
                start = token
            case 5: # defining accept states
                if (token in definedStates):
                    acceptStates.add(token)
                else:
                    raise Exception("Error! Specified accept state " + token + " is not defined!")
    for state in stateTransitions:
        if len(stateTransitions[state].keys()) != len(alphabet):
            raise Exception("Error! not enough transitions defined for state " + state)
    return (definedStates, alphabet, stateTransitions, start, acceptStates)


def isEmpty(dfa):
    (definedStates, alphabet, stateTransitions, start, acceptStates) = dfa
    explored = set()
    unexplored = [start]
    while len(unexplored) > 0:
        currState = unexplored.pop()
        explored.add(currState)
        for key in stateTransitions[currState]:
            if stateTransitions[currState][key] not in explored:
                unexplored.append(stateTransitions[currState][key])
    
    intersection = acceptStates.intersection(explored)

    return len(intersection) == 0

def main():
    if len(sys.argv) != 2:
       print("Invalid Number of Arguments " + str(len(sys.argv)) + " received, 2 expected.")
       return
    filename = sys.argv[1]
    try:
        with open(filename, "r") as file:
            dfa = run(file)
            if isEmpty(dfa):
                print("The specified DFA is empty")
            else:
                print("The specified DFA is nonempty")
    except FileNotFoundError:
        print("Specified file not found.")
    except Exception as e:
        print("Program failed with error: \"" + str(e) + "\"")

main()