"""
Line-by-line Python translation of ``week12/lecture/java/DoodleFallingSnow.java``.

The Java program animates snow falling over a night sky. Every 40 ms it
repaints: a new snowflake is added roughly once every 30 frames, existing
flakes fall, and flakes below the window are removed.

Java Swing to Python tkinter mapping used here:

  ``javax.swing.Timer``            -> ``root.after(milliseconds, callback)``
  ``repaint()``                    -> calling ``paint_component`` again
  ``ArrayList<Integer>``           -> a Python ``list[int]``
  ``Random.nextInt(n)``            -> ``random.Random().randrange(n)``
  ``Graphics2D.translate/rotate``  -> the ``AffineTransform`` helper below
  ``g.setTransform(original)``     -> ``Graphics.set_transform(original)``
  ``g.setStroke(new BasicStroke)`` -> ``Graphics.set_stroke_width``
  ``g.drawString``                 -> ``canvas.create_text``

``java.awt.geom.AffineTransform`` is the one Java type with no direct
tkinter equivalent: a Canvas line is stored in final screen coordinates,
so it cannot be rotated after creation. ``AffineTransform`` below keeps the
same six-number matrix and the same translate/rotate/setTransform
operations, and ``Graphics`` applies the matrix to each endpoint at drawing
time. That keeps the recursive frond code recognisable line for line.

One subtlety is integer division. Java's ``size * 2 / 3`` on an ``int``
truncates, so the Python form is ``size * 2 // 3``. Using ``/`` would pass
floats to a recursive call written for integers and change the geometry.
"""

import math
import random
import tkinter as tk

WINDOW_WIDTH = 640
WINDOW_HEIGHT = 480
FPS = 25
FRAME_MILLISECONDS = 1000 // FPS

# java.awt.Color constants used by the program, as tkinter colour strings.
WHITE = "#ffffff"
LIGHT_GRAY = "#c0c0c0"
DARK_GRAY = "#404040"
CYAN = "#00ffff"
BLUE = "#0000ff"
BLACK = "#000000"
RED = "#ff0000"
GREEN = "#00ff00"


class AffineTransform:
    """
    Minimal stand-in for ``java.awt.geom.AffineTransform``.

    The matrix is stored as the same six values Java uses:

        | a  c  e |
        | b  d  f |
        | 0  0  1 |

    ``apply`` maps a local point to canvas coordinates. Only translation
    and rotation are needed here, which is why there are no scale or shear
    methods.
    """

    def __init__(self, a: float = 1.0, b: float = 0.0, c: float = 0.0,
                 d: float = 1.0, e: float = 0.0, f: float = 0.0) -> None:
        self.a = a
        self.b = b
        self.c = c
        self.d = d
        self.e = e
        self.f = f

    def copy(self) -> "AffineTransform":
        """
        Return an independent copy, mirroring ``getTransform()``.

        Java returns a copy from ``getTransform`` so that later translations
        do not mutate the saved value. Returning ``self`` here would make
        every ``setTransform(original)`` a no-op.
        """
        return AffineTransform(self.a, self.b, self.c, self.d, self.e, self.f)

    def translate(self, tx: float, ty: float) -> None:
        """
        Post-concatenate a translation, like ``AffineTransform.translate``.

        Composition is ``this = this * T``. For a translation this only
        changes the ``e`` and ``f`` offsets.
        """
        self.e = self.a * tx + self.c * ty + self.e
        self.f = self.b * tx + self.d * ty + self.f

    def rotate(self, radians: float) -> None:
        """
        Post-concatenate a rotation, like ``AffineTransform.rotate``.

        The rotation matrix is ``[[cos, -sin], [sin, cos]]``. Composing it
        with the current matrix updates all four coefficients but leaves the
        translation offsets alone.
        """
        cos = math.cos(radians)
        sin = math.sin(radians)
        a, b, c, d = self.a, self.b, self.c, self.d
        self.a = a * cos + c * sin
        self.b = b * cos + d * sin
        self.c = -a * sin + c * cos
        self.d = -b * sin + d * cos

    def apply(self, x: float, y: float) -> tuple[float, float]:
        """
        Transform one local point into canvas coordinates.

        This is the step Java performs internally inside ``drawLine``; here
        it is explicit because the Canvas needs final coordinates.
        """
        return (self.a * x + self.c * y + self.e,
                self.b * x + self.d * y + self.f)


class Graphics:
    """
    The small part of ``java.awt.Graphics2D`` this program actually uses.

    Holding the colour, stroke width and transform in one object mirrors
    Java's graphics context. If the canvas were passed around directly, the
    recursive frond function would lose the current rotation between calls.
    """

    def __init__(self, canvas: tk.Canvas) -> None:
        self.canvas = canvas
        self.colour = BLACK
        self.stroke_width = 1.0
        self.font_size = 12
        self.transform = AffineTransform()

    def set_colour(self, colour: str) -> None:
        """Mirror of ``g.setColor(...)``."""
        self.colour = colour

    def set_stroke_width(self, width: float) -> None:
        """Mirror of ``g.setStroke(new BasicStroke(width))``."""
        self.stroke_width = width

    def set_font_size(self, size: int) -> None:
        """Mirror of ``g.setFont(font.deriveFont(size))``."""
        self.font_size = size

    def get_transform(self) -> AffineTransform:
        """Mirror of ``g.getTransform()``: a snapshot, not a live handle."""
        return self.transform.copy()

    def set_transform(self, transform: AffineTransform) -> None:
        """Mirror of ``g.setTransform(t)``: restore a saved matrix."""
        self.transform = transform.copy()

    def translate(self, x: float, y: float) -> None:
        """Mirror of ``g.translate(x, y)``."""
        self.transform.translate(x, y)

    def rotate(self, radians: float) -> None:
        """Mirror of ``g.rotate(radians)``."""
        self.transform.rotate(radians)

    def draw_line(self, x1: float, y1: float, x2: float, y2: float) -> None:
        """
        Mirror of ``g.drawLine(x1, y1, x2, y2)``.

        Both endpoints are transformed before the line is created, so the
        canvas stores the rotated line even though it cannot rotate items.
        """
        start_x, start_y = self.transform.apply(x1, y1)
        end_x, end_y = self.transform.apply(x2, y2)
        self.canvas.create_line(
            start_x, start_y, end_x, end_y,
            fill=self.colour, width=self.stroke_width,
        )

    def fill_oval(self, x: float, y: float, width: float, height: float) -> None:
        """Mirror of ``g.fillOval(x, y, width, height)``."""
        start_x, start_y = self.transform.apply(x, y)
        end_x, end_y = self.transform.apply(x + width, y + height)
        self.canvas.create_oval(
            start_x, start_y, end_x, end_y,
            fill=self.colour, outline=self.colour,
        )

    def fill_rect(self, x: float, y: float, width: float, height: float) -> None:
        """Mirror of ``g.fillRect(x, y, width, height)``."""
        start_x, start_y = self.transform.apply(x, y)
        end_x, end_y = self.transform.apply(x + width, y + height)
        self.canvas.create_rectangle(
            start_x, start_y, end_x, end_y,
            fill=self.colour, outline=self.colour,
        )

    def draw_string(self, text: str, x: float, y: float) -> None:
        """Mirror of ``g.drawString(text, x, y)`` with a top-left anchor."""
        draw_x, draw_y = self.transform.apply(x, y)
        self.canvas.create_text(
            draw_x, draw_y,
            text=text, fill=self.colour,
            font=("Arial", self.font_size), anchor="nw",
        )


class DoodlePanel:
    """
    Mirror of the Java ``DoodlePanel`` class.

    The Java class extends ``JPanel`` and draws from ``paintComponent``.
    This version owns a Canvas and a ``Graphics`` context, and drives
    repaints with tkinter's ``after`` instead of ``javax.swing.Timer``.
    """

    def __init__(self, root: tk.Tk, canvas: tk.Canvas) -> None:
        """Mirror of ``DoodlePanel()``: set up state and start the timer."""
        self.root = root
        self.canvas = canvas
        self.graphics = Graphics(canvas)

        # int frame; Random r = new Random();
        self.frame = 100
        self.rng = random.Random()

        # ArrayList<Integer> fields -> list[int] fields. Six parallel lists
        # represent one snowflake each, exactly as in the Java version.
        self.snow_x: list[int] = []
        self.snow_y: list[int] = []
        self.snow_velocity: list[int] = []
        self.snow_size: list[int] = []
        self.snow_spin: list[int] = []
        self.snow_colour: list[int] = []

        # Timer t = new Timer(1000/fps, e -> repaint()); t.start();
        # after() schedules one call; _tick schedules the next.
        self.paint_component()
        self.root.after(FRAME_MILLISECONDS, self._tick)

    def _tick(self) -> None:
        """Repaint and schedule the next frame, mirroring the Timer action."""
        self.paint_component()
        self.root.after(FRAME_MILLISECONDS, self._tick)

    def paint_component(self) -> None:
        """
        Mirror of ``DoodlePanel.paintComponent``.

        The method adds a flake, draws the sky, updates and draws every
        existing flake, then draws the greeting and the two counters.
        """
        graphics = self.graphics
        self.canvas.delete("all")  # super.paintComponent(g)
        self.frame += 1

        # Color col[] = {WHITE, LIGHT_GRAY, DARK_GRAY, CYAN, BLUE};
        colours = [WHITE, LIGHT_GRAY, DARK_GRAY, CYAN, BLUE]

        # if (r.nextInt(30) == 0) { ... } adds one new snowflake.
        if self.rng.randrange(30) == 0:
            self.snow_x.append(self.rng.randrange(540) + 50)
            self.snow_y.append(-150)
            self.snow_size.append(self.rng.randrange(100) + 50)
            self.snow_spin.append(self.rng.randrange(360))
            self.snow_velocity.append(self.rng.randrange(4) + 1)
            self.snow_colour.append(self.rng.randrange(len(colours)))

        # g.setColor(Color.BLACK); g.fillRect(0, 0, 640, 480)
        graphics.set_colour(BLACK)
        graphics.fill_rect(0, 0, 640, 480)

        # for (int n = 0; n < snow_x.size(); n++) { ... }
        # A while loop is needed because the body deletes the current item.
        n = 0
        while n < len(self.snow_x):
            graphics.set_colour(colours[self.snow_colour[n]])
            graphics.set_stroke_width(1.0)
            self.draw_complex_snowflake(
                graphics,
                colours[self.snow_colour[n]],
                self.snow_x[n],
                self.snow_y[n],
                self.snow_size[n],
                self.snow_spin[n],
            )

            # snow_y.set(n, snow_y.get(n) + snow_vel.get(n))
            self.snow_y[n] = self.snow_y[n] + self.snow_velocity[n]

            # if (snow_y.get(n) > 600) { remove every list at n; n--; }
            if self.snow_y[n] > 600:
                del self.snow_x[n]
                del self.snow_y[n]
                del self.snow_colour[n]
                del self.snow_size[n]
                del self.snow_spin[n]
                del self.snow_velocity[n]
                n -= 1
            n += 1

        # g.setColor(Color.RED); g.setFont(...deriveFont(40.0f));
        # g.drawString("Merry Christmas", 200, 50)
        graphics.set_colour(RED)
        graphics.set_font_size(40)
        graphics.draw_string("Merry Christmas", 200, 50)

        # g.setColor(Color.GREEN); g.drawString("Frame " + frame, 0, 450)
        graphics.set_colour(GREEN)
        graphics.set_font_size(12)
        graphics.draw_string(f"Frame {self.frame}", 0, 450)
        graphics.draw_string(f"Snowflakes {len(self.snow_x)}", 0, 470)

    def draw_simple_snowflake(self, graphics: Graphics, colour: str,
                              x: int, y: int, size: int, spin: int) -> None:
        """
        Mirror of ``DoodlePanel.drawSimpleSnowflake``.

        Six rays are drawn from the origin, then the origin is restored.
        The method is not called by ``paint_component`` in the Java source
        (both calls are commented out), but it is translated so the file is
        complete and the simpler shape can be compared with the complex one.
        """
        graphics.set_colour(colour)
        graphics.translate(x, y)

        radians_per_degree = math.pi * 2.0 / 360.0
        for n in range(6):
            # double angle = spin + ((360.0 / 6) * n);
            angle = spin + ((360.0 / 6) * n)
            # int casts truncate, matching Java's (int) cast.
            end_x = int(size * math.cos(angle * radians_per_degree))
            end_y = int(size * math.sin(angle * radians_per_degree))
            graphics.draw_line(0, 0, end_x, end_y)

        # g.translate(-x, -y) restores the origin.
        graphics.translate(-x, -y)

    def draw_complex_snowflake(self, graphics: Graphics, colour: str,
                               x: int, y: int, size: int, spin: int) -> None:
        """
        Mirror of ``DoodlePanel.drawComplexSnowflake``.

        The transform is saved, the origin is moved to the flake centre and
        rotated, six copies of the recursive frond are drawn 60 degrees
        apart, and the saved transform is restored.
        """
        graphics.set_colour(colour)
        graphics.set_stroke_width(4.0)

        original = graphics.get_transform()
        graphics.translate(x, y)
        graphics.rotate(math.pi * 2.0 * spin / 360.0)

        for _ in range(6):
            self.draw_complex_frond(graphics, size, 3)
            graphics.rotate(math.pi * 2.0 / 6.0)

        graphics.set_transform(original)

    def draw_complex_frond(self, graphics: Graphics, size: int,
                           complexity: int) -> None:
        """
        Mirror of ``DoodlePanel.drawComplexFrond``, including its recursion.

        Each level draws the main stem and four side branches. The branch
        positions use Java integer division, hence ``//``. Every branch
        restores the transform it started with, so sibling branches do not
        inherit one another's rotation.
        """
        if complexity == 0:
            return

        original = graphics.get_transform()
        graphics.draw_line(0, 0, 0, size)

        # g.translate(0, size*2/3); g.rotate(+60 degrees); recurse with size/3
        graphics.translate(0, size * 2 // 3)
        graphics.rotate(math.pi * 2.0 / 6.0)
        self.draw_complex_frond(graphics, size // 3, complexity - 1)
        graphics.set_transform(original)

        # The mirror branch: same position, opposite rotation.
        graphics.translate(0, size * 2 // 3)
        graphics.rotate(-math.pi * 2.0 / 6.0)
        self.draw_complex_frond(graphics, size // 3, complexity - 1)
        graphics.set_transform(original)

        # g.translate(0, size*1/3); g.rotate(+60 degrees); recurse with size/4
        graphics.translate(0, size // 3)
        graphics.rotate(math.pi * 2.0 / 6.0)
        self.draw_complex_frond(graphics, size // 4, complexity - 1)
        graphics.set_transform(original)

        # The mirror of the shorter branch.
        graphics.translate(0, size // 3)
        graphics.rotate(-math.pi * 2.0 / 6.0)
        self.draw_complex_frond(graphics, size // 4, complexity - 1)
        graphics.set_transform(original)


def create_and_show_gui() -> None:
    """
    Mirror of ``DoodleFallingSnow.createAndShowGUI``.

    Java creates a JFrame and adds a DoodlePanel. Here the root window and
    Canvas are created first, then passed to the panel object, because
    tkinter widgets need a parent at construction time.
    """
    root = tk.Tk()
    root.title("HelloWorldSwing")
    root.protocol("WM_DELETE_WINDOW", root.destroy)

    canvas = tk.Canvas(
        root,
        width=WINDOW_WIDTH,
        height=WINDOW_HEIGHT,
        background="black",
        highlightthickness=0,
    )
    canvas.pack()

    DoodlePanel(root, canvas)
    root.mainloop()


def main() -> None:
    """
    Mirror of ``DoodleFallingSnow.main``.

    Swing schedules the window on its event thread; tkinter's ``mainloop``
    is that event thread, so the call is direct.
    """
    create_and_show_gui()


if __name__ == "__main__":
    main()

