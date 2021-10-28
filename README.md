# Lecture video indexer

A python package for creating an index for lecture video - a list of timestamps of transitions between the lecture slides being presented. Provides both API and CLI.

## Table of contents

- [Installation](#installation)
- [Example](#example)
- [How it works](#how-it-works)
- [API](#api)
- [Run in Docker container](#run-in-docker-container)

## Installation

Required python version: >= 3.8

 1. Make sure `tesseract` binary is installed system-wise
 2. `pip install fit-lecture-indexer`

## Example

### API

```python
from indexer import LectureVideoIndexer

indexer = LectureVideoIndexer()
index = indexer.index(video_path='video/example.mp4')
print(index)
```

Example result

```json
[
    { "second": 4, "title": "Overview" },
    { "second": 244, "title": "Integration and Interoperability" },
    { "second": 312, "title": "Service Oriented Architecture" }
]

```

### CLI

In the package home directory:

```bash
python cli.py -i video/example.mp4
# or
python cli.py -h
```

## How it works

It converts the input video into image frames one frame every 2 seconds (configurable by parameter `frame_step`). Then follows two phases to identify transitions between different slides.

In the second phase it filters all similar frames with perceptual image hashing and comparison of the hashes. That quickly filters obvious duplicates.

In the last phase, for more precise results, it runs OCR on the filtered frames from the previous step and extracts a slide title (the first meaningful text on the image). For even better precision it is advised to provide a rectangle region of a slide of expected title location (parameter `crop_region`). The extracted title is then used for identification of slide transitions (changes of titles).

For the best precision, exact table of contents of the lecture can be provided as an input (see API for more info).

## API

### `LectureVideoIndexer(config: Config = default_config, progress_callback: ProgressCallback = None)`

A constructor for an object running the video indexing.

#### Config

```python
config: Config = {
    'frame_step': 2,
    'image_similarity_treshold': 0.9,
    'text_similarity_treshold': 0.85,
    'hash_size': 16,
}

indexer = LectureVideoIndexer(config=config)
```

| Parameter  | Description  | Default value |
|---|---|---|
| frame_step  |  Create a frame every X seconds of the video  | 2  |
| image_similarity_treshold  | Treshold two images are considered similar  | 0.9  |
| text_similarity_treshold  | Treshold two images are considered similar  |  0.85  |
| hash_size  | Number of bytes for image phash  | 16 |

#### `ProgressCallback`

Provide this callback to receive updates about current running stage and its progress in percent.

```python
from indexer import Stage

ProgressCallback = Callable[[Stage, float], None]

def handle_progress(stage: Stage, progress: float):
    print(stage, progress)
```

### `index(video_path: os.PathLike, skip_converting: bool = False, crop_region: CropRegion = None, toc: TableOfContents = None) -> VideoIndex`

A method to index an input video returning a `VideoIndex`. For tracking indexing progress, use `progress_callback` parameter when creating an instance of `LectureVideoIndexer`.

To set a custom directory for intermediary frames, use `FRAMES_DIR` environment variable. A one default is `frames`.

#### Parameters

| Parameter  | Description  | Default value |
|---|---|---|
| video_path  |  Path to the video file  | None  |
| skip_converting  | Skips conerting the video into frames. Useful when running the method multiple times or the conversion is executed externally.  | False |
| crop_region  | Crop region for frames a slide title is expected to be located. A tuple in format `(x_from, x_to, y_from, y_to)` where individual values are absolut value of pixels as integers. It improves both precision and performance. | None  |
| toc  | Path to a table of contents file in JSON format with array of slides titles. | None |

#### Example 

A TOC input file expecting 5 slides in the lecture.

```json
// Example toc.json
[
    { "title": "Overview" },
    { "title": "Compute Instances" },
    { "title": "Image" },
    { "title": "Autoscaling" },
    { "title": "Load Balancer" }
]
```

Usage
```python
from indexer import LectureVideoIndexer, CropRegion

indexer = LectureVideoIndexer()
index = indexer.index(video_path='video/example.mp4', crop_region=CropRegion(890, 1700, 0, 80), toc='toc.json')
```

Result

```json
[
    { "second": 4, "title": "Overview" },
    { "second": 62, "title": "Compute Instances" },
    { "second": 212, "title": "Image" },
    { "second": 342, "title": "Autoscaling" },
    { "second": 598, "title": "Load Balancer" }
]
```

## Run in Docker container

```bash
make build

# Runs bash in the container with mounted video folder
make run

python3 src/cli.py -i video/test.mp4
```
