from typing import NamedTuple


class Photo(NamedTuple):
    file_ur: str
    thumb_url: str
    resolution: tuple[int, int]
    