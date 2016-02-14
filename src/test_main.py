
from time import sleep
from datetime import datetime

from main import start, stop, log
from taskutils import resolve
from rsignal import mailbox, map

def print_rej(x):
  print "rejected-------"
  print str(x)
  print x

def print_res(x):
  print "resolved-------"
  print str(x)
  return x

def fork(task):
  return task.fork(print_rej, print_res)


(tasks,addr) = mailbox(resolve(None))
map(fork,tasks)

addr( start( datetime.utcnow(), "test", "can you hear me?" ) )

sleep(2)

addr( stop( datetime.utcnow() ) )

