#!/bin/bash

#create directories if they don't exist
if [ ! -d "testFiles" ]
then
    mkdir "testFiles"
fi

if [ ! -d "results" ]
then
    mkdir "results"
fi

if [ ! -d "errors" ]
then
    mkdir "errors"
fi

NUMTESTS=$(ls -1 testFiles | wc -l)
#echo $numTests
COUNTER=0
TESTFILE="testFiles/test"
RESULTS="results/result"
ERROR="errors/error"
TESTRESULT="TEST"

while [ $COUNTER -lt $NUMTESTS ]; do
    EXT=$COUNTER".cz"
    #get the return value
    RET=$(head -n 1 $TESTFILE$EXT)
    RET=${RET//#/}

    #stream everything but the first line into testCozy
    cat $TESTFILE$EXT | python testCozy.py 1>$RESULTS$COUNTER 2>$ERROR$COUNTER 
    FAILED=false

    #check if size of error file is greater than 0
    if [ -s $ERROR$COUNTER ]
    then
        FAILED=true
    fi

    if [ $FAILED = true ] 
    then
        TESTRESULT=$TESTRESULT$COUNTER" FAILED"
    else
        TESTRESULT=$TESTRESULT$COUNTER" SUCCESS"
    fi

    echo $TESTRESULT
    let COUNTER=$COUNTER+1
    
done


#python testCozy.py  > testoutput
