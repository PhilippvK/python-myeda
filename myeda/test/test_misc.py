from pyeda.inter import *
from myeda.misc import *
import nose

def test_onset_expr():
    assert onset(expr('y[0]&~y[1] | ~y[0]&y[1] | y[0]&y[1]')) == [2, 1]
    # TODO: allow any order

def test_onset_ttable():
    X = exprvars('x',3)
    assert onset(truthtable(X, "00110101")) == [2, 3, 5, 7]
    # TODO: allow any order

#def test_onset_one():
#    assert onset(1) == [0,1,2,...] 
#    assert onset(True) == [0,1,2,...] 
#    # TODO: allow any order

#def test_onset_zero():
#    assert onset(0) == [] 
#    assert onset(False) == [] 

def test_variables_expr():
    assert variables(expr('y[0]&~y[1] | ~y[0]&y[1] | y[0]&y[1]')) == ['y[0]', 'y[1]']
    # TODO: allow any order vs. force?

def test_variables_ttable():
    X = exprvars('x',3)
    assert variables(truthtable(X, "00110101")) == ['x[0]', 'x[1]', 'x[2]']
    # TODO: allow any order vs. force?

def test_variables_err():
    assert True

def test_bitstring2expr():
    assert expr(bitstring2expr({'-11', '00-'},['x[0]','x[1]','x[2]'])).equivalent(expr('x[0] & x[1] | ~x[1] & ~x[2]'))


if __name__ == '__main__':   
    nose.run()
