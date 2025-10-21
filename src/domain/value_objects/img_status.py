from enum import Enum


class ImgStatus(Enum, int):
    PROCESSING = 0
    COMPLETED = 1
    FAILED = 2
