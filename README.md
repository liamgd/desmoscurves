# desmoscurves

A bezier curve editor implemented in Python with an option to save as a Desmos graph.

Access Desmos here: https://www.desmos.com/calculator.

A bezier curve from [Wikipedia](https://en.wikipedia.org/wiki/File:B%C3%A9zier_3_big.gif):

<img src="https://www.google.com/url?sa=i&url=https%3A%2F%2Fen.wikipedia.org%2Fwiki%2FFile%3AB%25C3%25A9zier_3_big.gif&psig=AOvVaw1Bw52iKp-Q7ltx5aBNLyhp&ust=1702617083496000&source=images&cd=vfe&opi=89978449&ved=0CA8QjRxqFwoTCLDJ0IaVjoMDFQAAAAAdAAAAABAI" alt="Bezier curve example">

## Installation and Usage

Install:

1. Install Git and Python 3.10 or higher.
2. Open the terminal or command prompt.
3. Run `python3 -m pip install git+https://github.com/liamgd/desmoscurves` or `python -m pip install git+https://github.com/liamgd/desmoscurves` depending on installation.

Create:

4. Make a directory anywhere on your device for this program's saves and change directory to it.
5. Run `desmoscurves`.
6. Enter a project name (with no .json suffix).
7. Create your curve.

Save:

8. Press enter to save and enter configuration options if desired (blank to use default values).
9. Paste the equations from your clipboard into desmos.com.

## Creating Your Curves

After entering a project name, the editor opens in a new window. The canvas can be scrolled and zoomed. Most interactions are doing using a combination of cursor placement and a key or mouse press.

### Controls

Basic editing:

- Left click in blank space creates a new node (oscillates between anchor point and handle)
- Left click twice in the same spot in blank space creates a new sharp point anchor
- Left click and drag on nodes moves them
- Holding backspace deletes anchors under cursor

Scrolling:

- Right click and drag anywhere scrolls the canvas
- Scroll up zooms in to the mouse position
- Scroll down zooms out of the mouse position
- Pressing "R" resets the scroll and zoom of the canvas

Saving and loading:

- Enter saves curves as a Desmos graph after responding in the terminal
- Closing the window saves the current curve and quits
- Pressing "S" saves the current curve
- Pressing "L" loads the last saved curve after saving the current curve and continues loading previous curves if pressed repeatedly
- Pressing "C" saves the current curve and clears the entire screen

Other tools:

- Space toggles whether to show nodes and accessary lines (useful for getting a sense of the shape of the curve without the noise of the control points)
- Pressing "G" while hovering over a node toggles ghost on the curve segment behind that anchor (useful for making separations between curves)
- Pressing "P" while hovering over a node toggles sharp point mode
- Pressing "A" while hovering over a node adds a new anchor in between that and the subsequent node (useful for adding more detail or shape to previous segments)

### Ghost segments

Curve segments can be normal or ghost. Ghost segments are hidden from the Desmos graph and are rendered dark-blue in this editor. Ghost segments are how you separate multiple curves. Press "G" on a node to make the previous segment ghost.

### Sharp point anchors

Sharp point anchors have handles at the same location as the anchor point. They function as if they have no additional influence on the curve's direction. Use multiple adjacent sharp point anchors to create straight lines. Create a new sharp point anchor by left clicking twice in the same spot. Toggle an existing anchor between sharp and not normal by pressing "P" while hovering over it with your mouse.

### Exporting as a Desmos graph

After creating your curves, press enter to export as a Desmos graph. Go to the terminal where the program is being run. It will ask some questions. In most cases, you can leave the questions blank and press enter repeatedly to use the default values. If you would like to add new curves to a Desmos graph that already has the helper functions, enter "N" to the first question.

The resulting function(s) are in LaTeX form and will be saved to your clipboard. Paste them into a Desmos graph at https://www.desmos.com/calculator. Sign up or log in to save the graph on Desmos.

## Requirements

See the requirements.txt file.

Requirements file generated with `pipreqs --mode compat --force`, with `pywin32` removed.
