### DEPRECATED

# import turtle

# from constant import BUTTONS
# from position import Position
# import dataclasses

# positions = Positions()


# @dataclasses.dataclass
# class Bounds:
#     top: float
#     bottom: float
#     right: float
#     left: float


# @dataclasses.dataclass
# class Positions:
#     positions: List[Position] = dataclasses.field(default_factory=list)

#     @property
#     def length(self) -> int:
#         return len(self.positions)

#     @property
#     def last(self) -> Position:
#         return self.positions[-1]

#     @property
#     def bounds(self) -> Bounds:
#         x_values, y_values = zip(
#             *(position.tup for position in self.positions)
#         )
#         bounds = Bounds(
#             max(y_values), min(y_values), max(x_values), min(x_values)
#         )
#         return bounds

#     def add(self, position: Position) -> Position:
#         self.positions.append(position)

#     def clear(self) -> None:
#         self.positions.clear()

#     def collides(self, other: Position) -> bool:
#         return self.positions and self.positions[-1].x == other.x

#     def positions_to_formula(self) -> Formula:
#         height = self.bounds.top - self.bounds.bottom
#         width = self.bounds.left - self.bounds.right

#         y_lines = []

#         for i in range(len(self.positions) - 1):
#             line = LINE.format(
#                 x1=(self.positions[i].x - self.bounds.left) / width + i,
#                 y1=(self.positions[i].y - self.bounds.bottom) / height,
#                 x2=(self.positions[i + 1].x - self.bounds.left) / width + i,
#                 y2=(self.positions[i + 1].y - self.bounds.bottom) / height,
#             )
#             y_lines.append(line)

#         formula = (
#             LINE_EQUATION
#             + '\n'
#             + LINE_PARAMETRIC.format(
#                 lines=' + '.join(y_lines),
#                 x_scale=10,
#                 y_scale=10,
#                 period=1,
#             )
#         )

#         return Formula(formula)


# def click_canvas(x: float, y: float) -> None:
#     position = Position(x, y)

#     if positions.collides(position):
#         return

#     if positions.length:
#         turtle.pendown()
#     else:
#         turtle.penup()

#     positions.add(position)
#     turtle.goto(positions.last.x, positions.last.y)
#     position.print()


# def clear_drawing() -> None:
#     print('Clearing drawing')
#     positions.clear()
#     turtle.clear()


# def save_drawing() -> None:
#     print('Saving formula')
#     formula = positions.positions_to_formula()
#     formula.save()


# def gui() -> None:
#     window = turtle.Screen()
#     window.bgcolor('#1E1E1E')
#     window.title('Desmos Drawing')
#     turtle.speed(0)
#     turtle.shape('circle')
#     turtle.color('#FFFFFF')
#     turtle.pendown()
#     turtle.screensize()

#     window.onclick(click_canvas)

#     window.onkey(save_drawing, BUTTONS['save'])
#     window.onkey(clear_drawing, BUTTONS['clear'])
#     window.listen()

#     window.mainloop()


# if __name__ == '__main__':
#     gui()
