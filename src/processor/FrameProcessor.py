from abc import ABC, abstractmethod
from typing import Optional

from Types import VideoIndexEntry


class FrameProcessor(ABC):

    @abstractmethod
    def process_frame(self, frame: int, title: str) -> Optional[VideoIndexEntry]:
        pass
