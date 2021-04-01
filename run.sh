#!/bin/bash

DIR="$(dirname "$(realpath $0)")"
echo $DIR

ENV_BIN_OR_SCRIPTS=$DIR/env/bin

if [[ ! -d $ENV_BIN_OR_SCRIPTS ]]
then
    echo $ENV_BIN_OR_SCRIPTS not found, testing /env/Scripts
    ENV_BIN_OR_SCRIPTS=$DIR/env/Scripts

    if [[ ! -d $ENV_BIN_OR_SCRIPTS ]]
    then
        echo $ENV_BIN_OR_SCRIPTS does not exist, cannot find virtual environment, exiting.
        exit 1
    fi
fi

echo Found virtual environment $ENV_BIN_OR_SCRIPTS

PYTHON=$ENV_BIN_OR_SCRIPTS/python
MAIN=$DIR/app.py

# Check if virtual environment exists
if [ ! -e $PYTHON ]; then
    echo "No virtual environment with python found"
    exit
fi

$PYTHON --version
$PYTHON $MAIN -i 0.0.0.0 -p 6969