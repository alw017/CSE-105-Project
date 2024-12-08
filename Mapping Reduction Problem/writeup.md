# Mapping Reduction Problem

I will be creating an implementation of a Mapping Reduction from A_TM to HALT_TM.

# Program Documentation

## String Encoding Spec

We define a valid input string as the following:

A string should consist of 7 sections:

1. A list of semicolon separated unique strings indicating state names.
2. A string of unique ASCII characters indicating the alphabet. The end is marked with a semicolon.
3. A string of unique ASCII characters indicating the tape alphabet. The end is marked with a semicolon.
4. A list of semicolon separated list transition definitions, formatted as such: `<from_state>,<tape-read>-<to_state>,<tape-write>,<L/R>;`
5. A single string from the set of defined state names, defined as the start state.
6. A single string from the set of defined state names, defined as the accept state.
7. A single string from the set of defined state names, defined as the reject state.
8. The input string intended to be simulated with the defined Turing Machine.

Any unspecified transitions in the list of item 4 are assumed to go to the reject state.

Each of these sections are separated by the string `END_SECTION`, which is a reserved word and cannot be used as a state name.

Note that on top of the reserved word `END_SECTION`, the symbol `;` also cannot be used in state names or the alphabet. Note that all whitespaces are ignored, so a defining a state as `state name;` will be interpreted as `statename;`.

On top of this, state names cannot start with the prefix `internal`. This is to avoid conflicts with the new states we will create. For transitions, we will interpret the character `_` as the empty read. The program also requires that the tape alphabet of any input Turing machine cannot include `#`. It should be easy to remap the conflicting variables when necessary.

Thus an example string would look like such:
```
q1;
q2;
qacc;
qrej;
END_SECTION
abc;
END_SECTION
abc_;
END_SECTION
q1,_-q2,a,L;
END_SECTION
q1;
END_SECTION
qacc;
END_SECTION
qrej;
END_SECTION
thisisateststring;
END_SECTION
```

## How the Program Works:

Our program will construct a new string which simulates the previously defined turing machine on the specified string we defined in the input.

To do this, the program first parses the Turing machine into each section, separating states, the alphabet, tape alphabet, and other relevant information into a tuple.

Then, it adds two main things:
1. A set of states and transitions to clear the tape of any input
2. A set of states and transitions to write our specified input string to the tape

Then, it connects the end of these two steps to the original input Turing machine, to simulate the input machine on the specified input string.

The program requires a Turing machine, where all possible transitions are explicitly written out in the transition section, and the assumed convention is that all transitions from the reject state self loop for all possible tape reads.

Then the program returns a Turing machine in the following format:

In seven sections, each ended with a `END_SECTION` keyword:

1. A list of semicolon separated unique strings indicating state names.
2. A string of unique ASCII characters indicating the alphabet. The end is marked with a semicolon.
3. A string of unique ASCII characters indicating the tape alphabet. The end is marked with a semicolon.
4. A list of semicolon separated list transition definitions, formatted as such: `<from_state>,<tape-read>-<to_state>,<tape-write>,<L/R>;`
5. A single string from the set of defined state names, defined as the start state.
6. A single string from the set of defined state names, defined as the accept state.
7. A single string from the set of defined state names, defined as the reject state.

The reject transitions in this new turing machine are implicit, and not all listed out in the output string.

## Justification for Lack of Error Checking

You might be wondering why there isn't very thorough checking for a valid turing machine. This is because, if the input turing machine is invalid, since we use it to create our new Turing machine, the new Turing machine must also be invalid, thus our function output cannot be in HALT_TM.

# Example Strings

## String in A_TM

Consider the following string, which describes a Turing machine followed by an input string.

```
q1;
qacc;
qrej;
END_SECTION
01;
END_SECTION
01_;
END_SECTION
q1,1-qacc,_,R;
q1,0-qacc,_,R;
q1,_-qrej,_,R;
qacc,_-qrej,_,R;
qacc,1-qrej,_,R;
qacc,0-qrej,_,R;
qrej,_-qrej,_,R;
qrej,1-qrej,_,R;
qrej,0-qrej,_,R;
END_SECTION
q1;
END_SECTION
qacc;
END_SECTION
qrej;
END_SECTION
01;
END_SECTION
```

The state diagram describing this turing machine is as follows:

![](./Example%201.png)

Note that our specified input string 01, is accepted by this Turing Machine. Thus, our string above must be in A_TM.

## String not in A_TM

Consider the following string, which describes a Turing machine followed by an input string.

```
q1;
qacc;
qrej;
END_SECTION
01;
END_SECTION
01_;
END_SECTION
q1,1-qacc,_,R;
q1,0-qacc,_,R;
q1,_-qrej,_,R;
qacc,_-qrej,_,R;
qacc,1-qrej,_,R;
qacc,0-qrej,_,R;
qrej,_-qrej,_,R;
qrej,1-qrej,_,R;
qrej,0-qrej,_,R;
END_SECTION
q1;
END_SECTION
qacc;
END_SECTION
qrej;
END_SECTION
;
END_SECTION
```

The state diagram describing this turing machine is as follows:

![](./Example%201.png)

Note that our specified input string ε, is rejected by this Turing Machine. Thus, our string above cannot be in A_TM.