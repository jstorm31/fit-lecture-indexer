from LectureVideoIndexer import LectureVideoIndexer

from Config import Config
from Stage import Stage

def handleProgress(stage: Stage, progress: float):
    print("Progress: ", progress)

if __name__ == '__main__':
    indexer = LectureVideoIndexer(config={ 'frameStep' : 2 }, progressCallback=handleProgress)
    indexer.index('video/trimmed.mp4')
