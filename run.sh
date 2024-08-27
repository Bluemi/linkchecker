#!/bin/bash

case "$1" in
	r)
		shift
		python3 src/main.py "$@"
		;;
	i)
		shift
		python3 src/inspect_data.py "$@"
		;;
	*)
		echo "invalid argument"
		;;
esac
