#!/bin/bash

tmux kill-server

cd ~/mlh/project-triple-7/

git fetch && git reset origin/main -hard

source python3-virtualenv/bin/activate
pip install -r requirements.txt
tmux new-session -d -s mysession
