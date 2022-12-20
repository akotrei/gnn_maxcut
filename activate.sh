#!/bin/bash

SOURCE=${BASH_SOURCE[0]}
while [ -L "$SOURCE" ]; do # resolve $SOURCE until the file is no longer a symlink
  DIR=$( cd -P "$( dirname "$SOURCE" )" >/dev/null 2>&1 && pwd )
  SOURCE=$(readlink "$SOURCE")
  [[ $SOURCE != /* ]] && SOURCE=$DIR/$SOURCE # if $SOURCE was a relative symlink, we need to resolve it relative to the path where the symlink file was located
done
DIR=$( cd -P "$( dirname "$SOURCE" )" >/dev/null 2>&1 && pwd )

export PYTHONPATH=${PYTHONPATH}:${DIR}

# create python virtual enviroment
if [ ! -d "$env" ]; then
  python3 -m venv env
  pip install -r requirements.txt
fi

# activate
source env/bin/activate

# install pip package Goemans-Williamson classical algorithm for MaxCut
# create python virtual enviroment
if [ ! -d "$quantumflow-qaoa" ]; then
  git clone https://github.com/rigetticomputing/quantumflow-qaoa.git
  cd quantumflow-qaoa
  pip install -r requirements.txt
fi


