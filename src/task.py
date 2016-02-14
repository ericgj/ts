
from pymonad.Monad import *

class Task(Monad):

  def __init__(self, computation):
    self.fork = computation

  def __mult__(self,fn):
    return self.fmap(fn)

  def fmap(self, fn):
    def _mapfn(rej,res):
      return self.fork( lambda a: rej(a),  lambda b: res(fn(b)) )
    return Task(_mapfn) 
  
  def bind(self, fn):
    def _bindfn(rej,res):
      return self.fork( lambda a: rej(a),  lambda b: fn(b).fork(rej,res) )
    return Task(_bindfn)
  
  def amap(self, fvalue):
    return self.bind( lambda f: fvalue.fmap(f) ) 
  
  def bimap(self,rejfn,resfn):
    def _bimapfn(rej,res):
      return self.fork( lambda a: rej(rejfn(a)), lambda b: res(resfn(b)) )
    return Task(_bimapfn)

  @classmethod
  def unit(cls, value):
    return Task( lambda _,res: res(value) )

