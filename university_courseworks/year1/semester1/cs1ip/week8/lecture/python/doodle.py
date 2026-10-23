"""
Line-by-line Python translation of ``week8/lecture/java/Doodle.java``.

The Java program opens a 640x480 window and paints two circles. The
translation uses tkinter, which ships with CPython, rather than a third-party
GUI library.

Java Swing to Python tkinter mapping used here:

  ``class DoodlePanel extends JPanel``      -> a Canvas plus a paint function
  ``paintComponent(Graphics g)``            -> ``paint_component(canvas)``
  ``super.paintComponent(g)``               -> ``canvas.delete("all")``
  ``g.setColor(Color.BLUE)``                -> the ``outline``/``fill`` argument
  ``g.drawOval(x, y, w, h)``                -> ``create_oval(x, y, x+w, y+h)``
  ``g.fillOval(x, y, w, h)``                -> ``create_oval(..., fill=...)``
  ``JFrame`` / ``pack()`` / ``setVisible``  -> ``tk.Tk`` / ``pack()`` / ``mainloop``
  ``SwingUtilities.invokeLater(...)``        -> ``mainloop`` (single-threaded)

The coordinate systems differ in one important way. Java's ``drawOval``
takes a top-left corner plus width and height; tkinter's ``create_oval``
takes two opposite corners. The second corner is therefore ``x + width``
and ``y + height``. Writing ``create_oval(50, 50, 100, 100)`` would draw a
50x50 circle rather than the 100x100 circle the Java line describes.
"""

import tkinter as tk

WINDOW_WIDTH = 640
WINDOW_HEIGHT = 480


def paint_component(canvas: tk.Canvas) -> None:
    """
    Mirror of ``DoodlePanel.paintComponent``.

    ``super.paintComponent(g)`` fills the panel with its background and
    removes the previous frame. A tkinter Canvas keeps its items until they
    are deleted, so ``delete("all")`` is the equivalent first step. Without
    it, each repaint would draw a second set of circles on top of the first.
    """
    canvas.delete("all")

    # g.setColor(Color.BLUE); g.drawOval(50, 50, 100, 100)
    # drawOval is an outline in tkinter; width/height become x+w and y+h.
    canvas.create_oval(50, 50, 150, 150, outline="blue", width=2)

    # g.setColor(Color.RED); g.fillOval(200, 50, 150, 150)
    # fillOval is a solid shape; the outline matches so no border shows.
    canvas.create_oval(200, 50, 350, 200, fill="red", outline="red")


def create_and_show_gui() -> None:
    """
    Mirror of ``Doodle.createAndShowGUI``.

    Java builds a JFrame, adds the panel, sets a preferred size, then packs
    and shows the window. tkinter creates a root window, packs a Canvas of
    the same size, and enters ``mainloop`` to process events.
    """
    root = tk.Tk()
    root.title("HelloWorldSwing")

    # JFrame.EXIT_ON_CLOSE: closing the window ends the process.
    root.protocol("WM_DELETE_WINDOW", root.destroy)

    # panel.setPreferredSize(new Dimension(640, 480))
    # highlightthickness=0 removes tkinter's focus border inside the canvas.
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
    Mirror of ``Doodle.main``.

    Java schedules ``createAndShowGUI`` on the event-dispatching thread with
    ``SwingUtilities.invokeLater``. tkinter has one thread and one event
    loop, so calling the function directly and letting ``mainloop`` run is
    the faithful equivalent; spawning a thread here would be wrong.
    """
    create_and_show_gui()


if __name__ == "__main__":
    main()

