from termcolor import colored, cprint

def print_cube(n,f,prime_implicants,xs):
    if (n==2):
        if(n!=len(xs)):
            print('ERROR: invalid dimension!')
        colors = ['red','green','blue','gray']
        ex='|'
        ey='-'
        enx='|'
        eny='-'
        if len(prime_implicants)==1 and prime_implicants.is_one():
            ex=colored('|', colors[0])
            ey=colored('-', colors[0])
            enx=colored('|', colors[0])
            eny=colored('-', colors[0])
        elif len(prime_implicants)==1 and prime_implicants.is_zero():
            pass
        else:
            for i,p in enumerate(prime_implicants):
                c = colors[i]
                if p.restrict({xs[0]:1}).is_one():
                    ex=colored('|', c)
                if p.restrict({xs[1]:1}).is_one():
                    ey=colored('-', c)
                if p.restrict({xs[0]:0}).is_one():
                    enx=colored('|', c)
                if p.restrict({xs[1]:0}).is_one():
                    eny=colored('-', c)
        print('     ',end='')
        print(colored('01', 'magenta') if f.restrict({xs[0]:0, xs[1]:1})  else '01',end='')
        print(4*ey,end='')
        print(colored('11', 'magenta') if f.restrict({xs[0]:1, xs[1]:1})  else '11')
        print('     ',end='')
        print(enx,end='')
        print('      ',end='')
        print(ex)
        print('y    ',end='')
        print(enx,end='')
        print('      ',end='')
        print(ex)
        print('|    ',end='')
        print(enx,end='')
        print('      ',end='')
        print(ex)
        print('+-x  ',end='')
        print(colored('00', 'magenta') if f.restrict({xs[0]:0, xs[1]:0})  else '00',end='')
        print(4*eny,end='')
        print(colored('10', 'magenta')  if f.restrict({xs[0]:1, xs[1]:0})  else '10')
    elif (n==3):
        colors = ['red','green','blue','grey','yellow','white'] # TODO
        enxny='/'
        enxnz='|'
        enynz='-'
        enxy='/'
        enxz='|'
        enyz='-'
        exny='/'
        exnz='|'
        eynz='-'
        exy='/'
        exz='|'
        eyz='-'
        if len(prime_implicants)==1 and prime_implicants.is_one():
            ex=colored('|', colors[0])
            ey=colored('-', colors[0])
            enx=colored('|', colors[0])
            eny=colored('-', colors[0])
        elif len(prime_implicants)==1 and prime_implicants.is_zero():
            pass
        else:
            for i,p in enumerate(prime_implicants):
                c = colors[i]
                if p.restrict({xs[0]:1}).is_one():
                    ex=colored('|', c)
                if p.restrict({xs[1]:1}).is_one():
                    ey=colored('-', c)
                if p.restrict({xs[0]:0}).is_one():
                    enx=colored('|', c)
                if p.restrict({xs[1]:0}).is_one():
                    eny=colored('-', c)
                # x
                if p.restrict({xs[0]:1}).is_one():
                    exny=colored('/', c)
                    exnz=colored('|', c)
                    exy=colored('/', c)
                    exz=colored('|', c)
                # nx
                if p.restrict({xs[0]:0}).is_one():
                    enxny=colored('/', c)
                    enxnz=colored('|', c)
                    enxy=colored('/', c)
                    enxz=colored('|', c)
                # y
                if p.restrict({xs[1]:1}).is_one():
                    exy=colored('/', c)
                    eynz=colored('-', c)
                    enxy=colored('/', c)
                    enyz=colored('-', c)
                # ny
                if p.restrict({xs[1]:0}).is_one():
                    exny=colored('/', c)
                    enynz=colored('-', c)
                    enxny=colored('/', c)
                    enyz=colored('-', c)
                # z
                if p.restrict({xs[2]:1}).is_one():
                    exz=colored('|', c)
                    enxz=colored('|', c)
                    eyz=colored('-', c)
                    enyz=colored('-', c)
                # nz
                if p.restrict({xs[2]:0}).is_one():
                    exnz=colored('|', c)
                    enxnz=colored('|', c)
                    eynz=colored('-', c)
                    enynz=colored('-', c)
                # nxny
                if p.restrict({xs[0]:0,xs[1]:0}).is_one():
                    enxny=colored('/', c)
                # nxnz
                if p.restrict({xs[0]:0,xs[1]:0}).is_one():
                    enxnz=colored('|', c)
                # nynz
                if p.restrict({xs[1]:0,xs[2]:0}).is_one():
                                        enynz=colored('|-', c)
                # nxy
                if p.restrict({xs[0]:0,xs[1]:1}).is_one():
                                        enxy=colored('/', c)
                # nxz
                if p.restrict({xs[0]:0,xs[2]:1}).is_one():
                                        enxz=colored('|', c)
                # nyz
                if p.restrict({xs[1]:0,xs[2]:1}).is_one():
                                        enyz=colored('-', c)
                # xny
                if p.restrict({xs[0]:1,xs[1]:0}).is_one():
                                        exny=colored('/', c)
                # xnz
                if p.restrict({xs[0]:1,xs[2]:0}).is_one():
                                        exnz=colored('|', c)
                # ynz
                if p.restrict({xs[1]:1,xs[2]:0}).is_one():
                                        eynz=colored('-', c)
                # xy
                if p.restrict({xs[0]:1,xs[1]:1}).is_one():
                                        exy=colored('/', c)
                # xz
                if p.restrict({xs[0]:1,xs[2]:1}).is_one():
                                        exz=colored('|', c)
                # yz
                if p.restrict({xs[1]:1,xs[2]:1}).is_one():
                                        eyz=colored('-', c)
        print('        ',end='')
        print(colored('011', 'magenta') if f.restrict({xs[0]: 0, xs[1]:1, xs[2]:1}) else '011',end='')
        print(9*eyz,end='')
        print(colored('111', 'magenta') if f.restrict({xs[0]: 1, xs[1]:1, xs[2]:1}) else '111')
        print('\t',end='')
        print(enxy,end='')
        print(enxz,end='')
        print('          ',end='')
        print(exy,end='')
        print(exz)
        print('       ',end='')
        print(enxy,end='')
        print(' ',end='')
        print(enxz,end='')
        print('         ',end='')
        print(exy,end='')
        print(' ',end='')
        print(exz)
        print('      ',end='')
        print(enxy,end='')
        print('  ',end='')
        print(enxz,end='')
        print('        ',end='')
        print(exy,end='')
        print('  ',end='')
        print(exz)
        print('    ',end='')
        print(colored('010', 'magenta') if f.restrict({xs[0]: 0, xs[1]:1, xs[2]:0}) else '010',end='')
        print(9*eynz,end='')
        print(colored('110', 'magenta') if f.restrict({xs[0]: 1, xs[1]:1, xs[2]:0}) else '110',end='')
        print('  ',end='')
        print(exz)
        print('     ',end='')
        print(enxnz,end='')
        print('   ',end='')
        print(enxz,end='')
        print('       ',end='')
        print(exnz,end='')
        print('   ',end='')
        print(exz)
        print('     ',end='')
        print(enxnz,end='')
        print('   ',end='')
        print(enxz,end='')
        print('       ',end='')
        print(exnz,end='')
        print('   ',end='')
        print(exz)
        print('     ',end='')
        print(enxnz,end='')
        print('  ',end='')
        print(colored('001', 'magenta') if f.restrict({xs[0]: 0, xs[1]:0, xs[2]:1}) else '001',end='')
        print('------',end='')
        print(exnz,end='')
        print('--',end='')
        print(colored('101', 'magenta') if f.restrict({xs[0]: 1, xs[1]:0, xs[2]:1}) else '101')
        print('     ',end='')
        print(enxnz,end='')
        print('  ',end='')
        print(enxny,end='')
        print('        ',end='')
        print(exnz,end='')
        print('  ',end='')
        print(exny)
        print('y z  ',end='')
        print(enxnz,end='')
        print(' ',end='')
        print(enxny,end='')
        print('         ',end='')
        print(exnz,end='')
        print(' ',end='')
        print(exny)
        print('|/',end='')
        print('   ',end='')
        print(enxnz,end='')
        print(enxny,end='')
        print('          ',end='')
        print(exnz,end='')
        print(exny)
        print('+-x ',end='')
        print(colored('000', 'magenta') if f.restrict({xs[0]: 0, xs[1]:0, xs[2]:0}) else '000',end='')
        print('---------',end='')
        print(colored('100', 'magenta') if f.restrict({xs[0]: 1, xs[1]:0, xs[2]:0}) else '100')
    else:
        print("ERROR: Unsupported dimension: "+str(n))
