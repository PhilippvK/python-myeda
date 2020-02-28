"""
Test Boolean functions
"""

from nose.tools import assert_raises

from pyeda.boolalg.boolfunc import (
    num2point,
    num2upoint,
    num2term,
    point2upoint,
    point2term,
    iter_points,
    iter_upoints,
    iter_terms,
    var,
)
from pyeda.boolalg.expr import exprvar


a, b, c, d = map(exprvar, 'abcd')
aa, bb, cc, dd = a.uniqid, b.uniqid, c.uniqid, d.uniqid

def test_var():
    assert_raises(TypeError, var, 42)
    assert_raises(ValueError, var, tuple())
    assert_raises(TypeError, var, (42, ))
    assert_raises(TypeError, var, 'a', 'index')
    assert_raises(TypeError, var, 'a', ('index', ))
    assert_raises(ValueError, var, 'a', (-1, ))

def test_num2point():
    assert_raises(TypeError, num2point, 1.0, [a, b])
    assert_raises(ValueError, num2point, -1, [a, b])
    assert_raises(ValueError, num2point, 4, [a, b])

    assert num2point(0x0, [a, b, c, d]) == {a: 0, b: 0, c: 0, d: 0}
    assert num2point(0x1, [a, b, c, d]) == {a: 1, b: 0, c: 0, d: 0}
    assert num2point(0x2, [a, b, c, d]) == {a: 0, b: 1, c: 0, d: 0}
    assert num2point(0x3, [a, b, c, d]) == {a: 1, b: 1, c: 0, d: 0}
    assert num2point(0x4, [a, b, c, d]) == {a: 0, b: 0, c: 1, d: 0}
    assert num2point(0x5, [a, b, c, d]) == {a: 1, b: 0, c: 1, d: 0}
    assert num2point(0x6, [a, b, c, d]) == {a: 0, b: 1, c: 1, d: 0}
    assert num2point(0x7, [a, b, c, d]) == {a: 1, b: 1, c: 1, d: 0}
    assert num2point(0x8, [a, b, c, d]) == {a: 0, b: 0, c: 0, d: 1}
    assert num2point(0x9, [a, b, c, d]) == {a: 1, b: 0, c: 0, d: 1}
    assert num2point(0xA, [a, b, c, d]) == {a: 0, b: 1, c: 0, d: 1}
    assert num2point(0xB, [a, b, c, d]) == {a: 1, b: 1, c: 0, d: 1}
    assert num2point(0xC, [a, b, c, d]) == {a: 0, b: 0, c: 1, d: 1}
    assert num2point(0xD, [a, b, c, d]) == {a: 1, b: 0, c: 1, d: 1}
    assert num2point(0xE, [a, b, c, d]) == {a: 0, b: 1, c: 1, d: 1}
    assert num2point(0xF, [a, b, c, d]) == {a: 1, b: 1, c: 1, d: 1}

def test_num2upoint():
    assert num2upoint(0x0, [a, b, c, d]) == ({aa, bb, cc, dd}, set())
    assert num2upoint(0x1, [a, b, c, d]) == ({bb, cc, dd}, {aa})
    assert num2upoint(0x2, [a, b, c, d]) == ({aa, cc, dd}, {bb})
    assert num2upoint(0x3, [a, b, c, d]) == ({cc, dd}, {aa, bb})
    assert num2upoint(0x4, [a, b, c, d]) == ({aa, bb, dd}, {cc})
    assert num2upoint(0x5, [a, b, c, d]) == ({bb, dd}, {aa, cc})
    assert num2upoint(0x6, [a, b, c, d]) == ({aa, dd}, {bb, cc})
    assert num2upoint(0x7, [a, b, c, d]) == ({dd}, {aa, bb, cc})
    assert num2upoint(0x8, [a, b, c, d]) == ({aa, bb, cc}, {dd})
    assert num2upoint(0x9, [a, b, c, d]) == ({bb, cc}, {aa, dd})
    assert num2upoint(0xA, [a, b, c, d]) == ({aa, cc}, {bb, dd})
    assert num2upoint(0xB, [a, b, c, d]) == ({cc}, {aa, bb, dd})
    assert num2upoint(0xC, [a, b, c, d]) == ({aa, bb}, {cc, dd})
    assert num2upoint(0xD, [a, b, c, d]) == ({bb}, {aa, cc, dd})
    assert num2upoint(0xE, [a, b, c, d]) == ({aa}, {bb, cc, dd})
    assert num2upoint(0xF, [a, b, c, d]) == (set(), {aa, bb, cc, dd})

def test_num2term():
    assert_raises(TypeError, num2term, 1.0, [a, b])
    assert_raises(ValueError, num2term, -1, [a, b])
    assert_raises(ValueError, num2term, 4, [a, b])

    assert num2term(0x0, [a, b, c, d], conj=False) == (~a, ~b, ~c, ~d)
    assert num2term(0x1, [a, b, c, d], conj=False) == ( a, ~b, ~c, ~d)
    assert num2term(0x2, [a, b, c, d], conj=False) == (~a,  b, ~c, ~d)
    assert num2term(0x3, [a, b, c, d], conj=False) == ( a,  b, ~c, ~d)
    assert num2term(0x4, [a, b, c, d], conj=False) == (~a, ~b,  c, ~d)
    assert num2term(0x5, [a, b, c, d], conj=False) == ( a, ~b,  c, ~d)
    assert num2term(0x6, [a, b, c, d], conj=False) == (~a,  b,  c, ~d)
    assert num2term(0x7, [a, b, c, d], conj=False) == ( a,  b,  c, ~d)
    assert num2term(0x8, [a, b, c, d], conj=False) == (~a, ~b, ~c,  d)
    assert num2term(0x9, [a, b, c, d], conj=False) == ( a, ~b, ~c,  d)
    assert num2term(0xA, [a, b, c, d], conj=False) == (~a,  b, ~c,  d)
    assert num2term(0xB, [a, b, c, d], conj=False) == ( a,  b, ~c,  d)
    assert num2term(0xC, [a, b, c, d], conj=False) == (~a, ~b,  c,  d)
    assert num2term(0xD, [a, b, c, d], conj=False) == ( a, ~b,  c,  d)
    assert num2term(0xE, [a, b, c, d], conj=False) == (~a,  b,  c,  d)
    assert num2term(0xF, [a, b, c, d], conj=False) == ( a,  b,  c,  d)

    assert num2term(0x0, [a, b, c, d], conj=True) == ( a,  b,  c,  d)
    assert num2term(0x1, [a, b, c, d], conj=True) == (~a,  b,  c,  d)
    assert num2term(0x2, [a, b, c, d], conj=True) == ( a, ~b,  c,  d)
    assert num2term(0x3, [a, b, c, d], conj=True) == (~a, ~b,  c,  d)
    assert num2term(0x4, [a, b, c, d], conj=True) == ( a,  b, ~c,  d)
    assert num2term(0x5, [a, b, c, d], conj=True) == (~a,  b, ~c,  d)
    assert num2term(0x6, [a, b, c, d], conj=True) == ( a, ~b, ~c,  d)
    assert num2term(0x7, [a, b, c, d], conj=True) == (~a, ~b, ~c,  d)
    assert num2term(0x8, [a, b, c, d], conj=True) == ( a,  b,  c, ~d)
    assert num2term(0x9, [a, b, c, d], conj=True) == (~a,  b,  c, ~d)
    assert num2term(0xA, [a, b, c, d], conj=True) == ( a, ~b,  c, ~d)
    assert num2term(0xB, [a, b, c, d], conj=True) == (~a, ~b,  c, ~d)
    assert num2term(0xC, [a, b, c, d], conj=True) == ( a,  b, ~c, ~d)
    assert num2term(0xD, [a, b, c, d], conj=True) == (~a,  b, ~c, ~d)
    assert num2term(0xE, [a, b, c, d], conj=True) == ( a, ~b, ~c, ~d)
    assert num2term(0xF, [a, b, c, d], conj=True) == (~a, ~b, ~c, ~d)

def test_point2upoint():
    assert point2upoint({a: 0, b: 0, c: 0, d: 0}) == ({aa, bb, cc, dd}, set())
    assert point2upoint({a: 1, b: 0, c: 0, d: 0}) == ({bb, cc, dd}, {aa})
    assert point2upoint({a: 0, b: 1, c: 0, d: 0}) == ({aa, cc, dd}, {bb})
    assert point2upoint({a: 1, b: 1, c: 0, d: 0}) == ({cc, dd}, {aa, bb})
    assert point2upoint({a: 0, b: 0, c: 1, d: 0}) == ({aa, bb, dd}, {cc})
    assert point2upoint({a: 1, b: 0, c: 1, d: 0}) == ({bb, dd}, {aa, cc})
    assert point2upoint({a: 0, b: 1, c: 1, d: 0}) == ({aa, dd}, {bb, cc})
    assert point2upoint({a: 1, b: 1, c: 1, d: 0}) == ({dd}, {aa, bb, cc})
    assert point2upoint({a: 0, b: 0, c: 0, d: 1}) == ({aa, bb, cc}, {dd})
    assert point2upoint({a: 1, b: 0, c: 0, d: 1}) == ({bb, cc}, {aa, dd})
    assert point2upoint({a: 0, b: 1, c: 0, d: 1}) == ({aa, cc}, {bb, dd})
    assert point2upoint({a: 1, b: 1, c: 0, d: 1}) == ({cc}, {aa, bb, dd})
    assert point2upoint({a: 0, b: 0, c: 1, d: 1}) == ({aa, bb}, {cc, dd})
    assert point2upoint({a: 1, b: 0, c: 1, d: 1}) == ({bb}, {aa, cc, dd})
    assert point2upoint({a: 0, b: 1, c: 1, d: 1}) == ({aa}, {bb, cc, dd})
    assert point2upoint({a: 1, b: 1, c: 1, d: 1}) == (set(), {aa, bb, cc, dd})

def test_point2term():
    assert set(point2term({a: 0, b: 0, c: 0, d: 0}, conj=False)) == {~a, ~b, ~c, ~d}
    assert set(point2term({a: 1, b: 0, c: 0, d: 0}, conj=False)) == { a, ~b, ~c, ~d}
    assert set(point2term({a: 0, b: 1, c: 0, d: 0}, conj=False)) == {~a,  b, ~c, ~d}
    assert set(point2term({a: 1, b: 1, c: 0, d: 0}, conj=False)) == { a,  b, ~c, ~d}
    assert set(point2term({a: 0, b: 0, c: 1, d: 0}, conj=False)) == {~a, ~b,  c, ~d}
    assert set(point2term({a: 1, b: 0, c: 1, d: 0}, conj=False)) == { a, ~b,  c, ~d}
    assert set(point2term({a: 0, b: 1, c: 1, d: 0}, conj=False)) == {~a,  b,  c, ~d}
    assert set(point2term({a: 1, b: 1, c: 1, d: 0}, conj=False)) == { a,  b,  c, ~d}
    assert set(point2term({a: 0, b: 0, c: 0, d: 1}, conj=False)) == {~a, ~b, ~c,  d}
    assert set(point2term({a: 1, b: 0, c: 0, d: 1}, conj=False)) == { a, ~b, ~c,  d}
    assert set(point2term({a: 0, b: 1, c: 0, d: 1}, conj=False)) == {~a,  b, ~c,  d}
    assert set(point2term({a: 1, b: 1, c: 0, d: 1}, conj=False)) == { a,  b, ~c,  d}
    assert set(point2term({a: 0, b: 0, c: 1, d: 1}, conj=False)) == {~a, ~b,  c,  d}
    assert set(point2term({a: 1, b: 0, c: 1, d: 1}, conj=False)) == { a, ~b,  c,  d}
    assert set(point2term({a: 0, b: 1, c: 1, d: 1}, conj=False)) == {~a,  b,  c,  d}
    assert set(point2term({a: 1, b: 1, c: 1, d: 1}, conj=False)) == { a,  b,  c,  d}

    assert set(point2term({a: 0, b: 0, c: 0, d: 0}, conj=True)) == { a,  b,  c,  d}
    assert set(point2term({a: 1, b: 0, c: 0, d: 0}, conj=True)) == {~a,  b,  c,  d}
    assert set(point2term({a: 0, b: 1, c: 0, d: 0}, conj=True)) == { a, ~b,  c,  d}
    assert set(point2term({a: 1, b: 1, c: 0, d: 0}, conj=True)) == {~a, ~b,  c,  d}
    assert set(point2term({a: 0, b: 0, c: 1, d: 0}, conj=True)) == { a,  b, ~c,  d}
    assert set(point2term({a: 1, b: 0, c: 1, d: 0}, conj=True)) == {~a,  b, ~c,  d}
    assert set(point2term({a: 0, b: 1, c: 1, d: 0}, conj=True)) == { a, ~b, ~c,  d}
    assert set(point2term({a: 1, b: 1, c: 1, d: 0}, conj=True)) == {~a, ~b, ~c,  d}
    assert set(point2term({a: 0, b: 0, c: 0, d: 1}, conj=True)) == { a,  b,  c, ~d}
    assert set(point2term({a: 1, b: 0, c: 0, d: 1}, conj=True)) == {~a,  b,  c, ~d}
    assert set(point2term({a: 0, b: 1, c: 0, d: 1}, conj=True)) == { a, ~b,  c, ~d}
    assert set(point2term({a: 1, b: 1, c: 0, d: 1}, conj=True)) == {~a, ~b,  c, ~d}
    assert set(point2term({a: 0, b: 0, c: 1, d: 1}, conj=True)) == { a,  b, ~c, ~d}
    assert set(point2term({a: 1, b: 0, c: 1, d: 1}, conj=True)) == {~a,  b, ~c, ~d}
    assert set(point2term({a: 0, b: 1, c: 1, d: 1}, conj=True)) == { a, ~b, ~c, ~d}
    assert set(point2term({a: 1, b: 1, c: 1, d: 1}, conj=True)) == {~a, ~b, ~c, ~d}

def test_iter_points():
    assert list(iter_points([a, b])) == [{a: 0, b: 0}, {a: 1, b: 0}, {a: 0, b: 1}, {a: 1, b: 1}]

def test_iter_upoints():
    assert list(iter_upoints([a, b])) == [({aa, bb}, set()), ({bb}, {aa}), ({aa}, {bb}), (set(), {aa, bb})]

def test_iter_terms():
    assert list(set(term) for term in iter_terms([a, b], conj=False)) == [{~a, ~b}, {a, ~b}, {~a, b}, {a, b}]
    assert list(set(term) for term in iter_terms([a, b], conj=True)) == [{a, b}, {~a, b}, {a, ~b}, {~a, ~b}]

