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
