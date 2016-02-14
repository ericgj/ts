import sys
import traceback
import os.path
from datetime import datetime
import csv  # TODO unicodecsv
from collections import namedtuple

from pymonad.Maybe import Nothing, Just
from pymonad.Either import Left, Right
from pymonad.Reader import curry

from utils import always
from task import Task
from maybeutils import with_default, to_task
from eitherutils import to_task as either_to_task
from taskutils import resolve, reject, all

Entry = namedtuple('Entry', ['start','stop','category','description','value'])

class Err():
  def __init__(self, error, traceback):
    self.error = error
    self.traceback = traceback

  def __str__(self):
    return "%s\n%s" % (self.error, traceback.format_exc(self.traceback))

def err(e):
  return Err(e, sys.exc_info()[2])


tsfile = os.path.join(os.path.expanduser('~'), '.ts.csv')
tmpfile = os.path.join(os.path.expanduser('~'), '.ts-journal')

def start(t,cat,desc=''):
  return log_start(tmpfile, tsfile, Entry(t,t,cat,desc,0))

def stop(t,desc=''):
  return log_stop(tmpfile, tsfile, Entry(t,t,'',desc,0))

def log(t,cat,val,desc=''):
  return log_entry(tmpfile, Entry(t,t,cat,desc,val))


#-----------------------------------------------------------
def serialize_entry(e):
  return [ datetime.isoformat(e.start),
           datetime.isoformat(e.stop),
           e.category,
           e.description,
           str(e.value)
         ]

def deserialize_entry(parts):
  def _parse(d):
    return datetime.strptime(d,'%Y-%m-%dT%H:%M:%S.%f')

  try:
    return Right(
      Entry(
        _parse(parts[0]),
        _parse(parts[1]),
        parts[2],
        parts[3],
        int(parts[4])
      )
    )
  except ValueError as e:
    return Left(err(e))


#-----------------------------------------------------------

def log_start(tmp, ts, entry):
  initlogs = all([ log_init(tmp), log_init(ts) ])
  writestart = log_overwrite(tmp,entry)
  writestop = lambda last: log_stop(tmp,ts,last)

  return (
    ((((initlogs >>
          always(log_getlast(tmp))) >> 
          to_task(writestart)) >> 
          writestop)           >> 
          always(writestart))
  )

def log_stop(tmp, ts, entry):
  initlogs = all([ log_init(tmp), log_init(ts) ])
  def _write(last):
    stopentry = Entry(last.start, entry.stop, 
                      last.category, 
                      entry.description or last.description,
                      entry.value + last.value 
                )
    return log_append(ts, stopentry) 

  return (((initlogs >>
           always(log_getlast(tmp))) >>
           to_task(resolve(Nothing))) >>
           _write).fmap(Just)


def log_entry(ts, entry):
  return log_init(ts) >> always(log_append(ts, entry))


#-----------------------------------------------------------

def log_init(fname):
  def _init(rej,res):
    try:
      if os.path.exists(fname):
        res(Nothing)
      else:
        with open(fname, 'a+') as f:
          f.write('')
        res(Nothing)
    except Exception as e:
      rej(err(e))

  return Task(_init)


# String -> Task Error (Maybe Entry)
def log_getlast(fname):
  
  def _deserial(mrow):
    return with_default( 
      Right(Nothing), 
      mrow.fmap(compose(Just, deserialize_entry)) 
    )

  def _get(rej,res):
    try:
      ret = Nothing
      with open(fname, 'rb') as f:
        rdr = csv.reader(f)
        for row in rdr:
          ret = Just(row)
      res(ret)

    except Exception as e:
      rej(err(e))
   
  return Task(_get) >> compose(either_to_task, _deserial)


@curry
def log_append(fname,entry):
  return log_write(fname,False,entry)

@curry
def log_overwrite(fname,entry):
  return log_write(fname,True,entry)

@curry
def log_write(fname,ovr,entry):
  def _append(rej,res):
    try:
      with open(fname, 'wb' if ovr else 'ab' ) as f:
        wr = csv.writer(f, quoting=csv.QUOTE_MINIMAL)
        row = serialize_entry(entry)
        wr.writerow(row)
        res(entry)

    except Exception as e:
      rej(err(e))

  return Task(_append)

