# ts

Yet another CLI timesheet app

## Usage

    # Start time
    ts start "Project ABC" "Revise specs"

  
    # Stop time
    ts stop

    #   and change the description
    ts stop "Revise specs; ran into some questions, wrote back client"

    #   and adjust the time (in minutes)
    ts stop "" -5


    # Log time already spent
    ts log "Project DEF" "Send data" 35


    # Interrupt (shift) task currently working on
    ts shift Meeting "to resolve crisis"

    # Note: run this after the interruption ends to count the time towards the 
    # shifted task, and then restart time on the prior task.


## Installation

    cd ~
    git clone git@github.com:ericgj/ts.git .ts
    cd .ts
    make mod

    # add ~/.ts to your $PATH as you please


## What it does

Timesheet records are added to `~/.ts/ts-data` as pipe (|) delimited fields:

  - Start time (Unix timestamp, i.e. seconds from epoch)
  - Stop time (Unix timestamp)
  - Category (e.g. "Project ABC")
  - Description
  - Minutes adjustment (specified in `stop` or `log`).

While time is started on a task, a temporary record is saved to `~/.ts/.ts-data`

If you want to save data somewhere else, feel free to edit the scripts. They
are about 60 LOC in bash.


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

