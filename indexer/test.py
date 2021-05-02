# Compare an output to the reference test data

import json
import os

from tqdm import tqdm
from LectureVideoIndexer import LectureVideoIndexer
from Stage import Stage
from VideoConverter import CropRegion

current_stage = None


def list_diff(li1, li2):
    return (list(list(set(li1) - set(li2)) + list(set(li2) - set(li1))))


def handle_progress(bar, stage: Stage, progress: float):
    if current_stage != stage:
        bar.set_description(str(stage))
    bar.update(progress - bar.n)


def compare_index(ref_video, treshold):
    print(f"Creating index for {ref_video['name']}")
    bar = tqdm(total=100)
    current_stage = None

    config = {'frame_step': 2, 'hash_size': 16, 'image_similarity_treshold': treshold}
    crop_region = CropRegion(0, 80, 890, 1700)

    indexer = LectureVideoIndexer(
        config=config, progress_callback=lambda stage, progress: handle_progress(bar, stage, progress))
    index = indexer.index(video_path=os.path.join('video', ref_video['name']), crop_region=crop_region)
    seconds = [entry['second'] for entry in index]
    print(seconds)
    bar.close()

    intersection_cnt = len(list(set(seconds).intersection(set(ref_video['index']))))
    precision = intersection_cnt / len(ref_video['index'])
    print(precision)
    return precision


if __name__ == '__main__':
    tresholds = [0.9]

    with open('src/test_data/reference.json') as json_data:
        test_data = json.load(json_data)

        for treshold in tresholds:
            print("Running treshold ", treshold)
            precisions = []

            for video in test_data:
                index = compare_index(video, treshold)
                precisions.append(index)

            avg_precision = sum(precisions) / len(test_data)

            with open('output/measurements.txt', 'a') as output_file:
                output_file.write(f"Treshold {treshold}: {round(avg_precision, 3)}\n")
