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
    parser.add_argument('-i', help='Input video', required=True, type=str)
    parser.add_argument('--frame_step', help='Frame step', required=False, type=int)
    parser.add_argument('--hash_size', help='Number of bytes for image phash', required=False, type=int)
    parser.add_argument('--similarity_treshold',
                        help='Treshold two images are considered similar',
                        required=False,
                        type=float)
    args = parser.parse_args()

    # Index
    config: Config = {
        'frame_step': args.frame_step or 2,
        'hash_size': args.hash_size or 16,
        'image_similarity_treshold': args.similarity_treshold or 0.95
    }
    print("Received config", config)
    indexer = LectureVideoIndexer(config=config, progress_callback=handle_progress)
    bar = tqdm(total=100)

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
