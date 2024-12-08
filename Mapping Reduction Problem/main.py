import sys
import re

NON_HALTING_TM_STRING = "q1;qacc;qrej;END_SECTIONa;END_SECTIONa_;END_SECTIONq1,a-q1,a,L;q1,_-q1,_,L;END_SECTIONq1;END_SECTIONqacc;END_SECTIONqrej;END_SECTION"

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
    
def getTMCharacteristics(tokens):
    state = 1
    oldStates = ""
    oldAlphabet = ""
    oldTapeAlphabet = ""
    oldTransitions = ""
    oldStart = ""
    oldAccept = ""
    oldReject = ""
    inputString = ""
    for token in tokens:
        if (token == "END_SECTION"):
            state = state + 1
            continue
        else:
            match state:
                case 1:
                    oldStates = oldStates + token + ";"
                case 2:
                    if not oldAlphabet:
                        oldAlphabet = token
                    else:
                        raise Exception("multiple alphabets defined in input turing machine")
                case 3:
                    if not oldTapeAlphabet:
                        oldTapeAlphabet = token
                    else:
                        raise Exception("multiple tape alphabets defined in input turing machine")
                case 4:
                    oldTransitions = oldTransitions + token + ";"
                case 5:
                    if not oldStart:
                        oldStart = token
                    else:
                        raise Exception("multiple start states defined in input turing machine")
                case 6:
                    if not oldAccept:
                        oldAccept = token
                    else:
                        raise Exception("multiple accept states defined in input turing machine")
                case 7:
                    if not oldReject:
                        oldReject = token
                    else:
                        raise Exception("multiple reject states defined in input turing machine")
                case 8:
                    inputString = token
    return (oldStates, oldAlphabet, oldTapeAlphabet, oldTransitions, oldStart, oldAccept, oldReject, inputString)

def constructTransitionOverAlphabet(alphabet, fromstate, tostate, write, lr):
    out = ""
    for char in alphabet:
        out = out + fromstate + "," + char + "-" + tostate + "," + write + "," + lr + ";"
    return out

def constructTransitionNoOverwrite(alphabet, fromstate, tostate, lr):
    out = ""
    for char in alphabet:
        out = out + fromstate + "," + char + "-" + tostate + "," + char + "," + lr + ";"
    return out

def constructTransitionOverAlphabetNoSpace(alphabet, fromstate, tostate, write, lr):
    newalpha = alphabet.replace("_","")
    return constructTransitionOverAlphabet(newalpha, fromstate, tostate, write, lr)

    

def run(file):
    tokens = Lexer(file.read()).run()
    (oldStates, oldAlphabet, oldTapeAlphabet, oldTransitions, oldStart, oldAccept, oldReject, inputString) = getTMCharacteristics(tokens)
            
    # add tape clearing states and relevant transitions
    clearStates = "internalcs;internalcc;internalcr;internalcf;" # cs = clear start, cc = clearing, cr = clear return, cf = clear finish
    clearTransitions = (constructTransitionOverAlphabet(oldTapeAlphabet, "internalcs", "internalcc","#","R") +
                        constructTransitionOverAlphabetNoSpace(oldTapeAlphabet, "internalcc", "internalcc", "_", "R") + 
                        "internalcc,_-internalcr,_,L;" +
                        "internalcr,_-internalcr,_,L;" +
                        "internalcr,#-internalcf,#,R;" # we keep the hashtag so we know when we are back at the start of the tape.
                       )
    
    # add inputString into tape
    inputStates = ""
    inputTransitions = ""

    if (len(inputString) < 2):
        inputStates = "internalir;internalif;"
        inputTransitions = "internalcf,_-internalir,_,L;"
        if(len(inputString) == 0):
            inputTransitions = inputTransitions + "internalir,#-internalif,_,L;"
        else:
            inputTransitions = inputTransitions + "internalir,#-internalif," + inputString[0] + ",L;"
    else: 
        for i in range(len(inputString)-1): # keeping the hashtag start, start writing from the second tape box on.
            inputStates = inputStates + "internali" + str(i + 1) + ";"
        
        inputTransitions = "internalcf,_-internali1," + inputString[1] + ",R;"
        for i in range(2,len(inputString)):
            inputTransitions = inputTransitions + "internali" + str(i-1) + ",_-internali" + str(i) + "," + inputString[i] + ",R;"
        
        lastIndex = str(len(inputString) - 1)
        lastInputStateName = "internali" + lastIndex

        inputStates += "internalif;"
        inputTransitions += (constructTransitionNoOverwrite(oldTapeAlphabet, lastInputStateName, lastInputStateName, "L") + 
                             lastInputStateName + ",#-internalif," + inputString[0] + ",L;" 
                            ) 
        
    startTransition = constructTransitionNoOverwrite(oldAlphabet, "internalif", oldStart, "L")
    newRejectState = "internalNewReject;"

    newStates = oldStates + clearStates + inputStates + newRejectState
    newAlpabet = oldAlphabet + ";"
    newTapeAlphabet = ''.join(set(oldTapeAlphabet).union(set(oldAlphabet))) + "#;"
    newTransitions = oldTransitions + clearTransitions + inputTransitions + startTransition
    newStart = "internalcs;"
    newAccept = oldAccept + ";"
    newReject = newRejectState
    out = (newStates + "END_SECTION" 
           + newAlpabet + "END_SECTION" 
           + newTapeAlphabet + "END_SECTION" 
           + newTransitions + "END_SECTION" 
           + newStart + "END_SECTION" 
           + newAccept + "END_SECTION"
           + newReject + "END_SECTION"
    )

    return out

def main():
    if len(sys.argv) != 2:
       print("Invalid Number of Arguments " + str(len(sys.argv)) + " received, 2 expected.")
       return
    filename = sys.argv[1]
    try:
        with open(filename, "r") as file:
            return run(file)
    except FileNotFoundError: # not in ATM
        print("Specified file not found.")
        return NON_HALTING_TM_STRING
    except Exception as e:
        print (e)
        return NON_HALTING_TM_STRING
    


print(main())