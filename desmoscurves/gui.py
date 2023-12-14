import os

import pygame
import pygame.gfxdraw

from .classes.bezier_curve import BezierCurve
from .classes.enums import ClickType
from .classes.position import Position
from .constant import (
    AXES_COLOR,
    AXES_WIDTH,
    BEZIER_STEPS,
    CURVE_COLOR,
    DARK,
    GHOST,
    HANDLE_COLOR,
    HANDLE_RADIUS,
    POINT_RADIUS,
    SIZE,
    TENTATIVE_COLOR,
    ZOOM_MULTIPLIER,
)


def gui() -> None:
    print('\nAvailable saves:')
    for file_name in os.listdir():
        if file_name.endswith('.json') and not os.path.isdir(file_name):
            print('  - ' + file_name.removesuffix('.json'))
    print()

    name = input('Project name (new or existing): ').strip().lower()
    if name == '':
        raise ValueError('Name cannot be empty!')

    pygame.init()
    display = pygame.display.set_mode(SIZE)
    clock = pygame.time.Clock()
    print('Opened pygame')
    print('SEE README FOR INSTRUCTIONS')

    curve = BezierCurve(name)
    curve.load_drawing(1)
    show_anchors = True
    lookbehind = 0
    scrolling = False
    last_mouse = Position(0, 0)
    center = Position(0, 0)
    zoom_times = 1
    zoom = 1

    while True:
        mouse = Position(*pygame.mouse.get_pos())

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                curve.save_progress()
                pygame.quit()
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if curve.dragging is not None:
                        continue
                    curve.interact(
                        mouse.centered(center, zoom, True),
                        ClickType.MOUSE,
                        zoom,
                    )
                    lookbehind = 0
                elif event.button == 3:
                    scrolling = True
                    last_mouse = mouse.copy()
                elif event.button in (4, 5):
                    multiplier = 1 if event.button == 4 else -1
                    x_dist = (mouse.x - SIZE[0] / 2) / zoom
                    y_dist = (mouse.y - SIZE[1] / 2) / zoom
                    center.x += x_dist / ZOOM_MULTIPLIER**multiplier - x_dist
                    center.y += y_dist / ZOOM_MULTIPLIER**multiplier - y_dist
                    zoom_times += multiplier
                    zoom = ZOOM_MULTIPLIER**zoom_times
            elif event.type == pygame.MOUSEMOTION:
                curve.motion(mouse.centered(center, zoom, True))
                if scrolling:
                    center.x += (mouse.x - last_mouse.x) // zoom
                    center.y += (mouse.y - last_mouse.y) // zoom
                    last_mouse = mouse.copy()
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    curve.dragging = None
                    lookbehind = 0
                elif event.button == 3:
                    scrolling = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_l:
                    lookbehind += 1
                    if curve.load_drawing(lookbehind):
                        print('Resetting lookbehind')
                        lookbehind = 0
                    continue
                lookbehind = 0

                if event.key == pygame.K_SPACE:
                    show_anchors = not show_anchors
                elif event.key == pygame.K_RETURN:
                    formula = curve.curve_to_formula()
                    if formula is not None:
                        formula.save()
                elif event.key == pygame.K_c:
                    curve.save_progress()
                    curve.dragging = None
                    curve.anchors.clear()
                    print('Cleared board; load last save to revert chagnes')
                elif event.key == pygame.K_g:
                    curve.interact(
                        mouse.centered(center, zoom, True),
                        ClickType.GHOST,
                        zoom,
                    )
                elif event.key == pygame.K_p:
                    curve.interact(
                        mouse.centered(center, zoom, True),
                        ClickType.SHARP,
                        zoom,
                    )
                elif event.key == pygame.K_s:
                    curve.save_progress()
                elif event.key == pygame.K_a:
                    curve.interact(
                        mouse.centered(center, zoom, True), ClickType.ADD, zoom
                    )
                elif event.key == pygame.K_r:
                    center.x = 0
                    center.y = 0
                    zoom = 1

            keys = pygame.key.get_pressed()
            if keys[pygame.K_BACKSPACE]:
                curve.interact(
                    mouse.centered(center, zoom, True), ClickType.REMOVE, zoom
                )

        display.fill(DARK)

        if show_anchors:
            border = pygame.Rect(
                *Position(0, 0).centered(center, zoom).tup,
                SIZE[0] * zoom,
                SIZE[1] * zoom
            )
            pygame.draw.rect(display, AXES_COLOR, border, AXES_WIDTH)
            pygame.draw.line(
                display,
                AXES_COLOR,
                Position(0, SIZE[1] // 2).centered(center, zoom).tup,
                Position(SIZE[0], SIZE[1] // 2).centered(center, zoom).tup,
                AXES_WIDTH,
            )
            pygame.draw.line(
                display,
                AXES_COLOR,
                Position(SIZE[0] // 2, 0).centered(center, zoom).tup,
                Position(SIZE[0] // 2, SIZE[1]).centered(center, zoom).tup,
                AXES_WIDTH,
            )

            for anchor in curve.anchors:
                if anchor.point is None:
                    continue
                complete = (
                    anchor.reverse_handle is not None
                    and anchor.handle is not None
                )

                reverse_handle = (
                    anchor.reverse_handle.centered(center, zoom).tup
                    if complete
                    else anchor.point.centered(center, zoom).flip(mouse).tup
                )
                handle = (
                    anchor.handle.centered(center, zoom).tup
                    if complete
                    else mouse.tup
                )

                pygame.draw.circle(
                    display,
                    CURVE_COLOR if complete else TENTATIVE_COLOR,
                    anchor.point.centered(center, zoom).tup,
                    POINT_RADIUS,
                )
                pygame.draw.circle(
                    display,
                    HANDLE_COLOR if complete else TENTATIVE_COLOR,
                    reverse_handle,
                    HANDLE_RADIUS,
                )
                pygame.draw.circle(
                    display,
                    HANDLE_COLOR if complete else TENTATIVE_COLOR,
                    handle,
                    HANDLE_RADIUS,
                )
                pygame.draw.line(
                    display,
                    HANDLE_COLOR if complete else TENTATIVE_COLOR,
                    reverse_handle,
                    handle,
                )

        for quadruplet, ghost, incomplete in curve.quadruplets(
            mouse.centered(center, zoom, True), center, zoom
        ):
            pygame.gfxdraw.bezier(
                display,
                quadruplet,
                BEZIER_STEPS,
                TENTATIVE_COLOR
                if incomplete
                else GHOST
                if ghost
                else CURVE_COLOR,
            )

        clock.tick(30)
        pygame.display.update()


if __name__ == '__main__':
    gui()
