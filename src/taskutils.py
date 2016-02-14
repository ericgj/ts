from pymonad.Reader import curry
import pymonad.Either
import pymonad.Maybe

from task import Task

def reject(val):
  return Task( lambda rej,_: rej(val) )

resolve = Task.unit


def to_either(task):
  return task.bimap( Either.Left, Either.Right )

def to_maybe(task):
  return task.bimap( lambda _: Maybe.Nothing, Maybe.Just )

    
# TODO make parallel / immutable
# Python's scope rules make this a PITA

def all(tasks):
  def _alltask(rej,res):
    runstate = {
      'len': len(tasks),
      'result': [None]*len(tasks),
      'resolved': False
    }

    @curry
    def _rej(state,e):
      if state['resolved']:
        return None
      state['resolved'] = True
      rej(e)

    @curry
    def _res(state,x):
      if state['resolved']:
        return None
      state['result'][i] = x
      state['len'] = state['len'] - 1
      if state['len'] == 0:
        state['resolved'] = True
        res(state['result'])

    def _run(state,i,t):
      return t.fork(_rej(state), _res(state))

    if len(tasks) == 0:
      res([])
    else:
      for i,task in enumerate(tasks):
        _run(runstate,i,task)

  return Task(_alltask)


