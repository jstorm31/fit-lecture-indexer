from tqdm import tqdm

from LectureVideoIndexer import LectureVideoIndexer
from Config import Config
from Stage import Stage

def handleProgress(stage: Stage, progress: float):
    bar.update(progress - bar.n)

if __name__ == '__main__':
    indexer = LectureVideoIndexer(config={ 'frameStep' : 2 }, progressCallback=handleProgress)

    bar = tqdm(total = 100)
    indexer.index('video/trimmed.mp4')
    bar.close()
