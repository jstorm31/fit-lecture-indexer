from typing import TypedDict


class Config(TypedDict):
    frame_step: int
    image_similarity_treshold: float
    text_similarity_treshold: float
    hash_size: int
