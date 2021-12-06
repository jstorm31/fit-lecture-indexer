from typing import TypedDict


class Config(TypedDict):
    frame_step: int
    image_similarity_threshold: float
    text_similarity_threshold: float
    hash_size: int
