from pyeda.inter import *
from myeda.simulation import *
import nose


def test_state():
    test_state = State(-1, [], [], [])
    assert len(str(test_state)) > 0


def test_states():
    states = [State(-1, [], [], []), State(-10, [], [], [])]
    assert len(str(states)) > 0


def test_event():
    test_event = Event('A', True, -1, 1)
    assert len(str(test_event)) > 0


delay = 2
signals = ['A', 'B', 'sel', 'seln', 'S1', 'S2', 'Q']
deps = {
    'A': ['S1'],
    'B': ['S2'],
    'sel': ['seln', 'S2'],
    'seln': ['S1'],
    'S1': ['Q'],
    'S2': ['Q']}
func = {'S1': '~(A&seln)', 'S2': '~(B&sel)', 'seln': '~sel', 'Q': '~(S1&S2)'}
initial_state = {
    'A': False,
    'B': False,
    'sel': True,
    'seln': False,
    'S1': True,
    'S2': True,
    'Q': False}
stimuli = [
    Event(
        'A', True, 0, 20), Event(
            'B', True, 0, 10), Event(
                'sel', False, 0, 30)]
ts = '1 ns'


def test_sim():
    sim = Sim.Sim(signals, deps, initial_state, stimuli, func, delay, ts)
    assert sim.simulate()


def test_dump_vcd():
    sim = Sim.Sim(signals, deps, initial_state, stimuli, func, delay, ts)
    sim.simulate()
    vcd = sim.dump_vcd()
    assert len(vcd) > 0  # TODO


if __name__ == '__main__':
    nose.run()
