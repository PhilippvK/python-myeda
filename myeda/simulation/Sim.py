#!/usr/bin/python3

import os
from pyeda.inter import *
from collections import OrderedDict
import wavedrom


class State(object):

    def __init__(self, t, signals, evaluated, events):
        self.t = t
        self.signals = signals
        self.evaluated = evaluated
        self.events = events

    def __str__(self):
        return str("T=" + str(self.t) + "\t" + str(self.signals) + "\t" +
                   str(self.evaluated) + "\t" + str(self.events))

    def __repr__(self):
        return str("T=" + str(self.t) + "\t" + str(self.signals) + "\t" +
                   str(self.evaluated) + "\t" + str(self.events))


class Event(object):

    def __init__(self, signal, value, occured, planned):
        self.signal = signal
        self.value = value
        self.occured = occured
        self.planned = planned

    def __str__(self):
        return str((self.signal, int(self.value), self.occured, self.planned))

    def __repr__(self):
        return str((self.signal, int(self.value), self.occured, self.planned))


class Sim(object):

    def __init__(self, signals, deps, initial_state, stimuli, func, delay, ts):
        self.signals = signals
        self.deps = deps
        self.initial_state = initial_state
        self.stimuli = stimuli
        self.delay = delay
        self.events = []
        self.timeline = []
        self.changes = []
        self.events.extend(self.stimuli)
        self.timeline.append(
            State(
                0,
                self.initial_state,
                ["Initial State"],
                self.stimuli))
        self.changes = self.events.copy()
        self.exprs = []
        self.func = func
        self.ts = ts
        for s in self.signals:
            self.exprs.append(exprvar(s))

    def __str__(self):
        print("Sim(", self.signals, ")")

    def pop_events(self):
        choice = None
        choices = []
        for e in self.events:
            if len(choices) == 0:
                choice = e.planned
                choices = [e]
            elif e.planned == choice:
                choices.append(e)
            elif e.planned < choice:
                choice = e.planned
                choices = [e]
        for c in choices:
            self.events.remove(c)
        return choices

    def update_states(self, states, events):
        new_states = states.copy()
        new_events = []
        for e in events:
            new_states[e.signal] = e.value
        for e in events:
            if e.signal in self.deps.keys():
                mappings = {}
                for s in self.signals:
                    mappings[expr(s)] = new_states[s]
                for d in self.deps[e.signal]:
                    self.evaluated.append(d)
                    m = {expr(e.signal): e.value}
                    v = expr(self. func[d]).restrict(mappings).is_one()
                    if v != expr(new_states[d]).is_one():
                        new_events.append(
                            Event(
                                d,
                                v,
                                e.planned,
                                e.planned +
                                self.delay))
        return new_states, new_events

    def simulate(self):
        print(self.timeline[0])
        while len(self.events) > 0:
            self.evaluated = []
            e = self.pop_events()
            t = e[0].planned
            c = self.timeline[-1].signals.copy()
            c_new, e_new = self.update_states(c, e)
            #self.timeline.append((t, c_new, e_new))
            self.timeline.append(State(t, c_new, self.evaluated, e_new))
            self.events.extend(e_new)
            self.changes.extend(e_new)
#           print("t=" + str(t) + "\t" + str(c_new) + "\t" + str(e_new))
#           print("t=" + str(t) + "\t" + str(c_new) + "\t" + str(e_new))
            print(self.timeline[-1])

    def dump_vcd(self):
        events = sorted(self.changes, key=lambda x: x.planned)
        ret = ""
        t = -1
        ret += "$date today $end\n"
        ret += "$timescale {} $end\n".format(self.ts)
        ret += "$scope module top $end\n"
        for i, s in enumerate(self.signals):
            ret += "$var reg 1 {} {} $end\n".format(i, s)
        ret += "$upscope $end\n"
        ret += "$enddefinitions $end\n"
        ret += "#0\n"
        for i, s in enumerate(self.signals):
            ret += "b{} {}\n".format(int(self.initial_state[s]), i)
        for e in events:
            if e.planned > t:
                t = e.planned
                ret += "#{}\n".format(t)
            ret += "b{} {}\n".format(int(e.value),
                                     self.signals.index(e.signal))
        ret += "#{}".format(t+2)
        return ret

#   def plot(self):
#       timeout=5
#       fname="/tmp/scope.vcd"
#       file=open(fname,"w")
#       content=self.dump_vcd(ts)
#       file.write(content)
#       file.close()
#       os.environ['DISPLAY'] = ':0'
#       cmd="/usr/bin/timeout {} /usr/bin/gtkwave -S gtkwave.tcl {}".format(timeout,fname)
#       os.system(cmd)
#       os.system("rm {}".format(fname))
#       return fname+str(".ps")

    def render_svg(self):
        return wavedrom.render(Sim.vcd2wave(self.dump_vcd())).tostring()

    def vcd2wave(inp):
        ticks = []
        current_tick = 0
        timeline = []
        variables = OrderedDict()
        searching = True
        gather_vars = True
        for line in inp.split('\n'):
            if gather_vars:
                if '$timescale' in line:
                    split = line.split(' ')
                    ts = (int(split[-3]), split[-2])
                elif searching:
                    if '$var' in line:
                        searching = False
                        split = line.split(' ')
                        name = split[-2]
                        label = split[-3]
                        variables[label] = name
                else:
                    if '$var' not in line:
                        gather_vars = False
                        # print(variables)
                    else:
                        split = line.split(' ')
                        name = split[-2]
                        label = split[-3]
                        variables[label] = name
            else:
                if len(line) == 0:
                    break
                if line[0] == '#':
                    tick = int(line[1:])
                    ticks.append(tick)
                    current_tick = ticks[-1]
                    timeline.append([])
                elif line[0] == 'b':
                    split = line.split(' ')
                    label = split[-1]
                    value = bool(int(split[0][1:]))
                    timeline[-1].append((variables[label], value))

        step_size = min([ticks[i+1]-ticks[i]
                         for i in range(len(ticks)-1)])  # = 2
        steps = (ticks[-1]-ticks[0])//step_size  # = 18

        # print(list(enumerate(ticks)))

        waves = []
        for variable in variables.values():
            wave = [(t//step_size, val) for (i, t) in enumerate(ticks)
                    for (var, val) in timeline[i] if var == variable]
            w = ''
            for step in range(steps + 1):
                changes = [s for (s, v) in wave]
                if step in changes:
                    if wave[changes.index(step)][1]:
                        w = w + '1'
                    else:
                        w = w + '0'
                else:
                    w = w + '.'
            waves.append(w)

        title = "Simulation Waveform"

        output = ""

        output = output + """{
    \"signal\": [\n"""

        for i, variable in enumerate(variables.values()):
            output = output + "        {{ \"name\": \"{}\",\t\"wave\": \"{}\" }}{}\n".format(
                variable, waves[i], ',' if i < len(variables) - 1 else '')

        output = output + """    ],
    "head": {{
        "text": "{}"
    }},
    "foot": {{
        "text": "Time [{} {}]",
        "tick": {}
    }}
}}""".format(title, step_size * ts[0], ts[1], ticks[0] * ts[0])

        return output
