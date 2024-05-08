from automathon import DFA
q = {'q0', 'q1', 'q2'}
sigma = {'0', '1'}
delta = { 'q0' : {'0' : 'q0', '1' : 'q1'},
          'q1' : {'0' : 'q2', '1' : 'q0'},
          'q2' : {'0' : 'q1', '1' : 'q2'}
        }
initial_state = 'q0'
f = {'q0'}

automata = DFA(q, sigma, delta, initial_state, f)
automata.view("DFA Visualization")