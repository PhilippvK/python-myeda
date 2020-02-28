import collections

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

def variables(f):
	ret=[]
	for i in sorted(f.inputs):
		#ret.append(str(i).replace('[','').replace(']',''))
		ret.append(str(i))
	return ret