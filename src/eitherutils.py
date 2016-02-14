
from pymonad.Either import Left, Right
from pymonad.Maybe import Nothing, Just
from taskutils import reject, resolve

def to_maybe(e):
  return Nothing if isinstance(e,Left) else Just(e.getValue())

def get_or_else(x):
  return x if isinstance(e,Left) else e.getValue()

def to_task(e):
  return reject(e.getValue()) if isinstance(e,Left) else resolve(e.getValue())

