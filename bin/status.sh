

echo -n "metronome_gui: "
systemctl status --no-pager metronome_gui | grep "Active" | cut -d ":" -f2
echo -n "metronome_srv: "
systemctl status --no-pager metronome_srv | grep "Active" | cut -d ":" -f2
echo -n "metronome_pedalctrl: "
systemctl status --no-pager pedalctrl | grep "Active" | cut -d ":" -f2

