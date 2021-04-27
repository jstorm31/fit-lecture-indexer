import cv2 as cv
from os import PathLike, path
from typing import Callable

from constants import FRAMES_DIR, FRAME_PREFIX


class VideoConverter:
    frame_step: int
    progress_callback: Callable[[float], None]

    def __init__(self, frame_step: int = 1, progress_callback=lambda: None):
        self.frame_step = frame_step
        self.progress_callback = progress_callback

    def convert_to_frames(self, video_path: PathLike):
        video_capture = cv.VideoCapture(video_path)
        video_len = self.__get_video_length(video_path)

        second = 0
        success = self.__get_video_frame(video_capture, second)

        while success:
            second = second + self.frame_step
            success = self.__get_video_frame(video_capture, second)

            if self.progress_callback is not None:
                progress = round(second / video_len * 100)
                self.progress_callback(progress)

    def __get_video_frame(self, video_capture, second: int):
        video_capture.set(cv.CAP_PROP_POS_MSEC, second * 1000)
        has_frames, image = video_capture.read()

        if has_frames:
            output_path = path.join(FRAMES_DIR, f'{FRAME_PREFIX}{second}.png')
            cv.imwrite(output_path, image)

        return has_frames

    def __get_video_length(self, video_path: PathLike):
        video_capture = cv.VideoCapture(video_path)

        frames = video_capture.get(cv.CAP_PROP_FRAME_COUNT)
        fps = int(video_capture.get(cv.CAP_PROP_FPS))

        return int(frames / fps)