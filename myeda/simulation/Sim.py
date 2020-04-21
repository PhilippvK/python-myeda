'''Module Documentation'''
#!/usr/bin/python3

#from collections import OrderedDict
#import wavedrom
#from pyeda.inter import *
from pyeda.inter import expr, exprvar


class State:
    '''State Documentation'''

    def __init__(self, time, signals, evaluated, events):
        self.time = time
        self.signals = signals
        self.evaluated = evaluated
        self.events = events

    def __str__(self):
        return str("T=" + str(self.time) + "\t" + str(self.signals) + "\t" +
                   str(self.evaluated) + "\t" + str(self.events))

    def __repr__(self):
        return str("T=" + str(self.time) + "\t" + str(self.signals) + "\t" +
                   str(self.evaluated) + "\t" + str(self.events))


class Event:
    '''Event Documentation'''

    def __init__(self, signal, value, occured, planned):
        self.signal = signal
        self.value = value
        self.occured = occured
        self.planned = planned

    def __str__(self):
        return str((self.signal, int(self.value), self.occured, self.planned))

    def __repr__(self):
        return str((self.signal, int(self.value), self.occured, self.planned))


class Sim:
    '''Sim Documentation'''

    def __init__(self, signals, deps, initial_state,
                 stimuli, func, delay, timescale):
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
        self.timescale = timescale
        for s in self.signals:
            self.exprs.append(exprvar(s))

    def __str__(self):
        print("Sim(", self.signals, ")")

    def pop_events(self):
        '''pops list of events'''
        choice = None
        choices = []
        for event in self.events:
            if len(choices) == 0:
                choice = event.planned
                choices = [event]
            elif event.planned == choice:
                choices.append(event)
            elif event.planned < choice:
                choice = event.planned
                choices = [event]
        for choice in choices:
            self.events.remove(choice)
        return choices

    def update_states(self, states, events):
        '''updates the list of states'''
        new_states = states.copy()
        new_events = []
        for event in events:
            new_states[event.signal] = event.value
        for event in events:
            if event.signal in self.deps.keys():
                mappings = {}
                for signal in self.signals:
                    mappings[expr(signal)] = new_states[signal]
                for dep in self.deps[event.signal]:
                    self.evaluated.append(dep)
                    mapping = {expr(event.signal): event.value}
                    value = expr(self. func[dep]).restrict(mappings).is_one()
                    if value != expr(new_states[dep]).is_one():
                        new_events.append(
                            Event(
                                dep,
                                value,
                                event.planned,
                                event.planned +
                                self.delay))
        return new_states, new_events

    def simulate(self):
        '''run simulation'''
        print(self.timeline[0])
        while len(self.events) > 0:
            self.evaluated = []
            events = self.pop_events()
            time = events[0].planned
            signals = self.timeline[-1].signals.copy()
            signals_new, events_new = self.update_states(signals, events)
            self.timeline.append(State(time, signals_new, self.evaluated, events_new))
            self.events.extend(events_new)
            self.changes.extend(events_new)
            print(self.timeline[-1])
        return True

    def dump_vcd(self):
        '''return string containing value change dump format'''
        events = sorted(self.changes, key=lambda x: x.planned)
        ret = ""
        time = -1
        ret += "$date today $end\n"
        ret += "$timescale {} $end\n".format(self.timescale)
        ret += "$scope module top $end\n"
        for i, signal in enumerate(self.signals):
            ret += "$var reg 1 {} {} $end\n".format(i, signal)
        ret += "$upscope $end\n"
        ret += "$enddefinitions $end\n"
        ret += "#0\n"
        for i, signal in enumerate(self.signals):
            ret += "b{} {}\n".format(int(self.initial_state[signal]), i)
        for event in events:
            if event.planned > time:
                time = event.planned
                ret += "#{}\n".format(time)
            ret += "b{} {}\n".format(int(event.value),
                                     self.signals.index(event.signal))
        ret += "#{}".format(time+2)
        return ret

#    def render_svg(self):
#        return wavedrom.render(Sim.vcd2wave(self.dump_vcd())).tostring()
#
#    def vcd2wave(inp):
#        ticks = []
#        current_tick = 0
#        timeline = []
#        variables = OrderedDict()
#        searching = True
#        gather_vars = True
#        for line in inp.split('\n'):
#            if gather_vars:
#                if '$timescale' in line:
#                    split = line.split(' ')
#                    timescale = (int(split[-3]), split[-2])
#                elif searching:
#                    if '$var' in line:
#                        searching = False
#                        split = line.split(' ')
#                        name = split[-2]
#                        label = split[-3]
#                        variables[label] = name
#                else:
#                    if '$var' not in line:
#                        gather_vars = False
#                        # print(variables)
#                    else:
#                        split = line.split(' ')
#                        name = split[-2]
#                        label = split[-3]
#                        variables[label] = name
#            else:
#                if len(line) == 0:
#                    break
#                if line[0] == '#':
#                    tick = int(line[1:])
#                    ticks.append(tick)
#                    current_tick = ticks[-1]
#                    timeline.append([])
#                elif line[0] == 'b':
#                    split = line.split(' ')
#                    label = split[-1]
#                    value = bool(int(split[0][1:]))
#                    timeline[-1].append((variables[label], value))
#
#        step_size = min([ticks[i+1]-ticks[i]
#                         for i in range(len(ticks)-1)])  # = 2
#        steps = (ticks[-1]-ticks[0])//step_size  # = 18
#
#        # print(list(enumerate(ticks)))
#
#        waves = []
#        for variable in variables.values():
#            wave = [(t//step_size, val) for (i, t) in enumerate(ticks)
#                    for (var, val) in timeline[i] if var == variable]
#            w = ''
#            for step in range(steps + 1):
#                changes = [s for (s, v) in wave]
#                if step in changes:
#                    if wave[changes.index(step)][1]:
#                        w = w + '1'
#                    else:
#                        w = w + '0'
#                else:
#                    w = w + '.'
#            waves.append(w)
#
#        title = "Simulation Waveform"
#
#        output = ""
#
#        output = output + """{
#    \"signal\": [\n"""
#
#        for i, variable in enumerate(variables.values()):
#            output = output + "        {{ \"name\": \"{}\",\t\"wave\": \"{}\" }}{}\n".format(
#                variable, waves[i], ',' if i < len(variables) - 1 else '')
#
#        output = output + """    ],
#    "head": {{
#        "text": "{}"
#    }},
#    "foot": {{
#        "text": "Time [{} {}]",
#        "tick": {}
#    }}
#}}""".format(title, step_size * ts[0], ts[1], ticks[0] * ts[0])
#
#        return output
