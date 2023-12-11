import turtle

from classes import Position, Positions
from constant import BUTTONS

positions = Positions()


def click_canvas(x: float, y: float) -> None:
    position = Position(x, y)

    if positions.collides(position):
        return

    if positions.length:
        turtle.pendown()
    else:
        turtle.penup()

    positions.add(position)
    turtle.goto(positions.last.x, positions.last.y)
    position.print()


def clear_drawing() -> None:
    print('Clearing drawing')
    positions.clear()
    turtle.clear()


def save_drawing() -> None:
    print('Saving formula')
    formula = positions.positions_to_formula()
    formula.save()


def gui() -> None:
    window = turtle.Screen()
    window.bgcolor('#1E1E1E')
    window.title('Desmos Drawing')
    turtle.speed(0)
    turtle.shape('circle')
    turtle.color('#FFFFFF')
    turtle.pendown()
    turtle.screensize()

    window.onclick(click_canvas)

    window.onkey(save_drawing, BUTTONS['save'])
    window.onkey(clear_drawing, BUTTONS['clear'])
    window.listen()

    window.mainloop()


if __name__ == '__main__':
    gui()
