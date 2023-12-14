# gui.py
BUTTONS = {'save': 'Return', 'clear': 'BackSpace'}

# classes.py
STEP_EQUATION = 's\\left(x,x_{1},x_{2}\\right) =\\frac{\\operatorname{sign}\\left(\\frac{x-x_{1}}{x_{2}-x_{1}}\\right)-\\operatorname{sign}\\left(\\frac{x-x_{1}}{x_{2}-x_{1}}-1\\right)}{2}'
LINE_EQUATION = 'l\\left(x,x_{1},y_{1},x_{2},y_{2}\\right)=\\left(\\frac{y_{2}-y_{1}}{x_{2}-x_{1}}\\left(x-x_{1}\\right)+y_{1}\\right)s\\left(x,x_{1},x_{2}\\right)'
LINE = 'l({parameter}, {x1}, {y1}, {x2}, {y2})'
LINE_PARAMETRIC = '({x_scale}mod({parameter}, {period}), {y_scale}({lines}))'
BEZIER_EQUATION = 'b\\left(x,p_{1},p_{2},p_{3},p_{4}\\right)=s\\left(x,0,1\\right)\\left(\\left(1-x\\right)^{3}p_{1}+3x\\left(1-x\\right)^{2}p_{2}+3x^{2}\\left(1-x\\right)p_{3}+x^{3}p_{4}\\right)'
BEZIER_SUM_EQUATION = 'b_{s}\\left(x,p\\right)=\\sum_{n=0}^{\\frac{\\operatorname{count}\\left(p\\right)-4}{3}}b\\left(x-n,p\\left[3n+1\\right],p\\left[3n+2\\right],p\\left[3n+3\\right],p\\left[3n+4\\right]\\right)'
GHOST_EQUATION = 'g\left(x,p\\right)=\\frac{1}{1-\\sum_{n=1}^{\\operatorname{count}\\left(p\\right)}s\\left(x,p\\left[n\\right]-1,p\\left[n\\right]\\right)}'
BEZIER_PARAMETRIC = (
    '\\left(g\\left(',
    't,\\left[',
    '\\right]\\right)b_{s}\\left(',
    't,[',
    ']\\right),b_{s}\\left(',
    't,[',
    ']\\right)\\right)',
)

# pygame_gui.py
SIZE = (1920, 1080)
CURVE_COLOR = (255, 255, 255)
HANDLE_COLOR = (160, 120, 120)
TENTATIVE_COLOR = (120, 120, 120)
GHOST = (50, 50, 100)
AXES_COLOR = (80, 80, 80)
DARK = (30, 30, 30)
AXES_WIDTH = 2
HANDLE_RADIUS = 8
POINT_RADIUS = 12
DRAG_TOLERANCE = 3
BEZIER_STEPS = 10
UNSHARP_OFFSET = (30, 0)
NEW_HANDLE_RADIUS = 0.1
ZOOM_MULTIPLIER = 1.3
MAX_SAVES = 100
