from LectureVideoIndexer import LectureVideoIndexer
from Config import Config

if __name__ == '__main__':
    indexer = LectureVideoIndexer(config={ 'frameStep' : 2 })
    indexer.index('video/trimmed.mp4')
