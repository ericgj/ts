#!/usr/bin/env bash

ts=`date +%Y-%m-%dT%H:%M:%S`
tsdir="${HOME}/.ts"
jfile="${tsdir}/.ts-data"
tsfile="${tsdir}/ts-data"


function start {
  mkdir -p "${tsdir}"

  echo "$ts|$ts|$1|$2|0" > "${jfile}"
}


function stop {
  val=${2:-0}

  mkdir -p "${tsdir}"
  touch "${jfile}"

  IFS='|' read -ra PARTS < "${jfile}"
  if [ ! -z "${PARTS[1]}" ]; then
    PARTS[1]="${ts}"
    PARTS[3]="${1:-${PARTS[3]}}"
    PARTS[4]=$((${val} + ${PARTS[4]}))
    out=$(IFS='|'; echo "${PARTS[*]}")
    echo "$out"  >> "${tsfile}"
    echo "" > "${jfile}"
    echo "Stopped ${PARTS[2]} : ${PARTS[3]}"
  else
    echo "No current task"
    exit 1
  fi
}


function log {
  val=${3:-0}

  mkdir -p "${tsdir}"

  echo "$ts|$ts|$1|$2|$val" >> "${tsfile}"
}

#-----------------------------------------------------------------------------

cmd="$1"
shift

case $cmd in
  
  start)
    start $*
    ;;

  stop)
    stop $*
    ;;

  log)
    log $*
    ;;

esac


