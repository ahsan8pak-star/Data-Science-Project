"""
Line-by-line Python translation of ``week8/lecture/java/DoodleHouse.java``.

The Java program draws a greetings-card house: sky, grass, walls, door,
windows, roof, sun and a greeting. The translation keeps the same helper
functions (``draw_window`` and ``draw_sun``) and the same drawing order.

Java Swing to Python tkinter mapping used here:

  ``g.fillRect(x, y, w, h)``          -> ``create_rectangle(x, y, x+w, y+h)``
  ``g.drawLine(x1, y1, x2, y2)``      -> ``create_line(x1, y1, x2, y2)``
  ``g.fillPolygon(xs, ys, n)``        -> ``create_polygon(xs, ys)``
  ``g.drawString(text, x, y)``        -> ``create_text(..., anchor="nw")``
  ``g.translate(dx, dy)``             -> coordinates offset by dx and dy
  ``g.setFont(font.deriveFont(40f))`` -> ``font=("Arial", 40)``

Two differences are worth knowing. First, Java's ``fillRect``/``drawOval``
take width and height, while tkinter takes the opposite corner, so every
second coordinate is an addition. Second, Java's ``drawString`` places the
text baseline at ``y``, while tkinter's default anchor is the centre of the
text; ``anchor="nw"`` makes the coordinate the top-left corner instead.

The Java ``g.translate`` calls move the drawing origin and then move it
back. tkinter's Canvas has no persistent origin, so the same effect is
achieved by adding the offset to each coordinate, which is what the
``x +`` and ``y +`` terms below do.
"""

import math
import tkinter as tk

WINDOW_WIDTH = 640
WINDOW_HEIGHT = 480


def draw_window(canvas: tk.Canvas, x: int, y: int) -> None:
    """
    Mirror of ``DoodlePanel.drawWindow``.

    Java translates the origin to (x, y), draws a 50x50 blue square with a
    black cross, then translates back. Here the offset is applied to every
    coordinate, which produces the same picture without mutable state.
    """
    # g.translate(x, y); g.setColor(Color.BLUE); g.fillRect(0, 0, 50, 50)
    canvas.create_rectangle(x, y, x + 50, y + 50, fill="blue", outline="blue")

    # g.setColor(Color.BLACK); g.drawLine(25, 0, 25, 50)
    # A vertical line down the middle of the square.
    canvas.create_line(x + 25, y, x + 25, y + 50, fill="black")

    # g.drawLine(0, 25, 50, 25): the horizontal line.
    canvas.create_line(x, y + 25, x + 50, y + 25, fill="black")


def draw_sun(canvas: tk.Canvas, x: int, y: int, rays: int) -> None:
    """
    Mirror of ``DoodlePanel.drawSun``.

    The sun is a filled circle with ``rays`` lines radiating from its
    centre. Java computes each ray with ``Math.cos``/``Math.sin`` in radians
    after converting degrees; Python's ``math`` module uses the same radian
    convention, so only the function names change.
    """
    # g.translate(x, y); g.setColor(YELLOW); g.fillOval(-50, -50, 100, 100)
    # Corners are (-50, -50) and (50, 50) relative to the translated origin.
    canvas.create_oval(x - 50, y - 50, x + 50, y + 50, fill="yellow", outline="yellow")

    # Java: angle = (360.0 / rays) * n; radians = angle * PI * 2 / 360.
    # math.cos and math.sin take radians, so the arithmetic is unchanged.
    radius = 100.0
    radians_per_degree = math.pi * 2.0 / 360.0
    for n in range(rays):
        angle = (360.0 / rays) * n
        # g.drawLine(0, 0, length*cos(...), length*sin(...))
        # int() truncates toward zero exactly as Java's (int) cast does.
        end_x = x + int(radius * math.cos(angle * radians_per_degree))
        end_y = y + int(radius * math.sin(angle * radians_per_degree))
        canvas.create_line(x, y, end_x, end_y, fill="yellow")

    # g.translate(-x, -y): no code needed, because the offsets are local.


def paint_component(canvas: tk.Canvas) -> None:
    """
    Mirror of ``DoodlePanel.paintComponent``, in the original drawing order.

    The order matters: the sky is painted first and each later shape covers
    part of it. Painting the grass before the house, for example, would hide
    the bottom of the walls.
    """
    canvas.delete("all")  # super.paintComponent(g)

    # g.setColor(Color.CYAN); g.fillRect(0, 0, 640, 480) - the sky.
    canvas.create_rectangle(0, 0, 640, 480, fill="cyan", outline="cyan")

    # g.setColor(Color.GREEN); g.fillRect(0, 400, 640, 80) - the grass.
    canvas.create_rectangle(0, 400, 640, 480, fill="green", outline="green")

    # g.setColor(Color.WHITE); g.fillRect(170, 280, 300, 200) - the walls.
    canvas.create_rectangle(170, 280, 470, 480, fill="white", outline="white")

    # g.setColor(Color.RED); g.fillRect(300, 380, 40, 100) - the door.
    canvas.create_rectangle(300, 380, 340, 480, fill="red", outline="red")

    # drawWindow(g, 220, 380) and drawWindow(g, 370, 380)
    draw_window(canvas, 220, 380)
    draw_window(canvas, 370, 380)

    # g.fillPolygon(new int[]{170,470,420,220}, new int[]{280,280,230,230}, 4)
    # Roof corners: bottom-left, bottom-right, top-right, top-left.
    canvas.create_polygon(
        170, 280, 470, 280, 420, 230, 220, 230,
        fill="darkgray", outline="darkgray",
    )

    # drawSun(g, 530, 140, 10): centre at (530, 140) with ten rays.
    draw_sun(canvas, 530, 140, 10)

    # g.setColor(MAGENTA); g.setFont(...deriveFont(40.0f));
    # g.drawString("Happy Housewarming", 50, 100) - anchor="nw" is top-left.
    canvas.create_text(
        50, 100,
        text="Happy Housewarming",
        fill="magenta",
        font=("Arial", 40),
        anchor="nw",
    )


def create_and_show_gui() -> None:
    """
    Mirror of ``DoodleHouse.createAndShowGUI``.

    The window setup is identical to ``Doodle``: root window, 640x480
    Canvas, then the event loop. It is repeated so this file remains the
    complete translation of its own Java source.
    """
    root = tk.Tk()
    root.title("HelloWorldSwing")
    root.protocol("WM_DELETE_WINDOW", root.destroy)

    canvas = tk.Canvas(
        root,
        width=WINDOW_WIDTH,
        height=WINDOW_HEIGHT,
        background="white",
        highlightthickness=0,
    )
    canvas.pack()

    paint_component(canvas)
    root.mainloop()


def main() -> None:
    """
    Mirror of ``DoodleHouse.main``.

    ``SwingUtilities.invokeLater`` schedules the window creation on Swing's
    event thread. tkinter owns its thread, so ``mainloop`` is the
    equivalent scheduler and no explicit dispatch is needed.
    """
    create_and_show_gui()


if __name__ == "__main__":
    main()

