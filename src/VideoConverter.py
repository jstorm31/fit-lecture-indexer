from os import path
import cv2 as cv
from os import PathLike, path
from typing import Callable
from collections import namedtuple

from constants import FRAMES_DIR, FRAME_PREFIX

CropRegion = namedtuple('CropRegion', 'x_from x_to y_from y_to')


class VideoConverter:
    frame_step: int
    progress_callback: Callable[[float], None]

    def __init__(self, frame_step: int = 1, progress_callback=lambda: None):
        self.frame_step = frame_step
        self.progress_callback = progress_callback

    def convert_to_frames(self, video_path: PathLike, crop_region: CropRegion = None):
        if not path.exists(video_path):
            raise Exception('Invalid input video path')

        video_capture = cv.VideoCapture(video_path)
        video_len = self.__get_video_length(video_path)

        second = 0
        success = self.__get_video_frame(video_capture, second, crop_region=crop_region)

        while success:
            second = second + self.frame_step
            success = self.__get_video_frame(video_capture, second, crop_region=crop_region)

            if self.progress_callback is not None:
                progress = round(second / video_len * 100)
                self.progress_callback(progress)

    def __get_video_frame(self, video_capture, second: int, crop_region: CropRegion = None):
        video_capture.set(cv.CAP_PROP_POS_MSEC, second * 1000)
        has_frames, frame = video_capture.read()

        if has_frames:
            if crop_region:
                frame = frame[crop_region.x_from:crop_region.x_to, crop_region.y_from:crop_region.y_to]

            output_path = path.join(FRAMES_DIR, f'{FRAME_PREFIX}{second}.png')
            cv.imwrite(output_path, frame)

        return has_frames

    def __get_video_length(self, video_path: PathLike):
        video_capture = cv.VideoCapture(video_path)

        frames = video_capture.get(cv.CAP_PROP_FRAME_COUNT)
        fps = int(video_capture.get(cv.CAP_PROP_FPS))

        return int(frames / fps)
