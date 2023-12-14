import dataclasses
from typing import Tuple

from ..constant import SIZE


@dataclasses.dataclass
class Position:
    x: float
    y: float

    @staticmethod
    def lerp(
        position_a: 'Position', position_b: 'Position', amount: float
    ) -> 'Position':
        x_diff = position_b.x - position_a.x
        y_diff = position_b.y - position_a.y
        new_x = position_a.x + x_diff * amount
        new_y = position_a.y + y_diff * amount
        return Position(new_x, new_y)

    @property
    def tup(self) -> Tuple:
        return self.x, self.y

    def copy(self) -> 'Position':
        return Position(self.x, self.y)

    def print(self) -> None:
        print(f'x: {self.x}, y: {self.y}')

    def flip(self, other: 'Position') -> 'Position':
        new_position = Position(self.x * 2 - other.x, self.y * 2 - other.y)
        return new_position

    def convert(self, other: 'Position') -> None:
        self.x = other.x
        self.y = other.y

    def centered(
        self,
        center: 'Position',
        zoom: float | int,
        reverse: bool = False,
    ) -> 'Position':
        # multiplier = -1 if reverse else 1
        if reverse:
            return Position(
                ((self.x - SIZE[0] / 2) / zoom - center.x + (SIZE[0] / 2)),
                ((self.y - SIZE[1] / 2) / zoom - center.y + (SIZE[1] / 2)),
            )
        else:
            return Position(
                (self.x + center.x - (SIZE[0] / 2)) * zoom + SIZE[0] / 2,
                (self.y + center.y - (SIZE[1] / 2)) * zoom + SIZE[1] / 2,
            )
