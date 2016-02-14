#!/usr/bin/env bash

curdir="`dirname $0`"
cmd="$1"
shift

case $cmd in
  
  start)
    "${curdir}/start" $*
    ;;

  stop)
    "${curdir}/stop" $*
    ;;

  log)
    "${curdir}/log" $*
    ;;

esac
