#!/bin/bash

PYTHON=python3

cd tests
for TEST in *.bas; do
    TESTNAME=`basename $TEST .bas`
    echo -n "Running test ${TESTNAME//_/ }..."

    $PYTHON ../compiler.py $TEST
    java -cp . ${TESTNAME^} > $TESTNAME.output
    if [ -z "`cmp $TESTNAME.output $TESTNAME.expected`" ]; then
        echo -e "\e[1;32mOK\e[0m"
    else
        echo -e "\e[1;31mFailed\e[0m"
    fi
done
