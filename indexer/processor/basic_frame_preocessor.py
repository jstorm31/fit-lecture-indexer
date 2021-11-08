from typing import Optional
from strsimpy.normalized_levenshtein import NormalizedLevenshtein

from . import FrameProcessor
from ..Types import VideoIndexEntry


class BasicFrameProcessor(FrameProcessor):
    prev_title: str = None
    normalized_levenshtein = NormalizedLevenshtein()
    similarity_treshold: int

    def __init__(self, similarity_treshold):
        self.similarity_treshold = similarity_treshold

    def process_frame(self, frame: int, title: str, text: str) -> Optional[VideoIndexEntry]:
        entry: VideoIndexEntry = None

        if self.prev_title and title:
            similarity = self.normalized_levenshtein.similarity(self.prev_title, title)

            if similarity < self.similarity_treshold:
                entry = {'second': frame, 'title': title, 'text': text}

        elif not self.prev_title and title:
            entry = {'second': frame, 'title': title, 'text': text}

        if title:
            self.prev_title = title

        return entry
