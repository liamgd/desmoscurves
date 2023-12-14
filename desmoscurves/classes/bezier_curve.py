import dataclasses
import json
import math
import os
from typing import Any, Dict, Generator, List, Tuple

import dacite

from ..constant import (
    BEZIER_EQUATION,
    BEZIER_PARAMETRIC,
    BEZIER_SUM_EQUATION,
    DRAG_TOLERANCE,
    GHOST_EQUATION,
    HANDLE_RADIUS,
    MAX_SAVES,
    NEW_HANDLE_RADIUS,
    POINT_RADIUS,
    SIZE,
    STEP_EQUATION,
    UNSHARP_OFFSET,
)
from .anchor import Anchor
from .enums import ClickType, PointType
from .formula import Formula
from .position import Position


class BezierCurve:
    def __init__(self, name: str) -> None:
        self.anchors: List[Anchor] = []
        self.dragging: Tuple[Anchor, PointType] | None = None
        self.name = name

    def interact(
        self, mouse: Position, click_type: ClickType, zoom: float | int = 1
    ) -> None:
        for anchor in self.anchors:
            if (
                anchor.point
                and math.dist(mouse.tup, anchor.point.tup)
                <= (POINT_RADIUS + DRAG_TOLERANCE) / zoom
            ):
                point_type = PointType.POINT
                break
            elif (
                anchor.reverse_handle
                and math.dist(mouse.tup, anchor.reverse_handle.tup)
                <= (HANDLE_RADIUS + DRAG_TOLERANCE) / zoom
            ):
                point_type = PointType.REVERSE_HANDLE
                break
            elif (
                anchor.handle
                and math.dist(mouse.tup, anchor.handle.tup)
                <= (HANDLE_RADIUS + DRAG_TOLERANCE) / zoom
            ):
                point_type = PointType.HANDLE
                break
        else:
            if click_type == ClickType.MOUSE:
                self.add_anchor(mouse)
            return

        if click_type == ClickType.MOUSE:
            if anchor.handle is None or anchor.reverse_handle is None:
                anchor.reverse_handle = anchor.point.copy()
                anchor.handle = anchor.point.copy()
            else:
                self.dragging = anchor, point_type
        if click_type == ClickType.REMOVE:
            self.anchors.remove(anchor)
        elif click_type == ClickType.GHOST:
            anchor.ghost = not anchor.ghost
        elif (
            click_type == ClickType.SHARP
            and anchor.reverse_handle is not None
            and anchor.handle is not None
        ):
            if math.dist(anchor.point.tup, anchor.handle.tup) > 1:
                anchor.handle.convert(anchor.point)
            else:
                anchor.handle.x = anchor.point.x + UNSHARP_OFFSET[0]
                anchor.handle.y = anchor.point.y + UNSHARP_OFFSET[1]
            anchor.reverse_handle.convert(anchor.point.flip(anchor.handle))
        elif click_type == ClickType.ADD:
            anchor_index = self.anchors.index(anchor)
            if anchor_index == len(self.anchors) - 1:
                return
            next_anchor = self.anchors[anchor_index + 1]
            if next_anchor.point is None:
                return

            new_anchor = Anchor(
                Position.lerp(
                    anchor.point, next_anchor.point, 0.5 - NEW_HANDLE_RADIUS
                ),
                Position.lerp(anchor.point, next_anchor.point, 0.5),
                Position.lerp(
                    anchor.point, next_anchor.point, 0.5 + NEW_HANDLE_RADIUS
                ),
            )
            self.anchors.insert(anchor_index + 1, new_anchor)

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
        last_point: Position | None = None,
        center: Position | None = None,
        zoom: float | int = 1,
    ) -> Generator[List[Tuple[Tuple[float, float], bool, bool]], Any, None]:
        if len(self.anchors) < 2 or not self.anchors[1].point:
            return

        if center is None:
            center = Position(0, 0)

        last: Anchor = self.anchors[0]
        for anchor in self.anchors[1:]:
            incomplete = None in (
                anchor.reverse_handle,
                anchor.point,
                anchor.handle,
            )
            if incomplete and last_point is None:
                return

            quadruplet = [
                (position.x, position.y)
                for position in (
                    last.point.centered(center, zoom),
                    last.handle.centered(center, zoom),
                    anchor.point.flip(last_point).centered(center, zoom)
                    if incomplete
                    else anchor.reverse_handle.centered(center, zoom),
                    anchor.point.centered(center, zoom),
                )
            ]
            yield quadruplet, anchor.ghost, incomplete
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
            + GHOST_EQUATION
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

        quadruplets = list(self.quadruplets())
        x_values, y_values = zip(
            *(
                position
                for quadruplet, _, _ in quadruplets
                for position in quadruplet[:-1]
            )
        )
        ghosts = [
            str(index)
            for index, (_, ghost, _) in enumerate(quadruplets, 1)
            if ghost
        ]

        formula += (
            BEZIER_PARAMETRIC[0]
            + str(len(self.anchors) - 1)
            + BEZIER_PARAMETRIC[1]
            + ', '.join(ghosts)
            + BEZIER_PARAMETRIC[2]
            + str(len(self.anchors) - 1)
            + BEZIER_PARAMETRIC[3]
            + ', '.join(
                str(
                    round(
                        (value - SIZE[0] / 2) / SIZE[1] * height,
                        round_places,
                    )
                )
                for value in x_values + (self.anchors[-1].point.x,)
            )
            + BEZIER_PARAMETRIC[4]
            + str(len(self.anchors) - 1)
            + BEZIER_PARAMETRIC[5]
            + ', '.join(
                str(round((0.5 - value / SIZE[1]) * height, round_places))
                for value in y_values + (self.anchors[-1].point.y,)
            )
            + BEZIER_PARAMETRIC[6]
        )
        return Formula(formula)

    def save_progress(self) -> None:
        file_path = self.name + '.json'
        if not os.path.exists(file_path):
            with open(file_path, 'w') as file:
                json.dump([], file)

        with open(file_path, 'r') as file:
            saves: List[List[Dict[str, float]]] = json.load(file)

        save = [dataclasses.asdict(anchor) for anchor in self.anchors]

        if (
            saves
            and len(save) == len(saves[-1])
            and all(
                anchor_dict == last_save_dict
                for anchor_dict, last_save_dict in zip(
                    save, saves[-1], strict=True
                )
            )
        ):
            print('Nothing new to save')
            return

        saves.append(save)
        saves = saves[-MAX_SAVES:]

        with open(file_path, 'w') as file:
            json.dump(saves, file, indent=4)
        print('Saved progress')

    def load_drawing(self, lookbehind: int) -> bool:
        file_path = self.name + '.json'
        if not os.path.exists(file_path):
            return

        print(
            'Previous drawing: ',
            [dataclasses.asdict(anchor) for anchor in self.anchors],
        )
        with open(file_path, 'r') as file:
            saves = json.load(file)
        if lookbehind > len(saves) or lookbehind < 1:
            print(f'Could not look behind {lookbehind} saves')
            return True
        last_save = saves[-lookbehind]
        self.anchors = [
            dacite.from_dict(Anchor, anchor) for anchor in last_save
        ]
        print('Loaded drawing')
        return False
