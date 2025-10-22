from dataclasses import dataclass

from domain.value_objects.ordering import Ordering


@dataclass(frozen=False)
class SortField:
    """Value Object for sorting field and order."""
    field: str
    order: Ordering