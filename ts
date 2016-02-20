#!/usr/bin/env bash

# ts=`date +%Y-%m-%dT%H:%M:%S`
ts=`date +%s`
tsdir="${HOME}/.ts"
jfile="${tsdir}/.ts-data"
tsfile="${tsdir}/ts-data"


function starttask {
  stoptask
  echo "$ts|$ts|$1|$2|0" > "${jfile}"
  echo "You are starting $1 : $2"
}


function shifttask {
  local val=${3:-0}
  local orig

  mkdir -p "${tsdir}"
  touch "${jfile}"

  IFS='|' read -ra orig < "${jfile}"
  
  if [ ! -z "${orig[1]}" ]; then
    stoptask  "${1}"        "${2}"        $((0-val))
    logtask   "${orig[2]}" "${orig[3]}"   $((val))
    starttask "${orig[2]}" "${orig[3]}"
  fi
}

function stoptask {
  local val=${3:-0}
  local parts

  mkdir -p "${tsdir}"
  touch "${jfile}"

  IFS='|' read -ra parts < "${jfile}"
  if [ ! -z "${parts[1]}" ]; then
    parts[1]="${ts}"
    parts[2]="${1:-${parts[2]}}"
    parts[3]="${2:-${parts[3]}}"
    parts[4]=$((${val} + ${parts[4]}))
    out=$(IFS='|'; echo "${parts[*]}")
    echo "$out"  >> "${tsfile}"
    echo "" > "${jfile}"
    local mins=$(( ((${parts[1]}-${parts[0]})/60) + parts[4] ))
    echo "You spent ${mins} minutes on ${parts[2]} : ${parts[3]}"
  fi
}

function canceltask {
  echo "" > "${jfile}"
}

function logtask {
  local val=${3:-0}

  mkdir -p "${tsdir}"

  echo "$ts|$ts|$1|$2|$val" >> "${tsfile}"
}

#-----------------------------------------------------------------------------

cmd="$1"
shift

case $cmd in
  
  start)
    starttask "$@"
    ;;

  stop)
    stoptask "" "$@"
    ;;

  shift)
    shifttask "$@"
    ;;

  log)
    logtask "$@"
    ;;

  cancel)
    canceltask
    ;;

esac


