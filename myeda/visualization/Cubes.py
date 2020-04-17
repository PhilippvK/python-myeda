'''module docstring'''
from termcolor import colored, cprint


def print_cube(n, f, prime_implicants, xs):
    '''function docstring'''
    if n == 2:
        if n != len(xs):
            print('ERROR: invalid dimension!')
        colors = ['red', 'green', 'blue', 'gray']
        edge_x = '|'
        edge_y = '-'
        edge_nx = '|'
        edge_ny = '-'
        if len(prime_implicants) == 1 and prime_implicants.is_one():
            edge_x = colored('|', colors[0])
            edge_y = colored('-', colors[0])
            edge_nx = colored('|', colors[0])
            edge_ny = colored('-', colors[0])
        elif len(prime_implicants) == 1 and prime_implicants.is_zero():
            pass
        else:
            for i, p in enumerate(prime_implicants):
                color = colors[i]
                if p.restrict({xs[0]: 1}).is_one():
                    edge_x = colored('|', color)
                if p.restrict({xs[1]: 1}).is_one():
                    edge_y = colored('-', color)
                if p.restrict({xs[0]: 0}).is_one():
                    edge_nx = colored('|', color)
                if p.restrict({xs[1]: 0}).is_one():
                    edge_ny = colored('-', color)
        print('     ', end='')
        print(colored('01', 'magenta') if f.restrict(
            {xs[0]: 0, xs[1]: 1}) else '01', end='')
        print(4*edge_y, end='')
        print(colored('11', 'magenta') if f.restrict(
            {xs[0]: 1, xs[1]: 1}) else '11')
        print('     ', end='')
        print(edge_nx, end='')
        print('      ', end='')
        print(edge_x)
        print('y    ', end='')
        print(edge_nx, end='')
        print('      ', end='')
        print(edge_x)
        print('|    ', end='')
        print(edge_nx, end='')
        print('      ', end='')
        print(edge_x)
        print('+-x  ', end='')
        print(colored('00', 'magenta') if f.restrict(
            {xs[0]: 0, xs[1]: 0}) else '00', end='')
        print(4*edge_ny, end='')
        print(colored('10', 'magenta') if f.restrict(
            {xs[0]: 1, xs[1]: 0}) else '10')
    elif n == 3:
        colors = ['red', 'green', 'blue', 'grey', 'yellow', 'white']  # TODO
        edge_nxny = '/'
        edge_nxnz = '|'
        edge_nynz = '-'
        edge_nxy = '/'
        edge_nxz = '|'
        edge_nyz = '-'
        edge_xny = '/'
        edge_xnz = '|'
        edge_ynz = '-'
        edge_xy = '/'
        edge_xz = '|'
        edge_yz = '-'
        if len(prime_implicants) == 1 and prime_implicants.is_one():
            edge_x = colored('|', colors[0])
            edge_y = colored('-', colors[0])
            edge_nx = colored('|', colors[0])
            edge_ny = colored('-', colors[0])
        elif len(prime_implicants) == 1 and prime_implicants.is_zero():
            pass
        else:
            for i, p in enumerate(prime_implicants):
                color = colors[i]
                if p.restrict({xs[0]: 1}).is_one():
                    edge_x = colored('|', color)
                if p.restrict({xs[1]: 1}).is_one():
                    edge_y = colored('-', color)
                if p.restrict({xs[0]: 0}).is_one():
                    edge_nx = colored('|', color)
                if p.restrict({xs[1]: 0}).is_one():
                    edge_ny = colored('-', color)
                # x
                if p.restrict({xs[0]: 1}).is_one():
                    edge_xny = colored('/', color)
                    edge_xnz = colored('|', color)
                    edge_xy = colored('/', color)
                    edge_xz = colored('|', color)
                # nx
                if p.restrict({xs[0]: 0}).is_one():
                    edge_nxny = colored('/', color)
                    edge_nxnz = colored('|', color)
                    edge_nxy = colored('/', color)
                    edge_nxz = colored('|', color)
                # y
                if p.restrict({xs[1]: 1}).is_one():
                    edge_xy = colored('/', color)
                    edge_ynz = colored('-', color)
                    edge_nxy = colored('/', color)
                    edge_nyz = colored('-', color)
                # ny
                if p.restrict({xs[1]: 0}).is_one():
                    edge_xny = colored('/', color)
                    edge_nynz = colored('-', color)
                    edge_nxny = colored('/', color)
                    edge_nyz = colored('-', color)
                # z
                if p.restrict({xs[2]: 1}).is_one():
                    edge_xz = colored('|', color)
                    edge_nxz = colored('|', color)
                    edge_yz = colored('-', color)
                    edge_nyz = colored('-', color)
                # nz
                if p.restrict({xs[2]: 0}).is_one():
                    edge_xnz = colored('|', color)
                    edge_nxnz = colored('|', color)
                    edge_ynz = colored('-', color)
                    edge_nynz = colored('-', color)
                # nxny
                if p.restrict({xs[0]: 0, xs[1]: 0}).is_one():
                    edge_nxny = colored('/', color)
                # nxnz
                if p.restrict({xs[0]: 0, xs[1]: 0}).is_one():
                    edge_nxnz = colored('|', color)
                # nynz
                if p.restrict({xs[1]: 0, xs[2]: 0}).is_one():
                    edge_nynz = colored('|-', color)
                # nxy
                if p.restrict({xs[0]: 0, xs[1]: 1}).is_one():
                    edge_nxy = colored('/', color)
                # nxz
                if p.restrict({xs[0]: 0, xs[2]: 1}).is_one():
                    edge_nxz = colored('|', color)
                # nyz
                if p.restrict({xs[1]: 0, xs[2]: 1}).is_one():
                    edge_nyz = colored('-', color)
                # xny
                if p.restrict({xs[0]: 1, xs[1]: 0}).is_one():
                    edge_xny = colored('/', color)
                # xnz
                if p.restrict({xs[0]: 1, xs[2]: 0}).is_one():
                    edge_xnz = colored('|', color)
                # ynz
                if p.restrict({xs[1]: 1, xs[2]: 0}).is_one():
                    edge_ynz = colored('-', color)
                # xy
                if p.restrict({xs[0]: 1, xs[1]: 1}).is_one():
                    edge_xy = colored('/', color)
                # xz
                if p.restrict({xs[0]: 1, xs[2]: 1}).is_one():
                    edge_xz = colored('|', color)
                # yz
                if p.restrict({xs[1]: 1, xs[2]: 1}).is_one():
                    edge_yz = colored('-', color)
        print('        ', end='')
        print(colored('011', 'magenta') if f.restrict(
            {xs[0]: 0, xs[1]: 1, xs[2]: 1}) else '011', end='')
        print(9*edge_yz, end='')
        print(colored('111', 'magenta') if f.restrict(
            {xs[0]: 1, xs[1]: 1, xs[2]: 1}) else '111')
        print('\t', end='')
        print(edge_nxy, end='')
        print(edge_nxz, end='')
        print('          ', end='')
        print(edge_xy, end='')
        print(edge_xz)
        print('       ', end='')
        print(edge_nxy, end='')
        print(' ', end='')
        print(edge_nxz, end='')
        print('         ', end='')
        print(edge_xy, end='')
        print(' ', end='')
        print(edge_xz)
        print('      ', end='')
        print(edge_nxy, end='')
        print('  ', end='')
        print(edge_nxz, end='')
        print('        ', end='')
        print(edge_xy, end='')
        print('  ', end='')
        print(edge_xz)
        print('    ', end='')
        print(colored('010', 'magenta') if f.restrict(
            {xs[0]: 0, xs[1]: 1, xs[2]: 0}) else '010', end='')
        print(9*edge_ynz, end='')
        print(colored('110', 'magenta') if f.restrict(
            {xs[0]: 1, xs[1]: 1, xs[2]: 0}) else '110', end='')
        print('  ', end='')
        print(edge_xz)
        print('     ', end='')
        print(edge_nxnz, end='')
        print('   ', end='')
        print(edge_nxz, end='')
        print('       ', end='')
        print(edge_xnz, end='')
        print('   ', end='')
        print(edge_xz)
        print('     ', end='')
        print(edge_nxnz, end='')
        print('   ', end='')
        print(edge_nxz, end='')
        print('       ', end='')
        print(edge_xnz, end='')
        print('   ', end='')
        print(edge_xz)
        print('     ', end='')
        print(edge_nxnz, end='')
        print('  ', end='')
        print(colored('001', 'magenta') if f.restrict(
            {xs[0]: 0, xs[1]: 0, xs[2]: 1}) else '001', end='')
        print('------', end='')
        print(edge_xnz, end='')
        print('--', end='')
        print(colored('101', 'magenta') if f.restrict(
            {xs[0]: 1, xs[1]: 0, xs[2]: 1}) else '101')
        print('     ', end='')
        print(edge_nxnz, end='')
        print('  ', end='')
        print(edge_nxny, end='')
        print('        ', end='')
        print(edge_xnz, end='')
        print('  ', end='')
        print(edge_xny)
        print('y z  ', end='')
        print(edge_nxnz, end='')
        print(' ', end='')
        print(edge_nxny, end='')
        print('         ', end='')
        print(edge_xnz, end='')
        print(' ', end='')
        print(edge_xny)
        print('|/', end='')
        print('   ', end='')
        print(edge_nxnz, end='')
        print(edge_nxny, end='')
        print('          ', end='')
        print(edge_xnz, end='')
        print(edge_xny)
        print('+-x ', end='')
        print(colored('000', 'magenta') if f.restrict(
            {xs[0]: 0, xs[1]: 0, xs[2]: 0}) else '000', end='')
        print('---------', end='')
        print(colored('100', 'magenta') if f.restrict(
            {xs[0]: 1, xs[1]: 0, xs[2]: 0}) else '100')
    else:
        print("ERROR: Unsupported dimension: "+str(n))
