import dataclasses
import enum
import math
from typing import Any, Generator, List, Tuple

import pyperclip
from constant import (BEZIER_EQUATION, BEZIER_PARAMETRIC, BEZIER_SUM_EQUATION,
                      DRAG_TOLERANCE, HANDLE_RADIUS, LINE, LINE_EQUATION,
                      LINE_PARAMETRIC, POINT_RADIUS, SIZE, STEP_EQUATION)


@dataclasses.dataclass
class Position:
    x: float
    y: float

    @property
    def tup(self) -> Tuple:
        return self.x, self.y

    def print(self) -> None:
        print(f'x: {self.x}, y: {self.y}')

    def flip(self, other: 'Position') -> 'Position':
        new_position = Position(self.x * 2 - other.x, self.y * 2 - other.y)
        return new_position

    def convert(self, other: 'Position') -> None:
        self.x = other.x
        self.y = other.y


@dataclasses.dataclass
class Bounds:
    top: float
    bottom: float
    right: float
    left: float


@dataclasses.dataclass
class Formula:
    formula: str

    def save(self) -> None:
        pyperclip.copy(self.formula)
        print()
        print(self.formula)


@dataclasses.dataclass
class Positions:
    positions: List[Position] = dataclasses.field(default_factory=list)

    @property
    def length(self) -> int:
        return len(self.positions)

    @property
    def last(self) -> Position:
        return self.positions[-1]

    @property
    def bounds(self) -> Bounds:
        x_values, y_values = zip(
            *(position.tup for position in self.positions)
        )
        bounds = Bounds(
            max(y_values), min(y_values), max(x_values), min(x_values)
        )
        return bounds

    def add(self, position: Position) -> Position:
        self.positions.append(position)

    def clear(self) -> None:
        self.positions.clear()

    def collides(self, other: Position) -> bool:
        return self.positions and self.positions[-1].x == other.x

    def positions_to_formula(self) -> Formula:
        height = self.bounds.top - self.bounds.bottom
        width = self.bounds.left - self.bounds.right

        y_lines = []

        for i in range(len(self.positions) - 1):
            line = LINE.format(
                x1=(self.positions[i].x - self.bounds.left) / width + i,
                y1=(self.positions[i].y - self.bounds.bottom) / height,
                x2=(self.positions[i + 1].x - self.bounds.left) / width + i,
                y2=(self.positions[i + 1].y - self.bounds.bottom) / height,
            )
            y_lines.append(line)

        formula = (
            LINE_EQUATION
            + '\n'
            + LINE_PARAMETRIC.format(
                lines=' + '.join(y_lines),
                x_scale=10,
                y_scale=10,
                period=1,
            )
        )

        return Formula(formula)


class ClickType(enum.Enum):
    MOUSE = 1
    REMOVE = 2


class PointType(enum.Enum):
    REVERSE_HANDLE = 1
    POINT = 2
    HANDLE = 3


@dataclasses.dataclass
class Anchor:
    reverse_handle: Position | None
    point: Position | None
    handle: Position | None


class BezierCurve:
    def __init__(self) -> None:
        self.anchors: List[Anchor] = []
        self.dragging: Tuple[Anchor, PointType] | None = None

    def click(self, mouse: Position, click_type: ClickType) -> None:
        for anchor in self.anchors:
            if (
                anchor.reverse_handle
                and math.dist(mouse.tup, anchor.reverse_handle.tup)
                <= HANDLE_RADIUS + DRAG_TOLERANCE
            ):
                if click_type == ClickType.REMOVE:
                    self.anchors.remove(anchor)
                    return
                self.dragging = anchor, PointType.REVERSE_HANDLE
                break
            elif (
                anchor.point
                and math.dist(mouse.tup, anchor.point.tup)
                <= POINT_RADIUS + DRAG_TOLERANCE
            ):
                if click_type == ClickType.REMOVE:
                    self.anchors.remove(anchor)
                    return
                if anchor.handle and anchor.reverse_handle:
                    self.dragging = anchor, PointType.POINT
                break
            elif (
                anchor.handle
                and math.dist(mouse.tup, anchor.handle.tup)
                <= HANDLE_RADIUS + DRAG_TOLERANCE
            ):
                if click_type == ClickType.REMOVE:
                    self.anchors.remove(anchor)
                    return
                self.dragging = anchor, PointType.HANDLE
                break
        else:
            if click_type == ClickType.REMOVE:
                return
            self.add_anchor(mouse)

    def add_anchor(self, point: Position) -> None:
        if len(self.anchors) == 0:
            # Nothing yet; add anchor with point with no handles
            self.anchors.append(Anchor(None, point, None))
        elif len(self.anchors) == 1 and self.anchors[0].handle is None:
            # One point with no handles; set handle to mouse and reverse
            # handle to flipped
            self.anchors[0].handle = point
            self.anchors[0].reverse_handle = self.anchors[0].point.flip(point)
        elif self.anchors[-1].handle is not None:
            # Last anchor is complete; add new anchor with point
            self.anchors.append(Anchor(None, point, None))
        else:
            # Last anchor has point with no handles; set handle to mouse
            # and reverse handle to flipped
            self.anchors[-1].handle = point
            self.anchors[-1].reverse_handle = self.anchors[-1].point.flip(
                point
            )

    def motion(self, mouse: Position) -> None:
        if self.dragging is None:
            return

        anchor, point_type = self.dragging

        if point_type == PointType.POINT:
            offset_x = mouse.x - anchor.point.x
            offset_y = mouse.y - anchor.point.y
            anchor.reverse_handle.x += offset_x
            anchor.reverse_handle.y += offset_y
            anchor.handle.x += offset_x
            anchor.handle.y += offset_y
            anchor.point.convert(mouse)
        elif point_type == PointType.HANDLE:
            anchor.handle.convert(mouse)
            anchor.reverse_handle.convert(anchor.point.flip(mouse))
        elif point_type == PointType.REVERSE_HANDLE:
            anchor.reverse_handle.convert(mouse)
            anchor.handle.convert(anchor.point.flip(mouse))

    def quadruplets(
        self,
    ) -> Generator[List[Tuple[float, float]], Any, None]:
        if len(self.anchors) < 2 or not self.anchors[1].point:
            return

        last: Anchor = self.anchors[0]
        for anchor in self.anchors[1:]:
            if None in (anchor.reverse_handle, anchor.point):
                return

            quadruplet = [
                (position.x, position.y)
                for position in (
                    last.point,
                    last.handle,
                    anchor.reverse_handle,
                    anchor.point,
                )
            ]
            yield quadruplet
            last = anchor

    def curve_to_formula(self) -> Formula | None:
        if len(self.anchors) < 2 or not self.anchors[-1].handle:
            return

        formula = (
            STEP_EQUATION
            + '\n'
            + BEZIER_EQUATION
            + '\n'
            + BEZIER_SUM_EQUATION
            + '\n'
        )

        include_response = (
            input('Include setup formulae? (Y/N, default Y) ').strip().lower()
        )
        if include_response == 'n':
            formula = ''

        round_response = input('Round values to? (default 5) ').strip()
        round_places = int(round_response) if round_response.isdigit() else 5

        height_response = input(
            'Height of screen in Desmos units? (default 10.0) '
        ).strip()
        height = (
            float(height_response) if height_response.isdecimal() else 10.0
        )

        x_values, y_values = zip(
            *(
                position
                for quadruplet in self.quadruplets()
                for position in quadruplet[:-1]
            )
        )

        formula += (
            BEZIER_PARAMETRIC[0]
            + str(len(self.anchors) - 1)
            + BEZIER_PARAMETRIC[1]
            + ', '.join(
                str(
                    round(
                        (value - SIZE[0] / 2) / SIZE[1] * height,
                        round_places,
                    )
                )
                for value in x_values + (self.anchors[-1].point.x,)
            )
            + BEZIER_PARAMETRIC[2]
            + str(len(self.anchors) - 1)
            + BEZIER_PARAMETRIC[3]
            + ', '.join(
                str(round((0.5 - value / SIZE[1]) * height, round_places))
                for value in y_values + (self.anchors[-1].point.y,)
            )
            + BEZIER_PARAMETRIC[4]
        )
        return Formula(formula)
