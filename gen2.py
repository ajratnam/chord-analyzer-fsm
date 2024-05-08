import re
from automathon import DFA

with open('chords-stripped.fsm') as lang:
    data = lang.read().splitlines()

states = set()
sym = set()
trans = {}
final_states = set()
sw = {}

for line in data:
    if not line or line.isspace():
        continue
    state, *transitions, name = re.split(r'\s+', line)
    if len(transitions) % 2:
        transitions += name,
        name = "TEMP"
    if name in ["TEMP", "START"]:
        states.add(state)
    else:
        sw[state] = name
        states.add(name)
    trans[state] = {}
    for char, next_state in zip(*[iter(transitions)]*2):
        sym.add(char.rstrip("."))
        trans[state][char.rstrip(".")] = next_state
    # if state != "00":
    #     for char, next in trans["00"].items():
    #         trans[state].setdefault(char, next)

    if name not in ["TEMP", "START"]:
        final_states.add(name)

# print("states = ", states)
# print("trans = ", trans)
# print("final_states = ", final_states)

# import pprint
# pprint.pprint(trans)

for state, transitions in trans.copy().items():
    for char, next_state in transitions.items():
        if next_state in sw:
            transitions[char] = sw[next_state]
    if state in sw:
        trans[sw[state]] = trans[state]
        del trans[state]

dfa = DFA(
    states,
    sym,
    trans,
    "00",
    final_states
)

dfa.view("chords-fsm3")
