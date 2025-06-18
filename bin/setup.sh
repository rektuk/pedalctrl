#!/bin/bash

PIPS="streamlit gpiozero python-osc lgpio flask simpleaudio"

#if [ -d ../venv ]
#then
  echo ist da
#else
  echo Setting up environment
  cd ..
  python3 -m venv venv
  source venv/bin/activate

  for i in $PIPS
  do
    pip3 install $i
  done
#fi
