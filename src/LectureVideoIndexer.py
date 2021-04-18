from typing import Optional, Callable
from os import PathLike
from pathlib import Path
import shutil
from ffmpeg_progress_yield import FfmpegProgress

from Config import Config
from Stage import Stage

FRAMES_DIR = 'frames'
FRAME_PREFIX = 'frame_'


class LectureVideoIndexer:
    config = {
        'frameStep': 2
    }
    progressCallback = None
    
    def __init__(self, config: Optional[Config] = None, progressCallback: Callable[[Stage, float], None] = None):
        if config is not None:
            self.config = config
        if progressCallback is not None:
            self.progressCallback = progressCallback

    def index(self, videoPath: PathLike):
        self.__clean()
        self.__convertToFrames(videoPath)

    def __clean(self):
        dirpath = Path(FRAMES_DIR)

        if dirpath.exists() and dirpath.is_dir():
            shutil.rmtree(dirpath)
        dirpath.mkdir(parents=True, exist_ok=True)

    def __convertToFrames(self, videoPath: PathLike):
        cmd = [
            'ffmpeg',
            '-i', videoPath,
            '-vf', f"fps=1,select='not(mod(t,{self.config['frameStep']}))",
            '-vsync', '0',
            '-frame_pts', '1',
            f'{FRAMES_DIR}/{FRAME_PREFIX}%d.png'
        ]
        
        ff = FfmpegProgress(cmd)
        for progress in ff.run_command_with_progress():
            if self.progressCallback is not None:
                self.progressCallback(Stage.CONVERTING_FRAMES, float(progress))
