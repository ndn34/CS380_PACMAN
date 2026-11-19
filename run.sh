#!/bin/sh
if [ "$#" -eq 4 ]; then
    python3 main.py "$1" "$2" "$3" "$4"
elif [ "$#" -eq 3 ]; then
    python3 main.py "$1" "$2" "$3"
elif [ "$#" -eq 2 ]; then
    python3 main.py "$1" "$2"
else
    python3 main.py "$1"
fi

