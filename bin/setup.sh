#!/bin/bash

PIPS="streamlit gpiozero python-osc lgpio flask simpleaudio streamlit_autorefresh"

echo Setting up environment
cd ..
python3 -m venv venv
source venv/bin/activate

for i in $PIPS
do
  pip3 install $i
done


sudo ln -s /home/nbeglm/pedalctrl/etc/metronome_srv.service /etc/systemd/system/metronome_srv.service
sudo ln -s /home/nbeglm/pedalctrl/etc/metronome_gui.service /etc/systemd/system/metronome_gui.service
sudo ln -s /home/nbeglm/pedalctrl/etc/pedalctrl.service /etc/systemd/system/pedalctrl.service


sudo systemctl daemon-reexec
sudo systemctl daemon-reload

SRV="metronome_srv metronome_gui pedalctrl"

for i in $SRV
do
	sudo systemctl enable $i
	sudo systemctl start $i
done
