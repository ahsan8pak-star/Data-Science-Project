String[] frames = {
    """
    ________
    |   __   |
    |  |  |  |
    |  |  |  |
    |  |__|  |
    |        |
    |________|
    """,
    """
     ________
    |   __   |
    |  |  |  |
    |  |  |  |
    |  |  |  |
    |   \\ |  |
    |____\\___|
    """,
    """
     ________
    |   __   |
    |   | |  |
    |   | |  |
    |   | |  |
    |    \\|  |
    |_____\\__|
    """,
    """
     ________
    |        |
    |     || |
    |     || |
    |     || |
    |     || |
    |______\\ |
    """,
    """
     ________
    |        |
    |        |
    |        |
    |        |
    |        |
    |_______ |
    """,
};

for (String frame : frames) {
    System.out.print("\033[H\033[2J");
    System.out.flush();
    System.out.println(frame);
    Thread.sleep(500);  // Wait for 500 milliseconds before showing the next frame
}
