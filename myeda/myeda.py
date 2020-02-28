#!/usr/bin/python3

# IMPORTS
from pyeda.inter import *
import collections
import qm
import sys
from termcolor import colored, cprint

# FUNCTIONS
def variables(f):
	ret=[]
	for i in sorted(f.inputs):
		#ret.append(str(i).replace('[','').replace(']',''))
		ret.append(str(i))
	return ret

def onset(f):
	ret=[]
	for d in list(f.satisfy_all()):
		od = collections.OrderedDict(reversed(sorted(d.items())))
		s = str(list(od.keys()))
		#ss = s.replace('[','').replace(']','').split(', ')
		ss = s.split(', ')

		l = list(od.values())
		ll = ''
		for li in l:
			ll=ll+str(li)
		ret.append(int(ll,2))
	return(ret)


def map_minterm(n,m,xs):
	mapping={}
	for i,c in enumerate(reversed(bin(m))):
		if (i==n):
			break
		if c=='1':
			mapping[xs[i]]=1
		elif c=='0':
			mapping[xs[i]]=0
		else: # b
			if i<n:
				for j in range(i,n):
					mapping[xs[j]]=0
				break
	return(mapping)

def bitstring2expr(bs,v):
	st=''
	ss=[]
	for bsi in bs:
		s=[]
		vi=0
		for bsj in reversed(bsi):
			if(bsj!='-'):
				if(bsj=='1'):
					s.append(v[vi])
				else:
					s.append('~'+v[vi])
			vi=vi+1
		st=' & '.join(s)
		ss.append(st)
	sst=' | '.join(ss)
	return(sst)

def cover_table(n,minterms,prime_implicants,xs):
	minterms=sorted(minterms)
	print('table \t'+'\t'.join(['m'+str(m) for m in minterms]))
	for i,p in enumerate(prime_implicants):
		print('p'+str(i),end=' \t')
		for m in minterms:
			mapping=map_minterm(n,m,xs)
			if(p.restrict(mapping)):
				print("X",end='')
			else:
				print(" ",end='')
			print("\t",end='')
		print()

def num2expr(num,vs):
	return expr('&'.join([ str(t) for t in num2term(num,vs)]))

def cover_condition(n,minterms,prime_implicants,vs):
	T=exprvar('t',len(prime_implicants))
	k=[]
	for m in minterms:
		mexpr = num2expr(m,vs)
		l=[]
		for i,p in enumerate(prime_implicants):
			mapping=map_minterm(n,m,vs)
			if p.restrict(mapping):
				l.append('t['+str(i)+']')
		k.append('('+'|'.join(l)+')')
	return expr('&'.join(k))

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

print("--- FUNCTION 1 (N=2) ---")
q=qm.QuineMcCluskey()
print("Variables for function g:")
Y = exprvars('y',2)
print(Y)
print("Expression for function g:")
g=expr('y[0]&~y[1] | ~y[0]&y[1] | y[0]&y[1]')
print(g)
print("Truth Table for g:")
gt=expr2truthtable(g)
print(gt)
print("Result of QM for g:")
gs=q.simplify(onset(gt))
print(gs)
print("Simplified version of g:")
ge=expr(bitstring2expr(gs,variables(gt)))
print(ge)
print("Cover Table of g:")
cover_table(2,onset(gt),ge.xs,Y)
print("Cover Condition for g (with all solutions):")
gc=cover_condition(2,onset(gt),ge.xs,Y)
print(gc)
print(list(gc.satisfy_all()))
print("Cube Diagram of g:")
print_cube(2,g,ge.xs,Y)

print("--- FUNCTION 2 (N=3) ---")
q=qm.QuineMcCluskey()
print("Variables for function f:")
X = exprvars('x', 3)
print("Truth Table for f:")
ft = truthtable(X, "00110101")
print(ft)
print("Expression for function f:")
f=truthtable2expr(ft)
print(f)
print("Result of QM for f:")
fs=q.simplify(onset(ft))
print(fs)
print("Simplified version of f:")
fe=expr(bitstring2expr(fs,variables(ft)))
print(fe)
print("Cover Table of f:")
cover_table(3,onset(ft),fe.xs,X)
print("Cover Condition for f (with all solutions):")
fc=cover_condition(3,onset(ft),fe.xs,X)
print(fc)
print(list(fc.satisfy_all()))
print("Cube Diagram of f:")
print_cube(3,f,fe.xs,X)

