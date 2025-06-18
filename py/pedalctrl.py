#!/usr/bin/env python3

from gpiozero import DigitalInputDevice
from signal import pause
from pythonosc.udp_client import SimpleUDPClient
import time

# Mixer settings
MIXER_IP = "192.168.6.10"
MIXER_PORT = 10023
client = SimpleUDPClient(MIXER_IP, MIXER_PORT)

# Define switch pedal and OSC path
PEDALS = {
    21: ("Pedal Men", "/ch/24/mix/01/on"),   # GPIO 16
    4: ("Pedal Marcello", "/ch/24/mix/03/on"),
    16:("Pedal Adi", "/ch/24/mix/07/on"),  # Aux 5 to Bus 3

}

# Store switch objects and last event times
switches = {}
last_trigger_time = {}

# Debounce time in seconds
DEBOUNCE_INTERVAL = 0.3

def handle_switch_change(pin):
    now = time.time()
    if now - last_trigger_time.get(pin, 0) < DEBOUNCE_INTERVAL:
        return  # Skip if within debounce interval

    last_trigger_time[pin] = now
    label, path = PEDALS[pin]
    state = 1 if switches[pin].value else 0
    client.send_message(path, state)
    print(f"{label} -> {'Unmuted' if state == 1 else 'Muted'}")

# Set up each switch
for pin in PEDALS:
    try:
        switch = DigitalInputDevice(pin, pull_up=True, bounce_time=0.1)
        switches[pin] = switch
        last_trigger_time[pin] = 0
        switch.when_activated = lambda pin=pin: handle_switch_change(pin)
        switch.when_deactivated = lambda pin=pin: handle_switch_change(pin)
        print(f"✅ {PEDALS[pin][0]} connected as switch on GPIO{pin}")
    except Exception as e:
        print(f"❌ Failed to configure GPIO{pin}: {e}")

print("🎛️  Switch monitor running (gpiozero). Press Ctrl+C to exit.")
pause()

