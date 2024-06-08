import re
import time

from threading import Thread, Lock

THRESHOLD = 0.3
KEYS = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]


def sorter(note):
    key, oct = get_note(note)
    return KEYS.index(key) + oct * len(KEYS)


def get_note(note):
    key, oct = re.match(r'([A-G]#?)(\d+)', note).groups()
    oct = int(oct)
    return key, oct


def press(key):
    _, oct = get_note(key)
    fsms[oct - 1].process(key, time.time())
    if oct > 2:
        fsms[oct - 2].process(key, time.time())


class State:
    def __init__(self, state, transitions, name):
        self.name = name
        self.state_number = state
        self.incremental = []
        self.transition_table = {}
        for input_, next_state in zip(transitions[::2], transitions[1::2]):
            if input_.endswith("."):
                self.incremental.append(input_ := input_[:-1])
            self.transition_table[input_] = next_state

        if "START" in name:
            FSM.start_state = self
        elif "NORMAL" not in name:
            FSM.end_states.append(self)

    @property
    def is_final(self):
        return self in FSM.end_states

    def transition(self, char, prev_octave=None):
        key, octave = get_note(char)
        next_state = self.transition_table.get(key)
        reset = next_state is None
        reset |= prev_octave is not None and (octave != prev_octave + (key in self.incremental))
        if reset:
            return FSM.start_state.transition(char)
        return FSM.states[next_state], octave


class FSM:
    states = {}
    start_state = None
    end_states = []
    detected_queue = []
    lock = Lock()

    def __init__(self):
        self.prev_time = 0
        self.prev_octave = None
        self.cur_state = self.start_state
        self.exec_queue = []
        Thread(target=self.checker, daemon=True).start()

    def run_queue(self):
        for char in sorted(self.exec_queue, key=sorter):
            old_state = self.cur_state
            self.cur_state, self.prev_octave = self.cur_state.transition(char, self.prev_octave)
            if old_state.is_final and not self.cur_state.is_final:
                print("Detected " + str(old_state.name)+"\n",end="")
        self.exec_queue.clear()
        if self.cur_state.is_final:
            with FSM.lock:
                exist = any(
                    state == self.cur_state.name for state, _ in FSM.detected_queue if time.time() - _ < THRESHOLD)
                index = 0
                while index < len(FSM.detected_queue):
                    if time.time() - FSM.detected_queue[index][1] > THRESHOLD:
                        FSM.detected_queue.pop(index)
                    else:
                        index += 1
                if not exist:
                    FSM.detected_queue.append((self.cur_state.name, time.time()))
                    print("Detected " + str(self.cur_state.name)+"\n", end="")
        self.cur_state = FSM.start_state

    def checker(self):
        while True:
            time.sleep(0)
            if time.time() - self.prev_time > THRESHOLD:
                if self.exec_queue:
                    self.run_queue()

    def process(self, char, ctime):
        self.exec_queue.append(char)
        self.prev_time = ctime


with open('chords-stripped.fsm') as lang:
    data = lang.read().splitlines()

for line in data:
    if not line or line.isspace():
        continue
    state, *transitions, name = re.split(r'\s+', line)
    if len(transitions) % 2:
        transitions += name,
        name = "NORMAL"
    FSM.states[state] = State(state, transitions, name)

fsms = [FSM() for _ in range(6)]
