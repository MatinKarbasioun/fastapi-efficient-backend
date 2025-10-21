from enum import Enum


class Gender(Enum, int):
    MALE = 0
    FEMALE = 1
    UNDEFINED = 2