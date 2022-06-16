#!/bin/bash
tmux kill-server
cd /root/project-ajw
git fetch && git reset origin/main --hard
source python3-virtualenv/bin/activate
pip install -r requirements.txt
tmux new -d 'flask run --host=0.0.0.0'
