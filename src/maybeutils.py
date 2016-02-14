
from pymonad.Reader import curry
from pymonad.Maybe import Nothing, Just

import taskutils

@curry
def with_default(val,maybe):
  return val if maybe == Nothing else maybe.getValue()

@curry
def to_task_reject(e,maybe):
  return to_task(taskutils.reject(e), maybe)

@curry
def to_task(t,maybe):
  return with_default(
    t,
    maybe.fmap( lambda x: taskutils.resolve(x) )
  )

