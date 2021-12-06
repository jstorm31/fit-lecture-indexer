# Compare an output to the reference test data

import argparse
import json
import os

from tqdm import tqdm
from indexer import LectureVideoIndexer, Stage, CropRegion
from utils.Intersector import Intersector

current_stage = None
test_videos_path = os.environ.get('TEST_VIDEO_PATH')


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

    # crop_region = CropRegion(0, 80, 890, 1700)

    indexer = LectureVideoIndexer(
        config=config, progress_callback=lambda stage, progress: handle_progress(bar, stage, progress))
    index = indexer.index(video_path=os.path.join(test_videos_path, ref_video['name']))
    seconds = [entry['second'] for entry in index]
    print(seconds)
    bar.close()

    # Intersection with a custom equivalence metric considering error in seconds
    intersector = Intersector(lambda x, y: abs(x - y) <= config['frame_step'])
    intersection_cnt = len(list(intersector.intersect(set(seconds), set(ref_video['index']))))
    precision = intersection_cnt / len(ref_video['index'])
    print(precision)
    return precision


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

    with open('test_data/reference.test.json') as json_data:
        test_data = json.load(json_data)

        for value in values:
            print(f"{observed_param} value: {value}")
            precisions = []

            config[observed_param] = value

            for video in test_data:
                index = compare_index(video, config)
                precisions.append(index)

            results.append({
                'value': value,
                'avg_precision': round(sum(precisions) / len(test_data), 3),
                'max_precision': max(precisions),
                'min_precision': min(precisions)
            })

    with open(f'output/{observed_param}_results.json', 'w') as output_file:
        json = json.dumps(results, indent=4)
        output_file.write(json)
