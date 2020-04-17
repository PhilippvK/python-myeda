'''helpers docstring'''
import collections


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


def variables(f):
    """Returns all variables if a boolean expression as list of strings"""
    ret = []
    for i in sorted(f.inputs):
        # ret.append(str(i).replace('[','').replace(']',''))
        ret.append(str(i))
    return ret
