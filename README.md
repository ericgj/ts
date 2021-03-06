# ts

Yet another CLI timesheet app

## Logging time

### Log time already spent
    ts log "Project DEF" "Send data" 35

    
### Start time on task
    ts start "Project ABC" "Revise specs"

  
### Stop time on task
    ts stop

  - and change the description

        ts stop "Revise specs; ran into some questions, wrote back client"

  - and adjust the time (in minutes)
        
        ts stop "" -5

### Check time on current timed task
    ts check

### Cancel current timed task
    ts cancel


### Shift time
    ts shift Meeting "to resolve crisis" 3

Note: run this _after_ the interruption ends to split the time.  In this
example, we are saying the interrupting task (Meeting) started 3 minutes
after starting the task currently being timed. So, the time is logged for the
Meeting, minus 3 minutes. The current task is then restarted with 3 minutes
"credit".


## Reporting time

### List all logged time
    ts list

  - or by category
        
        ts list "Project ABC"

Note:
  - You can use regular expressions to filter the category.
  - The listing is not formatted in any way. Typically you will want to pipe it
    to a program that can do something useful with the data. See for example
    `ts select` below.


### Run a query on logged time
    ts select "Project DEF" some/query.sql

Note: 
  - This requires python and sqlite. 
  - Query files can be any set of SQL statements in sqlite syntax.
  - By default, the data is manipulated in-memory, but you can also persist 
    to an sqlite file by specifying an additional parameter:

        ts select "" some/query.sql data.sqlite

  - There is an example query file in `reporters/summary.sql`.


## Installation

    cd ~
    git clone git@github.com:ericgj/ts.git .ts
    cd .ts
    make mod

    # add ~/.ts to your $PATH as you please


## What it does

Timesheet records are added to the file `ts-data` as pipe (|) delimited fields:

  - Start time (Unix timestamp, i.e. seconds from epoch)
  - Stop time (Unix timestamp)
  - Category (e.g. "Project ABC")
  - Description
  - Minutes adjustment (specified in `stop` or `log`).

While time is started on a task, a temporary record is saved to `.ts-data`

Files are stored relative to wherever you install the script.

If you want to save data somewhere else, feel free to edit `ts`.


## License

The MIT License (MIT) Copyright (c) 2016 `Eric Gjertsen <ericgj72@gmail.com>`

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation the
rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
sell copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.

