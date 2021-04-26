import os
import shutil
import imagehash

from typing import Optional, Callable
from pathlib import Path
from ffmpeg_progress_yield import FfmpegProgress
from PIL import Image
from textdistance import hamming

from Config import Config
from Stage import Stage

FRAMES_DIR = 'frames'
FRAME_PREFIX = 'frame_'

VideoIndex = [int]


class LectureVideoIndexer:
    config = {
        'frame_step': 2,
        'image_similarity_treshold': 0.95,
        'hash_size': 16,
    }
    progress_callback = None

    def __init__(self,
                 config: Optional[Config] = None,
                 progress_callback: Callable[[Stage, float], None] = None):
        if config is not None:
            self.config = {**self.config, **config}
        if progress_callback is not None:
            self.progress_callback = progress_callback
        print("Config", self.config)

    def index(self, video_path: os.PathLike) -> VideoIndex:
        self.__clean()
        frames = self.__convert_to_frames(video_path)
        _, _, frames = next(os.walk(FRAMES_DIR))

        filtered_frames = self.__filter_similar_frames(frames_count=len(frames))
        return filtered_frames

    def __clean(self):
        dirpath = Path(FRAMES_DIR)

        if dirpath.exists() and dirpath.is_dir():
            shutil.rmtree(dirpath)
        dirpath.mkdir(parents=True, exist_ok=True)

    def __convert_to_frames(self, video_path: os.PathLike) -> [str]:
        cmd = [
            'ffmpeg', '-i', video_path, '-vf', f"fps=1,select='not(mod(t,{self.config['frame_step']}))",
            '-vsync', '0', '-frame_pts', '1',
            os.path.join(FRAMES_DIR, f'{FRAME_PREFIX}%d.png')
        ]

        ff = FfmpegProgress(cmd)
        for progress in ff.run_command_with_progress():
            if self.progress_callback is not None:
                self.progress_callback(Stage.CONVERTING_FRAMES, float(progress))

        _, _, frames = next(os.walk(FRAMES_DIR))
        return frames

    def __filter_similar_frames(self, frames_count: int) -> [int]:
        filtered_frames: [int] = [0]
        prev_frame = 0

        for frame in range(self.config['frame_step'], frames_count, self.config['frame_step']):
            frame_path = self.__create_frame_path(frame)
            similarity = self.__compare_images(self.__create_frame_path(prev_frame), frame_path)

            if (similarity < self.config['image_similarity_treshold']):
                filtered_frames.append(frame)
            prev_frame = frame

            progress = round((frame + 1) / frames_count * 100)
            self.progress_callback(Stage.FILTERING_FRAMES, progress)

        return filtered_frames

    def __compare_images(self, img_path_a: os.PathLike, img_path_b: os.PathLike) -> float:
        hash_a = imagehash.phash(Image.open(img_path_a), hash_size=self.config['hash_size'])
        hash_b = imagehash.phash(Image.open(img_path_b), hash_size=self.config['hash_size'])

        return hamming.normalized_similarity(str(hash_a), str(hash_b))

    def __create_frame_path(self, frame) -> str:
        return os.path.join(FRAMES_DIR, f"{FRAME_PREFIX}{frame}.png")
