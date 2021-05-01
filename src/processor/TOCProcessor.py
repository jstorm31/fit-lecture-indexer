from typing import Optional
from strsimpy.normalized_levenshtein import NormalizedLevenshtein

from . import FrameProcessor
from Types import VideoIndexEntry, TableOfContents


class TOCProcessor(FrameProcessor):
    toc: TableOfContents
    current_slide: int = 0

    normalized_levenshtein = NormalizedLevenshtein()
    similarity_treshold: int

    def __init__(self, toc: TableOfContents, similarity_treshold: int):
        self.toc = toc
        self.similarity_treshold = similarity_treshold

    def process_frame(self, frame: int, title: str) -> Optional[VideoIndexEntry]:
        if title and self.current_slide < len(self.toc):
            expected_title: str = self.toc[self.current_slide]['title']
            similarity = self.normalized_levenshtein.similarity(expected_title, title)

            if similarity >= self.similarity_treshold:
                entry: VideoIndexEntry = {'second': frame, 'title': expected_title}
                self.current_slide += 1

                return entry

        return None
