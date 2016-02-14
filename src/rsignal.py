from datetime import datetime
from threading import Thread
from collections import namedtuple
from uuid import uuid4 as uuid

noop = lambda _: None
runtime = { 'inputs': [], 'updating': False }

# public

Mailbox = namedtuple('Mailbox', ['signal','address'])

def mailbox(value):
  def _rej(e):
    raise e
  def _send(v):
    async_task( lambda: notify(s.id,v) ).fork(_rej, noop)

  s = input(value)
  return Mailbox(signal=s, address=_send)

def map(fn, signal):
  return lift(fn, [signal])

def lift(fn, signals):
  def _refresh():
    return fn(*[s.value for s in signals])
  return Signal(_refresh, signals)

def foldp(fn, init, signal):
  def _notify(timestamp, pupdate, pid):
    if pupdate:
      s.value = fn(signal.value, s.value)
    for kid in s.kids:
      kid.notify(timestamp, pupdate, s.id)
  
  s = Signal(lambda: init, [signal])
  s.notify = _notify
  return s


# private

class AlreadyUpdating(Exception):
  def __str__(self):
    return "Already updating, please notify asynchronously"

def notify(targetid, value):
  if runtime['updating']:
    raise AlreadyUpdating()
  runtime['updating'] = True
  ts = datetime.now()
  for input in runtime['inputs']:
    input.notify(ts, targetid, value)
  runtime['updating'] = False

def input(value):
  def _notify(timestamp, targetid, v):
    update = (s.id == targetid)
    if update:
      s.value = v
    for kid in s.kids:
      kid.notify(timestamp, update, s.id)
    return update

  s = Signal(lambda: value, [])
  s.notify = _notify
  runtime['inputs'].append(s)
  return s


def build_notify(node, refresh):
  ctrl = { 'count': 0, 'update': False }
  nparents = len(node.parents)

  def _notify(timestamp, pupdate, pid):
    ctrl['count'] += 1
    ctrl['update'] = ctrl['update'] or pupdate
    if ctrl['count'] == nparents:
      if ctrl['update']:
        node.value = refresh()
      for kid in node.kids:
        kid.notify(timestamp, pupdate, node.id)
      ctrl['update'] = False
      ctrl['count'] = 0

  return _notify


def async_task(fn):
  def _callback(rej,res):
    def _run():
      try:
        fn()
      except Exception as e:
        rej(e)
    th = Thread(target=_run)
    th.start()
    th.join()  # block to allow IO to finish
    res(None)

  return Task( _callback )


class Signal():
  def __init__(self, refresh, parents=[]):
    self.id = uuid()
    self.value = refresh()
    self.parents = parents
    self.kids = []
    self.notify = build_notify(self,refresh)
    for p in parents:
      p.kids.append(self)


class Task():
  def __init__(self,fork):
    self.fork = fork

