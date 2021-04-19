from tqdm import tqdm

from LectureVideoIndexer import LectureVideoIndexer
from Config import Config
from Stage import Stage

current_stage = None


def handle_progress(stage: Stage, progress: float):
    if current_stage != stage:
        bar.set_description(str(stage))
    bar.update(progress - bar.n)


if __name__ == '__main__':
    indexer = LectureVideoIndexer(progress_callback=handle_progress)

    bar = tqdm(total=100,)
    index = indexer.index('video/lecture3.mp4')
    bar.close()
    print("Extracted index: ", index)
