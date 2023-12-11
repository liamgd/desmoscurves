# gui.py
BUTTONS = {'save': 'Return', 'clear': 'BackSpace'}

# classes.py
STEP_EQUATION = 's\\left(x,x_{1},x_{2}\\right) =\\frac{\\operatorname{sign}\\left(\\frac{x-x_{1}}{x_{2}-x_{1}}\\right)-\\operatorname{sign}\\left(\\frac{x-x_{1}}{x_{2}-x_{1}}-1\\right)}{2}'
LINE_EQUATION = 'l\\left(x,x_{1},y_{1},x_{2},y_{2}\\right)=\\left(\\frac{y_{2}-y_{1}}{x_{2}-x_{1}}\\left(x-x_{1}\\right)+y_{1}\\right)s\\left(x,x_{1},x_{2}\\right)'
LINE = 'l({parameter}, {x1}, {y1}, {x2}, {y2})'
LINE_PARAMETRIC = '({x_scale}mod({parameter}, {period}), {y_scale}({lines}))'
BEZIER_EQUATION = 'b\\left(x,p_{1},p_{2},p_{3},p_{4}\\right)=s\\left(x,0,1\\right)\\left(\\left(1-x\\right)^{3}p_{1}+3x\\left(1-x\\right)^{2}p_{2}+3x^{2}\\left(1-x\\right)p_{3}+x^{3}p_{4}\\right)'
BEZIER_SUM_EQUATION = 'b_{s}\\left(x,p\\right)=\\sum_{n=0}^{\\frac{\\operatorname{count}\\left(p\\right)-4}{3}}b\\left(x-n,p\\left[3n+1\\right],p\\left[3n+2\\right],p\\left[3n+3\\right],p\\left[3n+4\\right]\\right)'
BEZIER_PARAMETRIC = (
    '\\left(b_{s}\\left(',
    't,[',
    ']\\right),b_{s}\\left(',
    't,[',
    ']\\right)\\right)',
)

# pygame_gui.py
SIZE = (1920, 1080)
LIGHT = (255, 255, 255)
GREY = (160, 160, 160)
DARK = (30, 30, 30)
HANDLE_RADIUS = 8
POINT_RADIUS = 12
DRAG_TOLERANCE = 3
BEZIER_STEPS = 10
