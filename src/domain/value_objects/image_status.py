from enum import Enum


class ImageStatus(int, Enum):
    """ Represents the state of image processing processing."""
    PROCESSING = 0
    COMPLETED = 1
    FAILED = 2