from typing import Optional, Tuple
from strsimpy.normalized_levenshtein import NormalizedLevenshtein

from . import FrameProcessor
from ..Types import VideoIndexEntry, TableOfContents


class TOCProcessor(FrameProcessor):
    toc: TableOfContents
    current_slide: int = 0

    normalized_levenshtein = NormalizedLevenshtein()
    similarity_treshold: int

    def __init__(self, toc: TableOfContents, similarity_treshold: int):
        self.toc = toc
        self.similarity_treshold = similarity_treshold

    def process_frame(self, frame: int, title: str, text: str) -> Optional[VideoIndexEntry]:
        if title and self.current_slide < len(self.toc):
            similarity, expected_title = self.__similarity(title, self.current_slide)

            if similarity >= self.similarity_treshold:
                entry: VideoIndexEntry = {'second': frame, 'title': expected_title, 'text': text}
                self.current_slide += 1
                return entry

            # Check also the next slide in case the current one has been missed
            if self.current_slide + 1 >= len(self.toc):
                similarity, expected_title = self.__similarity(title, self.current_slide + 1)

                if similarity >= self.similarity_treshold:
                    entry: VideoIndexEntry = {'second': frame, 'title': expected_title, 'text': text}
                    self.current_slide += 2
                    return entry

        return None

    def __similarity(self, title: str, slide_index: int) -> Tuple[float, str]:
        expected_title: str = self.toc[slide_index]['title']
        similarity = self.normalized_levenshtein.similarity(expected_title, title)

        return similarity, expected_title
