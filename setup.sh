#!/bin/bash

python3 -m venv venv
source venv/bin/activate
./venv/bin/pip install ipython
./my_virtual_env/bin/pip install ipykernel
./venv/bin/ipython kernel install --user --name=venv
jupyter lab