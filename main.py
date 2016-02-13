
import csv
from collections import namedtuple

from pymonad.Maybe import Nothing, Just
from task import Task
from maybeutils import to_task
from taskutils import resolve, reject

from rsignal import mailbox

Entry = namedtuple('Entry', ['timestamp','action','value','category','description'])
logfile = '~/.ts.csv'

def start(ts,cat,desc=''):
  return resolve( Entry(ts,'START',0,cat,desc) )

def stop(ts,desc=''):
  def _stop_last(entry):
    return Entry(ts,'STOP',0, entry.category, 
                 desc if len(desc)>0 else entry.description)

  return ((log_getlast(logfile) >> 
            to_task(NothingStartedError()) ).fmap(
            _stop_last )
         )


def fork(t):
  t.fork(prtrej, prtres)

(sig,_) = mailbox(resolve(None))
map( lambda t: t >> log_append(logfile), sig )



#-----------------------------------------------------------

def log_getlast(logfile):
  def _get(rej,res):
    try:
      with open(logfile, 'rb') as f:
        ret = Nothing
         rdr = csv.reader(f)
        for row in rdr:
          ret = Just( Entry(*row) )
        res(ret)

    except Exception as e:
      rej(e)


@curry
def log_append(logfile,entry):
  def _append(rej,res):
    try:
      with open(logfile, 'wb') as f:
        wr = csv.writer(f, quoting=csv.QUOTE_MINIMAL)
        row = [part for part in entry]
        wr.writerow(row)
        res(row)

    except Exception as e:
      rej(e)

  return Task(_append)
