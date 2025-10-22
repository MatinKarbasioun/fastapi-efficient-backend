from enum import Enum


class Ordering(str, Enum):
    """Value Object for sorting order."""
    ASC = "asc"
    DESC = "desc"