import pygame
import pygame.gfxdraw
from classes import BezierCurve, ClickType, Position
from constant import (
    BEZIER_STEPS,
    DARK,
    GREY,
    HANDLE_RADIUS,
    LIGHT,
    POINT_RADIUS,
    SIZE,
)


def gui() -> None:
    pygame.init()
    display = pygame.display.set_mode(SIZE)
    clock = pygame.time.Clock()

    curve = BezierCurve()
    show_anchors = True

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if curve.dragging is not None:
                    continue
                curve.click(
                    Position(*event.pos),
                    ClickType.MOUSE,
                )
            elif event.type == pygame.MOUSEMOTION:
                curve.motion(Position(*event.pos))
            elif event.type == pygame.MOUSEBUTTONUP:
                curve.dragging = None
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    show_anchors = not show_anchors
                elif event.key == pygame.K_RETURN:
                    formula = curve.curve_to_formula()
                    if formula is not None:
                        formula.save()
                elif event.key == pygame.K_c:
                    curve.dragging = None
                    curve.anchors.clear()

            keys = pygame.key.get_pressed()
            if keys[pygame.K_BACKSPACE]:
                curve.click(
                    Position(*pygame.mouse.get_pos()),
                    ClickType.REMOVE,
                )

        display.fill(DARK)

        if show_anchors:
            for anchor in curve.anchors:
                if anchor.reverse_handle:
                    pygame.draw.circle(
                        display, GREY, anchor.reverse_handle.tup, HANDLE_RADIUS
                    )
                if anchor.point:
                    pygame.draw.circle(
                        display, LIGHT, anchor.point.tup, POINT_RADIUS
                    )
                if anchor.handle:
                    pygame.draw.circle(
                        display, GREY, anchor.handle.tup, HANDLE_RADIUS
                    )
                if anchor.reverse_handle and anchor.handle:
                    pygame.draw.line(
                        display,
                        GREY,
                        anchor.reverse_handle.tup,
                        anchor.handle.tup,
                    )

        for quadruplet in curve.quadruplets():
            pygame.gfxdraw.bezier(display, quadruplet, BEZIER_STEPS, LIGHT)

        clock.tick(30)
        pygame.display.update()


if __name__ == '__main__':
    gui()
