#!/usr/bin/env bash

# ts=`date +%Y-%m-%dT%H:%M:%S`
ts=`date +%s`
tsdir="${HOME}/.ts"
jfile="${tsdir}/.ts-data"
tsfile="${tsdir}/ts-data"


function start {
  stop
  echo "$ts|$ts|$1|$2|0" > "${jfile}"
  echo "You are starting $1 : $2"
}

function shifttask {
  mkdir -p "${tsdir}"
  touch "${jfile}"

  IFS='|' read -ra ps < "${jfile}"

  stop "$@"
  if [ ! -z "${ps[1]}" ]; then
    start "${ps[2]}" "${ps[3]}"
  fi
}

function stop {
  val=${3:-0}

  mkdir -p "${tsdir}"
  touch "${jfile}"

  IFS='|' read -ra PARTS < "${jfile}"
  if [ ! -z "${PARTS[1]}" ]; then
    PARTS[1]="${ts}"
    PARTS[2]="${1:-${PARTS[2]}}"
    PARTS[3]="${2:-${PARTS[3]}}"
    PARTS[4]=$((${val} + ${PARTS[4]}))
    out=$(IFS='|'; echo "${PARTS[*]}")
    echo "$out"  >> "${tsfile}"
    echo "" > "${jfile}"
    mins=$(( ((${PARTS[1]}-${PARTS[0]})/60) + PARTS[4] ))
    echo "You spent ${mins} minutes on ${PARTS[2]} : ${PARTS[3]}"
  fi
}

function cancel {
  echo "" > "${jfile}"
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
    start "$@"
    ;;

  stop)
    stop "" "$@"
    ;;

  shift)
    shifttask "$@"
    ;;

  log)
    log "$@"
    ;;

  cancel)
    cancel
    ;;

esac


