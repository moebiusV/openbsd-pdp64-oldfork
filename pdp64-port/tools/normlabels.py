import re,sys
t=open(sys.argv[1]).read(); m={}
def r(x):
    k=x.group(0)
    if k not in m: m[k]='.LN%d'%len(m)
    return m[k]
sys.stdout.write(re.sub(r'\.?\bL\d+\b',r,t))
