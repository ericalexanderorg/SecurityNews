#!/bin/bash

# CD to where actions/checkout adds code
cd "$GITHUB_WORKSPACE/ACTIONS/GET-RSS" || exit
echo "$PWD"
pip install -r job.requirements
python job.py