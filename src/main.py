import argparse
import shutil
import json
import os

from pathlib import Path
from tqdm import tqdm
from LectureVideoIndexer import LectureVideoIndexer
from Config import Config
from Stage import Stage

OUTPUT_DIR = 'output'
current_stage = None


def handle_progress(stage: Stage, progress: float):
    if current_stage != stage:
        bar.set_description(str(stage))
    bar.update(progress - bar.n)


if __name__ == '__main__':
    # Parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', help='Input video', required=True)
    args = parser.parse_args()

    # Index
    indexer = LectureVideoIndexer(progress_callback=handle_progress)
    bar = tqdm(total=100,)

    index = indexer.index(video_path=args.i)
    bar.close()

    # Output
    dirpath = Path(OUTPUT_DIR)
    video_name = args.i.split('/')[-1]
    video_name = video_name[0:video_name.index('.')]

    if not dirpath.exists():
        dirpath.mkdir()

    with open(os.path.join(OUTPUT_DIR, video_name + '.json'), 'w') as output_file:
        json.dump(index, output_file)
    print(f"Index saved to output/{video_name}.json")
