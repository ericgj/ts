# functional toolbelt

from functools import reduce
from pymonad.Reader import curry

def identity(x):
  return x

def always(x):
  return lambda _: x

def fst((x,_)): 
  return x

def snd((_,x)): 
  return x

def flip(fn):
  def _fn(a,b,*args,**kwargs):
    return fn(b,a,*args,**kwargs)
  return curry(_fn)

@curry
def applyf(args,fn):
  return fn(*args)


def compose(*fns):
  if fns:
    pair = lambda f,g: lambda *a,**k: f(g(*a,**k))
    return reduce(pair, fns, identity)
  else:
    return identity

