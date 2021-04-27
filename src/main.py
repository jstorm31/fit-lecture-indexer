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
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', help='Input video', required=True, type=str)
    parser.add_argument('--skip-converting',
                        dest='skip_converting',
                        action='store_true',
                        help='Skip converting video to frames',
                        required=False)
    parser.add_argument('--frame-step', dest='frame_step', help='Frame step', required=False, type=int)
    parser.add_argument('--hash-size',
                        dest='hash_size',
                        help='Number of bytes for image phash',
                        required=False,
                        type=int)
    parser.add_argument('--image-similarity-treshold',
                        dest='image_similarity_treshold',
                        help='Treshold two images are considered similar',
                        required=False,
                        type=float)
    parser.add_argument('--text-similarity-treshold',
                        dest='text_similarity_treshold',
                        help='Treshold two images are considered similar',
                        required=False,
                        type=float)
    args = parser.parse_args()

    # Index
    config: Config = {
        'frame_step': args.frame_step or 2,
        'hash_size': args.hash_size or 16,
        'image_similarity_treshold': args.image_similarity_treshold or 0.95,
        'text_similarity_treshold': args.text_similarity_treshold or 0.85,
    }
    indexer = LectureVideoIndexer(config=config, progress_callback=handle_progress)
    bar = tqdm(total=100)

    index = indexer.index(video_path=args.i, skip_converting=args.skip_converting)
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
