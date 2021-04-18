from typing import Optional
from os import PathLike
from pathlib import Path
import shutil
import ffmpeg

from Config import Config
from errors import ConvertFramesError

FRAMES_DIR = 'frames'
FRAME_PREFIX = 'frame_'

class LectureVideoIndexer:
    config = {
        'frameStep': 2
    }
    
    def __init__(self, config: Optional[Config] = None):
        if config is not None:
            self.config = config

    def index(self, videoPath: PathLike):
        self.__clean()
        self.__convertToFrames(videoPath)

    def __clean(self):
        dirpath = Path(FRAMES_DIR)

        if dirpath.exists() and dirpath.is_dir():
            shutil.rmtree(dirpath)
        dirpath.mkdir(parents=True, exist_ok=True)

    def __convertToFrames(self, videoPath: PathLike):
        process = (ffmpeg
            .input(videoPath)
            .output(
                f'{FRAMES_DIR}/{FRAME_PREFIX}%d.png',
                vf=f"fps=1,select='not(mod(t,{self.config['frameStep']}))",
                vsync='0',
                frame_pts='1'
            )
            .run_async(quiet=True, overwrite_output=True))
        process.wait()
