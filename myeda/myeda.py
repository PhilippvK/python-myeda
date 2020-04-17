"""Original version of myEDA (single file, to be replaced!)"""

# IMPORTS
import collections
import qm
from pyeda.inter import expr, exprvar, num2term
#from termcolor import colored, cprint

# FUNCTIONS

def variables(f):
    """Returns all variables if a boolean expression as list of strings"""
    ret = []
    for i in sorted(f.inputs):
        # ret.append(str(i).replace('[','').replace(']',''))
        ret.append(str(i))
    return ret

def onset(f):
    """Return the 1-set as list of integers, DC not allowed"""
    ret = []
    for term in list(f.satisfy_all()):
        ordered = collections.OrderedDict(reversed(sorted(term.items())))

        literals = list(ordered.values())
        tmp_str = ''
        for literal in literals:
            tmp_str = tmp_str + str(literal)
        ret.append(int(tmp_str, 2))
    return ret

def map_minterm(n, minterm, xs):
    """Maps minterms of boolean functions"""
    mapping = {}
    for i, character in enumerate(reversed(bin(minterm))):
        if i == n:
            break
        if character == '1':
            mapping[xs[i]] = 1
        elif character == '0':
            mapping[xs[i]] = 0
        else:  # b
            if i < n:
                for j in range(i, n):
                    mapping[xs[j]] = 0
                break
    return mapping

def bitstring2expr(bitstrings, variable_list):
    """Converts List of Bitstrings to Boolean expressions"""
    string = ''
    ret_list = []
    for bitstring in bitstrings:
        tmp_list = []
        var = 0
        for character in reversed(bitstring):
            if character != '-':
                if character == '1':
                    tmp_list.append(variable_list[var])
                else:
                    tmp_list.append('~' + variable_list[var])
            var = var + 1
        term = ' & '.join(tmp_list)
        ret_list.append(term)
    ret = ' | '.join(ret_list)
    return ret

def cover_table(n, minterms, prime_implicants, xs):
    '''Prints a cover table of a ?'''
    minterms = sorted(minterms)
    print('table \t'+'\t'.join(['m'+str(min) for min in minterms]))
    for i, prime_implicant in enumerate(prime_implicants):
        print('p'+str(i), end=' \t')
        for minterm in minterms:
            mapping = map_minterm(n, minterm, xs)
            if prime_implicant.restrict(mapping):
                print("X", end='')
            else:
                print(" ", end='')
            print("\t", end='')
        print()

def num2expr(num, vs):
    '''Convert a decimal number to a boolean expression'''
    return expr('&'.join([str(term) for term in num2term(num, vs)]))


def cover_condition(n, minterms, prime_implicants, vs):
    '''Return a boolean function for the cover condition'''
    _ = exprvar('t', len(prime_implicants))
    ret_list = []
    for minterm in minterms:
        minterm_expr = num2expr(minterm, vs)
        tmp_list = []
        for i, prime_implicant in enumerate(prime_implicants):
            mapping = map_minterm(n, minterm, vs)
            if prime_implicant.restrict(mapping):
                tmp_list.append('t['+str(i)+']')
        ret_list.append('('+'|'.join(tmp_list)+')')
    return expr('&'.join(ret_list))


#print("--- FUNCTION 1 (N=2) ---")
#q = qm.QuineMcCluskey()
#print("Variables for function g:")
#Y = exprvars('y', 2)
#print(Y)
#print("Expression for function g:")
#g = expr('y[0]&~y[1] | ~y[0]&y[1] | y[0]&y[1]')
#print(g)
#print("Truth Table for g:")
#gt = expr2truthtable(g)
#print(gt)
#print("Result of QM for g:")
#gs = q.simplify(onset(gt))
#print(gs)
#print("Simplified version of g:")
#ge = expr(bitstring2expr(gs, variables(gt)))
#print(ge)
#print("Cover Table of g:")
#cover_table(2, onset(gt), ge.xs, Y)
#print("Cover Condition for g (with all solutions):")
#gc = cover_condition(2, onset(gt), ge.xs, Y)
#print(gc)
#print(list(gc.satisfy_all()))
#print("Cube Diagram of g:")
#print_cube(2, g, ge.xs, Y)

#print("--- FUNCTION 2 (N=3) ---")
#q = qm.QuineMcCluskey()
#print("Variables for function f:")
#X = exprvars('x', 3)
#print("Truth Table for f:")
#ft = truthtable(X, "00110101")
#print(ft)
#print("Expression for function f:")
#func = truthtable2expr(ft)
#print(func)
#print("Result of QM for f:")
#fs = q.simplify(onset(ft))
#print(fs)
#print("Simplified version of f:")
#fe = expr(bitstring2expr(fs, variables(ft)))
#print(fe)
#print("Cover Table of f:")
#cover_table(3, onset(ft), fe.xs, X)
#print("Cover Condition for f (with all solutions):")
#fc = cover_condition(3, onset(ft), fe.xs, X)
#print(fc)
#print(list(fc.satisfy_all()))
#print("Cube Diagram of f:")
#print_cube(3, func, fe.xs, X)
