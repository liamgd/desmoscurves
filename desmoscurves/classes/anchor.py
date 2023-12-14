import dataclasses

from .position import Position


@dataclasses.dataclass
class Anchor:
    reverse_handle: Position | None
    point: Position | None
    handle: Position | None
    ghost: bool = False
