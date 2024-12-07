# Computational Problem

In this project, I intend to construct a program that decides the DFA emptiness problem.

# Program Documentation

## String Encoding Spec

We define a valid string as the following:

A string should consist of 5 sections:

1. A list of semicolon separated unique strings indicating state names.
2. A string of unique ASCII characters indicating the alphabet. The end is marked with a semicolon.
3. A list of semicolon separated list transition definitions, formatted as such: `<from_state>-<to_state>,<input>;`
4. A single string from the set of defined state names.
5. A list of semicolon separated strings from the defined states in item 1. Repeats are ignored.

Each of these sections are separated by the string `END_SECTION`, which is a reserved word and cannot be used as a state name.

Note that on top of the reserved word `END_SECTION`, the symbol `;` also cannot be used in state names or the alphabet. All whitespaces are ignored.

Thus an example string would look like such:
```
q1;
q2;
END_SECTION
abc;
END_SECTION
q1-q2,a;
q1-q1,b;
q1-q2,c;
q2-q1,a;
q2-q2,b;
q2-q2,c;
END_SECTION
q1;
END_SECTION
q2;
END_SECTION
```

# Example Strings

## Example in the Set of Empty DFAs

```
q1;q2;END_SECTION
0;END_SECTION
q1-q1,0;q2-q1,0;END_SECTION
q1;END_SECTION
q2;END_SECTION
```

There is no way to reach the accept state `q2` from the start state `q1`, so we know that this DFA must recognize the empty set.
 
## Example not in the Set of Empty DFAs

```
q1;q2;q3;q4;END_SECTION
01;END_SECTION
q1-q1,1;q1-q2,0;
q2-q2,0;q2-q3,1;
q3-q3,1;q3-q4,0;
q4-q4,0;q4-q4,1;END_SECTION
q1;END_SECTION
q3;END_SECTION
```

This DFA recognizes the language defined by the Regular Expression: `1*0+1+`. One example of a string accepted is "01". Thus it is not in the Set E_DFA.