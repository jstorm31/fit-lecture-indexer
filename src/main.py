import argparse

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
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', help='Input video', required=True)
    args = parser.parse_args()

    indexer = LectureVideoIndexer(progress_callback=handle_progress)

    bar = tqdm(total=100,)
    index = indexer.index(video_path=args.i)
    bar.close()
    print("Extracted index: ", index)
