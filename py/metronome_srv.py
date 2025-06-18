#!/usr/bin/env python3

from flask import Flask, request, jsonify
import threading
import time
import simpleaudio as sa
import os

app = Flask(__name__)

class Metronome:
    def __init__(self, bpm=120, click_sound="../opt/Synth_Square_E_hi.wav"):
        self.bpm = bpm
        self.beat_interval = 60.0 / bpm
        self.running = False
        self.thread = None
        self.click_wave = sa.WaveObject.from_wave_file(click_sound)

    def _run(self):
        try:
            os.sched_setaffinity(0, {0})
        except AttributeError:
            pass

        start_time = time.perf_counter()
        beat_count = 0

        while self.running:
            self.click_wave.play()
            beat_count += 1
            sleep_time = (start_time + beat_count * self.beat_interval) - time.perf_counter()
            if sleep_time > 0:
                time.sleep(sleep_time)
            else:
                print("⚠️ Behind schedule!")

    def start(self, bpm):
        if self.running:
            return
        self.bpm = bpm
        self.beat_interval = 60.0 / bpm
        self.running = True
        self.thread = threading.Thread(target=self._run, daemon=True)
        self.thread.start()

    def stop(self):
        self.running = False
        if self.thread:
            self.thread.join()
            self.thread = None

metronome = Metronome()

@app.route("/start", methods=["POST"])
def start():
    data = request.get_json()
    bpm = data.get("bpm", 120)
    metronome.start(bpm)
    return jsonify({"status": "started", "bpm": bpm})

@app.route("/stop", methods=["POST"])
def stop():
    metronome.stop()
    return jsonify({"status": "stopped"})

@app.route("/status", methods=["GET"])
def status():
    return jsonify({
        "running": metronome.running,
        "bpm": metronome.bpm if metronome.running else None
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

