#!/bin/bash

sudo iptables -t nat -A PREROUTING -p tcp --dport 80 -j REDIRECT --to-ports 8501
$PWD/../venv/bin/streamlit run $PWD/../py/metronome_gui.py
