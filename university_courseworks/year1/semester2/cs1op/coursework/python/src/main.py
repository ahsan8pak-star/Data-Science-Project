"""
Space Mission entry point.

Translation of ``Main.java``: install a global crash handler that
reports the error instead of dying silently, then launch the GUI game.
Run the text adventure instead with ``python main.py --text``.
"""

import sys
import traceback


def install_crash_handler():
    """
    Report any uncaught error to standard error before exiting.
    """

    def handle(exc_type, exc_value, exc_trace):
        import text_ui
        text_ui.eprint("Error: " + str(exc_value))
        traceback.print_exception(exc_type, exc_value, exc_trace)
        sys.exit(1)

    sys.excepthook = handle


def main(argv=None):
    """
    Launch the GUI game, or the text adventure with ``--text``.
    """
    install_crash_handler()
    args = list(sys.argv[1:] if argv is None else argv)
    if "--text" in args:
        from game import Game
        Game.get_instance().start()
        return
    from game_gui import GameGUI
    GameGUI().run()


if __name__ == "__main__":
    main()

