#!/bin/bash
if [ -z $2 ] 
then
    python runCozy.py -i $1
elif [ "$2" = "-o" ]
then
    OUTPUT=${1//.cz/}
    python runCozy.py -i $1 -o $OUTPUT
else
    echo "usage: ./CoZy <input .cz file> [-o]"
fi
