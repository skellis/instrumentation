"""
.. module: rPiCameraB
   :platform: Windows
.. moduleauthor:: Scott R Ellis skellis@gmail.com>

Runs a Raspberry Pi Camera (B) Rev 2 on a Raspberry Pi 5

..
   This file is part of the pyFSRS app.

   This program is free software: you can redistribute it and/or modify
   it under the terms of the GNU General Public License as published by
   the Free Software Foundation, either version 3 of the License, or
   (at your option) any later version.

   This program is distributed in the hope that it will be useful,
   but WITHOUT ANY WARRANTY; without even the implied warranty of
   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
   GNU General Public License for more details.

   You should have received a copy of the GNU General Public License
   along with this program. If not, see <http://www.gnu.org/licenses/>.

   Copyright 2014-2025 Scott R Ellis skellis@gmail.com>.
"""
from __future__ import annotations
import time
import numpy as np
import core.FSRSModule as module
import argparse
from typing import Tuple
from picamera2 import Picamera2


def howMany():
    return 1
    
def configure_camera(p2: Picamera2, size: Tuple[int, int], fps: int, color: bool):
    """Configure Picamera2 for a fixed frame‑rate video stream."""
    fmt = "RGB888" if color else "YUV420"
    cfg = p2.create_video_configuration(main={"size": size, "format": fmt})
    p2.configure(cfg)

    # Force the sensor to deliver frames at exactly *fps*
    frame_duration_us = int(1e6 / fps)
    p2.set_controls({"FrameDurationLimits": (frame_duration_us, frame_duration_us)})
    p2.start()


class rPiCameraB(module.Input):
    def __init__(self):
        print("init")
        module.Input.__init__(self)
        parser = argparse.ArgumentParser(description="Continuous Picamera2 1‑D stream")
        parser.add_argument("--fps", type=int, default=46.34, help="Frames per second to capture & print")
        parser.add_argument("--res", default="1296x972", help="Resolution as WIDTHxHEIGHT (default 640x480)")
        parser.add_argument("--mono", action="store_true", help="Capture monochrome (use Y channel only)")
        self.args = parser.parse_args()
        self.width, self.height = map(int, self.args.res.lower().split("x"))
        self.picam = Picamera2()
        self.picam.sensor_modes
        configure_camera(self.picam, (self.width, self.height), self.args.fps, not self.args.mono)
        self.dt_target = 1.0 / self.args.fps
        self.name = "Raspberry Pi Camera (B)"

        # setup properties and convert dictionary to properties object
        prop = []
        prop.append({"label": "Phase Flip", "type": "choice", "value": 0, "choices": ["0 deg", "180 deg"]})
        self.parsePropertiesDict(prop)

    # return the band integral over the entire CCD using column 1
    def read(self):
        print("read")
        c, _, _ = self.readNframes(80)
        return c.sum() / float(len(c))

    # this is the camera function that returns a 3xN array containing the data from the camera driver
    # columns are: col2 / col3, col2, col3
    def readNframes(self, N, canQuit=None):
        try:
            while True:
                print("readNframes")
                t0 = time.perf_counter()
                # Capture latest frame (blocking until next frame is ready)
                frame = self.picam.capture_array("main")  # shape: (H, W, C) or (H, W)
                # Convert to grayscale if needed
                if not self.args.mono:
                    # Average RGB channels to a single intensity (float32) array
                    frame = frame.mean(axis=2)
                # Vertically bin by summing across rows → 1‑D profile of length W
                A = frame.sum(axis=0).astype(np.float32)
                elapsed = time.perf_counter() - t0
                if elapsed < self.dt_target:
                    time.sleep(dt_target - elapsed)
                return np.array([A,A,A])
        except KeyboardInterrupt:
            passs

    # this function is called when the application is shut down; do all the clean up here (close drivers, etc)
    def shutdown(self):
        self.updTimer.Stop()
        self.picam.stop()
