import argparse
import math
import os
import subprocess
import sys
import time
from threading import Timer
from typing import Callable

from utils import StartableBackgroundThread

parser = argparse.ArgumentParser(description="Minimal meditation CLI with a bell.")
parser.add_argument("-m", "--minutes", default=10, type=int, help="Total minutes to meditate. To have an open ended meditation, set to 0. Defaults to 10.")
parser.add_argument("-i", "--interval", default=2, type=int, help="Interval in minutes to ring meditation bell. Defaults to 2.")
args = parser.parse_args()

minutes = args.minutes * 60
interval = args.interval * 60


class MeditationTimer(StartableBackgroundThread):
    """Meditation Timer"""

    def __init__(self, total_time: int, interval_time: int):
        super().__init__()
        self._total_time = total_time
        self._time_spent_meditating = 0
        self._interval_time = interval_time
        self._interval_timer = None

    def _get_background_task_function(self) -> Callable:
        return self._timer

    def _timer(self):
        # Untimed meditation => Infinite timer
        if self._total_time == 0:
            while True:
                if self._interval_timer is None:
                    self._interval_timer = IntervalTimer(self._interval_time)
                    self._interval_timer.start()

                mins, seconds = divmod(self._time_spent_meditating, 60)
                timeformat = '{:02d}:{:02d}'.format(mins, seconds)
                os.system('clear')
                print(timeformat)
                time.sleep(1)
                self._time_spent_meditating += 1

        # Timed meditation
        while self._total_time:
            if self._interval_timer is None:
                self._interval_timer = IntervalTimer(self._interval_time)
                self._interval_timer.start()

            mins, seconds = divmod(self._total_time, 60)
            timeformat = '{:02d}:{:02d}'.format(mins, seconds)
            os.system('clear')
            print(timeformat)
            time.sleep(1)
            self._time_spent_meditating += 1
            self._total_time -= 1
        os.system('clear')
        print(f"Finished meditating for {math.floor(self._time_spent_meditating / 60)} minutes.")
        sys.exit()


class IntervalTimer(StartableBackgroundThread):
    """Interval Timer. Rings a bell after a given interval."""

    def __init__(self, interval_time: int):
        super().__init__(True)
        self._original_interval = interval_time
        self._remaining_interval_time = interval_time

    def _get_background_task_function(self) -> Callable:
        return self._interval_timer

    def _interval_timer(self):
        while self._remaining_interval_time:
            if self._remaining_interval_time == 1:
                time.sleep(1)
                bell_sound = PlayBellSound()
                bell_sound.start()
                self._remaining_interval_time = self._original_interval
            time.sleep(1)
            self._remaining_interval_time -= 1


class PlayBellSound(StartableBackgroundThread):
    """Plays the bell sound in a background process."""

    def __init__(self):
        super().__init__()
        self._audio_path = os.path.abspath("assets/bowl.mp3")

    def _get_background_task_function(self) -> Callable:
        return self._play_audio

    def _play_audio(self):
        subprocess.call(["afplay", self._audio_path])


meditation_timer = MeditationTimer(minutes, interval)
meditation_timer.start()
