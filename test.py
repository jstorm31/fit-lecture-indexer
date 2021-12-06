# Compare an output to the reference test data

import argparse
import json
import os
import time

from tqdm import tqdm
from indexer import LectureVideoIndexer, Stage, CropRegion
from utils.Intersector import Intersector

current_stage = None
test_videos_path = os.environ.get('TEST_VIDEO_PATH')
EXTRA_FRAME_RATIO = 0.5


def list_diff(li1, li2):
    return (list(list(set(li1) - set(li2)) + list(set(li2) - set(li1))))


def handle_progress(bar, stage: Stage, progress: float):
    if current_stage != stage:
        bar.set_description(str(stage))
    bar.update(progress - bar.n)


def compare_index(ref_video, config):
    print(f"Creating index for {ref_video['name']}")
    bar = tqdm(total=100)
    current_stage = None

    crop_region = None
    if 'cropRegion' in ref_video:
        coordinates = ref_video['cropRegion']
        crop_region = CropRegion(coordinates[0], coordinates[1], coordinates[2], coordinates[3])

    indexer = LectureVideoIndexer(
        config=config, progress_callback=lambda stage, progress: handle_progress(bar, stage, progress))
    index = indexer.index(video_path=os.path.join(test_videos_path, ref_video['name']),
                          crop_region=crop_region)
    seconds = [entry['second'] for entry in index]
    bar.close()

    # Intersection with a custom equivalence metric considering error in seconds
    intersector = Intersector(lambda x, y: abs(x - y) <= config['frame_step'])
    intersection = intersector.intersect(set(seconds), set(ref_video['index']))

    intersection_set = set([x[0] for x in intersection])
    extra_frames = list(set(seconds) - intersection_set)
    missing_frames = list(set(ref_video['index']) - intersection_set)

    intersection_cnt = len(list(intersection))
    extra_frames_cnt = len(seconds) - intersection_cnt

    precision = (intersection_cnt - extra_frames_cnt * EXTRA_FRAME_RATIO) / len(ref_video['index'])

    if precision < 0:
        precision = 0

    print("Missing keyframes: ", missing_frames)
    print("Extra keyframes: ", extra_frames)
    print(f"Precision: {precision}\n")

    return {
        'video': ref_video['name'],
        'precision': precision,
        'missingTimestamps': missing_frames,
        'extraTimestamps': extra_frames,
    }


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--param', dest="param", help="Name of the observed config param", required=True)
    parser.add_argument('--values', dest="values", help="Comma separated values", required=True)

    args = parser.parse_args()
    observed_param = args.param

    values = [
        int(x) if observed_param == 'frame_step' or observed_param == 'hash_size' else float(x)
        for x in args.values.split(',')
    ]

    results = []

    config = {
        'frame_step': 2,
        'hash_size': 16,
        'image_similarity_threshold': 0.9,
        'text_similarity_treshold': 0.85
    }

    with open('test_data/reference.json') as json_data:
        test_data = json.load(json_data)

        for value in values:
            print(f"{observed_param} value: {value}")
            precisions = []
            local_results = []

            config[observed_param] = value

            for video in test_data:
                start = time.time()
                result = compare_index(video, config)
                end = time.time()
                precisions.append(result['precision'])
                local_results.append(result)

            results.append({
                'value': value,
                'avg_precision': round(sum(precisions) / len(test_data), 3),
                'max_precision': round(max(precisions), 3),
                'min_precision': round(min(precisions), 3),
                'time': round(end - start),
                'results': local_results
            })

    with open(f'output/{observed_param}_results.json', 'w') as output_file:
        json = json.dumps(results, indent=4)
        output_file.write(json)
