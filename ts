#!/usr/bin/env bash

cmd="$1"
shift

case $cmd in
  
  start)
    ./start $*
    ;;

  stop)
    ./stop $*
    ;;

  log)
    ./log $*
    ;;

esac
