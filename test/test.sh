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
    
#remove parsetable and other generated files
cd ..
rm -rf *.pyc out.py parsetab.py parser.out
cd test/
rm -rf *.pyc out.py parsetab.py parser.out
cd testFiles/
rm *~
cd ..
NUMTESTS=$(ls -1 testFiles | wc -l)
#echo $numTests
COUNTER=0
TESTFILE="testFiles/test"
RESULTS="results/result"
ERROR="errors/error"
red='\e[0;31m'
grn='\e[0;32m'
NC='\e[0m' # No Color

while [ $COUNTER -lt $NUMTESTS ]; do
    
    TESTRESULT="TEST"
    EXT=$COUNTER".cz"
    
    #get first line of testfile
    FAIL_INTENT=$(head -n 1 $TESTFILE$EXT | grep "fail" | wc -l)

    cat $TESTFILE$EXT | python -W ignore testCozy.py 1>$RESULTS$COUNTER 2>$ERROR$COUNTER & 
    PID=$(ps -ef | grep testCozy | awk {'print$2'})
    PID=$(echo $PID | awk {'print $1'})
    sleep 0.9

    kill $PID 2>/dev/null 
    wait $PID 2>/dev/null

    FAILED=false

    #check if size of error file is greater than 0
    if [ -s $ERROR$COUNTER ]
    then
        FAILED=true
    fi

    if [[ $FAILED = true && $FAIL_INTENT -gt 0 ]]
    then
        TESTRESULT=$TESTRESULT$COUNTER${red}" FAILED "${grn}" [ SUPPOSED TO FAIL]"${NC}
    elif [ $FAILED = true ]
    then
        TESTRESULT=$TESTRESULT$COUNTER${red}" FAILED"${NC}
    else
        TESTRESULT=$TESTRESULT$COUNTER${grn}" SUCCESS"${NC}
    fi

    echo -e $TESTRESULT
    let COUNTER=$COUNTER+1
done


#python testCozy.py  > testoutput
