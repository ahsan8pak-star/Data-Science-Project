// DoorSelectionScreen Class - Five Mystery Doors with Box-Drawn ASCII Art Numbered 1 to 5
// Doors Display Only the Door Number Before Selection
// ASCII Art Is Shown on Reveal After a Door Is Opened
// Selected Door Shows a Semi-Transparent Green Glow Highlight Over the Entire Door Box
// Sound: DOOR_NAVIGATE on Left/Right, ENTER to Open a Door

import java.awt.BasicStroke;
import java.awt.Color;
import java.awt.Font;
import java.awt.FontMetrics;
import java.awt.Graphics;
import java.awt.Graphics2D;
import java.awt.event.KeyEvent;
import java.awt.event.KeyListener;
import java.util.ArrayList;
import java.util.List;

public class DoorSelectionScreen extends BaseGameScreen implements KeyListener {

    // Door Factory and Active Doors
    private DoorFactory doorFactory;
    private List<Door> availableDoors;

    // Selection and Reveal State
    private int selectedDoorIndex = 0;
    private boolean doorRevealed = false;
    private String resultMessage = "";
    private boolean minigamePending = false;
    private String pendingMinigameType = "";

    // Shiny Chest ASCII Art for Reward Door
    private static final String[] CHEST_ASCII = {
            "*******************************************************************************",
            "          |                   |                  |                     |",
            " _________|________________.=\"\"_;=.______________|_____________________|_______",
            "|                   |  ,-\"_,=\"\"     `\"=.|                  |",
            "|___________________|__\"=._o`\"-._        `\"=.______________|___________________",
            "          |                `\"=._o`\"=._      _`\"=._                     |",
            " _________|_____________________:=._o \"=._.\"|.-=\"'\"=.__________________|_______",
            "|                   |    __.--\" , ; `\"=._o.\" ,-\"\"\"-._ \".   |",
            "|___________________|_._\"  ,. .` ` `` ,  `\"-._\"-._   \". '__|___________________",
            "          |           |o`\"=._` , \"` `; .\". ,  \"-._\"-._; ;              |",
            " _________|___________| ;`-.o`\"=._; .\" ` '`.\"|` . \"-._ /_______________|_______",
            "|                   | |o;    `\"-.o`\"=._``  '` \" ,__.--o;   |",
            "|___________________|_| ;     (#) `-.o `\"=.`_.--\"_o.-; ;___|___________________",
            "____/______/______/___|o;._    '      `.o|o_.--'    ;o;____/______/______/____",
            "/______/______/______/_\"=._o--._        ; | ;        ; ;/______/______/______/_",
            "____/______/______/______/__\"=._o--._   ;o|o;     _._;o;____/______/______/____",
            "/______/______/______/______/____\"=._o._; | ;_.--\"o.--\"_/______/______/______/_",
            "____/______/______/______/______/_____\"=.o|o_.--\"\"___/______/______/______/____",
            "/______/______/______/______/______/______/______/______/______/______/______/_",
            "*******************************************************************************"
    };

    // Poison Bottle ASCII Art for Penalty Door
    private static final String[] POISON_ASCII = {
            "                                       ______",
            "                                       |____|",
            "                                    __/      \\__",
            "                                   /            \\",
            "---------------------------------- |            | ----------------------------------",
            "|                                  |            |                                  |",
            "|                                  |            |                                  |",
            "|                                  \\____________/                                  |",
            "|                                                                                  |",
            "|                            __----------------------__                            |",
            "|                          ..'                        '..                          |",
            "|                        ./                              \\.                        |",
            "|                       ./                                \\.                       |",
            "|                      ./                                  \\.                      |",
            "|                      /                                    \\                      |",
            "|                     | \\                                  / |                     |",
            "|                     |  \\                                /  |                     |",
            "|                     |   \\                              /   |                     |",
            "|                  #######  ########  ##  #####  ########  ###  ##                 |",
            "|                  ##   ##  ##    ##  ##  ##     ##    ##  ## # ##                 |",
            "|                  #######  ##    ##  ##  #####  ##    ##  ## # ##                 |",
            "|               __ ##       ##    ##  ##     ##  ##    ##  ##  ### __              |",
            "|              (   ##       ########  ##  #####  ########  ##   ##   )             |",
            "|              )    \\_    /      ...    /   \\    ...      \\    _/    (             |",
            "|             (     _ '.  \\            /     \\            /  .' _     )            |",
            "|              '---' '. '. \\          (       )          / .' .' '---'             |",
            "|                      '. '.\\          '-'''-'          /.' .'                     |",
            "|                        '.  \\__                     __/  .'                       |",
            "|                          '. \\|'\\...-_--_-_-_--.../'|/ .'                         |",
            "|                           .' |  ||||_||_|_|_|||||  |  '.                         |",
            "|                         .'  .|  '\\.|||\\_|_/|||./'  |'.  '.                       |",
            "|                       .'  .' |                     |  '.  '.                     |",
            "|                _____.'  .'   '\\.   ..       ..   ./'    '.  '._____              |",
            "|              (       _.'       '-_             _-'        '_        )            |",
            "|               |     /             '._________.'             \\      |             |",
            "|                \\___/                                         \\____/              |",
            "|                                                                                  |",
            "------------------------------------------------------------------------------------"
    };

    // Open Door ASCII Art for Nothing Door
    private static final String[] NOTHING_ASCII = {
            " ___________________________",
            "|\\ ________________________/|",
            "| |        |               ||",
            "| |        |   /' .        ||",
            "| |        |   |    ' .    ||",
            "| |        |   |       \\   ||",
            "| |        |   |       |   ||",
            "| |        |   \\       |   ||",
            "| |        |    ' .    |   ||",
            "| |        |        ' ./   ||",
            "| |        ()              ||",
            "| |        |               ||",
            "| |        |   /' .        ||",
            "| |        |   |    ' .    ||",
            "| |        |   |       \\   ||",
            "| |        |   |       |   ||",
            "| |        |   \\       |   ||",
            "| |        |    ' .    |   ||",
            "| |        |        ' ./   ||",
            "| |        '  .            ||",
            "| |              '  .      ||",
            "|/_____________________'  .\\|"
    };

    // Table Tennis Court ASCII Art for Pong Minigame Door
    private static final String[] PONG_ASCII = {

            "                                        ..-+##+-..                                            ",
            "                                       .++......-#.                                           ",
            "                                      .+-.........+.                                          ",
            "            ...-+#######+-...         .#..........#.           ....-----....                  ",
            "         ..-#################+..       +-........-+.       ..-##++----++++###-..              ",
            "       .-#######################+.     .++--.----+.     ..+#+--+++++++++++++++##-..           ",
            "      .###########################+.     .-+##+-.     ..++-++++++++++++++++++++++#+.          ",
            "    .-##############################+.               .++-++++++-------+++++++++++++#..        ",
            "   .+################################+.            ..#-++++++-------++++++++++++++++#-.       ",
            "   -#+#################################.           .#+++++++-----++++++++++++++++++++#-       ",
            "  .#+####+++###########################+          .#++++++++++++++++++++++++++++++++++#.      ",
            " .-#+###++++############################.        .++++++++++++++++++++++++++++++++++++#-.     ",
            " .+#+###++++#############################.       -#+++++++++++++++++++++++++++++++++++++.     ",
            " .+#+###++++#############################.      .+#++++++++++++++++++++++++++++++++++++#.     ",
            " .+#+###+++++############################.      .#++++++++++++++++++++++++++++++++++++++.     ",
            " .-#+####################################.      .##+++++++++++++++++++++++++++++++++++#+.     ",
            "  .++################################+-++.      .+++##++++++++++++++++++++++++++++++++#.      ",
            "   -##############################+----#.        .+---+##++++++++++++++++++++++++++++#+.      ",
            "   .-##########################+------++          ++...--+##+++++++++++++++++++++++++#.       ",
            "    .-######################---------++.          .#---------##+++++++++++++++++++++#.        ",
            "      .#################+--##++#+---++.            .#+----+###--##++++++++++++++++#+.         ",
            "       .-############+----++----+#--+.              .#---#----++---+##+++++++++++#-.          ",
            "         .-#######+-..-----#-..---##-                -#+#-..--+#------+##++++++#-.            ",
            "           ..-##+---.------+#-..---#+                -#+-..--+#----------+###+..              ",
            "               ..--+#######+##-.----++.             .#+------#--+++++++##+-..                 ",
            "                          ..-#+------++.           .#-------##-.........                      ",
            "                             .++-------#.         -#-------#..                                ",
            "                              .++-------#.      .++-------#..                                 ",
            "                               .+--------#-    .++-------#-                                   ",
            "                                .++----+#-.    -#+------#-.                                   ",
            "                                 .#++#-.        ..-#+--+-.                                    ",
            "                                  ...              ..-#-.                                     "
    };

    // Spacecraft ASCII Art for Space Invaders Minigame Door
    private static final String[] SPACEINVADERS_ASCII = {
            " /\\/\\/\\                            /  \\",
            "| \\  / |                         /      \\",
            "|  \\/  |                       /          \\",
            "|  /\\  |----------------------|     /\\     |",
            "| /  \\ |                      |    /  \\    |",
            "|/    \\|                      |   /    \\   |",
            "|\\    /|                      |  | (  ) |  |",
            "| \\  / |                      |  | (  ) |  |",
            "|  \\/  |                 /\\   |  |      |  |   /\\",
            "|  /\\  |                /  \\  |  |      |  |  /  \\",
            "| /  \\ |               |----| |  |      |  | |----|",
            "|/    \\|---------------|    | | /|  ..  |\\ | |    |",
            "|\\    /|               |    | /  |  ..  |  \\ |    |",
            "| \\  / |               |    /    |  ..  |    \\    |",
            "|  \\/  |               |  /      |  ..  |      \\  |",
            "|  /\\  |---------------|/        |  ..  |        \\|",
            "| /  \\ |              /          |  ..  |          \\",
            "|/    \\|              (          |      |           )",
            "|/\\/\\/\\|               |    | |--|      |--| |    |",
            "------------------------/  \\-----/  \\/  \\-----/  \\--------",
            "                        \\\\//     \\\\//\\\\//     \\\\//",
            "                         \\/       \\/  \\/       \\/"
    };

    // Constructor
    public DoorSelectionScreen(GameGUI gui, GameController controller) {
        super(gui, controller);
        doorFactory = new DoorFactory();
        initializeDoors();
        setFocusable(true);
        addKeyListener(this);
    }

    // Create Five Fresh Doors and Reset the Reveal State
    private void initializeDoors() {
        availableDoors = new ArrayList<>();
        for (int i = 1; i <= 5; i++) {
            availableDoors.add(doorFactory.createRandomDoor(i));
        }
        doorRevealed = false;
        resultMessage = "";
        minigamePending = false;
        pendingMinigameType = "";
    }

    // Render Either the Selection Phase or the Reveal Phase
    @Override
    protected void paintComponent(Graphics g) {
        super.paintComponent(g);
        Graphics2D g2d = (Graphics2D) g;
        enableAntiAliasing(g2d);
        int W = getWidth(), H = getHeight();

        drawBorder(g2d, 20, 20, W - 40, H - 40, 2);
        drawStatus(g2d);

        if (doorRevealed) {
            drawRevealPhase(g2d, W, H);
        } else {
            drawSelectionPhase(g2d, W, H);
        }
    }

    // Draw the EXP and Lives Status Bar at the Top
    private void drawStatus(Graphics2D g2d) {
        Player p = controller.getCurrentPlayer();
        if (p == null)
            return;
        g2d.setColor(ARC_TEXT);
        g2d.setFont(new Font("Monospaced", Font.PLAIN, 14));
        g2d.drawString("EXP: " + p.getExp() + " / 500", 30, 45);
        g2d.drawString("Lives: " + p.getLives(), 30, 65);
    }

    // Draw the Five Door Selection Grid
    // Selected Door Gets a Semi-Transparent Green Glow Overlay and a Neon Border
    private void drawSelectionPhase(Graphics2D g2d, int W, int H) {
        g2d.setFont(new Font("Monospaced", Font.BOLD, 24));
        g2d.setColor(ARC_LIME);
        drawCenteredText(g2d, "CHOOSE  A  DOOR", W / 2, 100, null);

        Font doorFont = new Font("Monospaced", Font.PLAIN, 13);
        g2d.setFont(doorFont);
        FontMetrics fm = g2d.getFontMetrics();

        int numRows = 12;

        // Loop Through All Rows to Find the True Maximum Rendered Width
        // Guarantees the Highlight Box Always Fully Covers Every Door Row
        int doorW = 0;
        for (int row = 0; row < numRows; row++) {
            doorW = Math.max(doorW, fm.stringWidth(getDoorLine(5, row)));
        }

        int lineH = fm.getHeight() + 1;
        int doorH = numRows * lineH;

        int totalDoorsW = 5 * doorW;
        int remaining = W - 60 - totalDoorsW;
        int gap = Math.max(8, remaining / 6);
        int startX = (W - (totalDoorsW + 4 * gap)) / 2;
        int startY = 120;

        for (int i = 0; i < 5; i++) {
            int dx = startX + i * (doorW + gap);
            boolean isSelected = (i == selectedDoorIndex);

            if (isSelected) {
                // Step 1: Semi-Transparent Green Glow Fill
                // Creates the Translucent Highlighter Pen Effect Over the Entire Door
                g2d.setColor(ARC_GLOW);
                g2d.fillRect(dx - 3, startY - 3, doorW + 6, doorH + 6);

                // Step 2: Neon Green Border Around the Selection
                g2d.setColor(ARC_NEON);
                g2d.setStroke(new BasicStroke(2));
                g2d.drawRect(dx - 3, startY - 3, doorW + 6, doorH + 6);
                g2d.setStroke(new BasicStroke(1));

                // Step 3: Door Text in Bright Lime Green on Top of the Glow
                g2d.setColor(ARC_LIME);
            } else {
                g2d.setColor(ARC_TEXT);
            }

            g2d.setFont(doorFont);
            for (int row = 0; row < numRows; row++) {
                g2d.drawString(getDoorLine(i + 1, row), dx, startY + (row + 1) * lineH);
            }
        }

        // Selected Door Label Below the Grid
        int hintsY = startY + doorH + 28;
        g2d.setColor(ARC_NEON);
        g2d.setFont(new Font("Monospaced", Font.BOLD, 14));
        drawCenteredText(g2d, "DOOR " + (selectedDoorIndex + 1) + "  selected", W / 2, hintsY, null);

        // Navigation Hint at the Bottom
        g2d.setColor(ARC_DIM);
        g2d.setFont(new Font("Monospaced", Font.PLAIN, 13));
        drawCenteredText(g2d,
                "[ ← ] [ → ] Select     [ ENTER ] Open Door     [ ESC ] Back",
                W / 2, H - 30, null);
    }

    // Return One Row of the Door Box for the Given Door Number and Row Index
    private String getDoorLine(int doorNum, int row) {
        return switch (row) {
            case 0 -> "╔═══════════╗";
            case 1 -> "║ ╔══════╗ ║";
            case 2 -> "║ ║  " + doorNum + "  ║ ║";
            case 3 -> "║ ║     ║ ║";
            case 4 -> "║ ║     ║ ║";
            case 5 -> "║ ╚══════╝ ║";
            case 6 -> "()═════════║";
            case 7 -> "║ ╔══════╗ ║";
            case 8 -> "║ ║     ║ ║";
            case 9 -> "║ ║     ║ ║";
            case 10 -> "║ ╚══════╝ ║";
            case 11 -> "╚═══════════╝";
            default -> "";
        };
    }

    // Draw the Reveal Phase Showing the Result Message and the Door ASCII Art
    private void drawRevealPhase(Graphics2D g2d, int W, int H) {
        g2d.setFont(new Font("Monospaced", Font.BOLD, 16));
        FontMetrics fm = g2d.getFontMetrics();
        int msgW = fm.stringWidth(resultMessage) + 50;
        int msgX = (W - msgW) / 2, msgY = 75, msgH = 36;

        g2d.setColor(ARC_NEON);
        g2d.setStroke(new BasicStroke(2));
        g2d.drawRect(msgX, msgY, msgW, msgH);
        g2d.setStroke(new BasicStroke(1));
        g2d.drawString(resultMessage, msgX + 25, msgY + 24);

        Door door = availableDoors.get(selectedDoorIndex);
        String[] art = artForDoor(door);
        int artAreaY = msgY + msgH + 10;
        int artAreaH = H - artAreaY - 45;
        drawScaledArt(g2d, art, 20, artAreaY, W - 40, artAreaH);

        g2d.setFont(new Font("Monospaced", Font.PLAIN, 13));
        g2d.setColor(ARC_DIM);
        String hint = minigamePending ? "[ ENTER ] Play Minigame" : "[ ENTER ] Continue";
        drawCenteredText(g2d, hint, W / 2, H - 25, null);
    }

    // Scale and Render ASCII Art to Fill the Given Rectangle Area
    private void drawScaledArt(Graphics2D g2d, String[] art, int ax, int ay, int aw, int ah) {
        if (art == null || art.length == 0)
            return;
        int fsize = Math.max(5, ah / (art.length + 1));
        while (fsize > 5) {
            g2d.setFont(new Font("Monospaced", Font.PLAIN, fsize));
            FontMetrics fm = g2d.getFontMetrics();
            int maxW = 0;
            for (String ln : art)
                maxW = Math.max(maxW, fm.stringWidth(ln));
            if (maxW <= aw && art.length * fm.getHeight() <= ah)
                break;
            fsize--;
        }
        g2d.setFont(new Font("Monospaced", Font.PLAIN, fsize));
        FontMetrics fm = g2d.getFontMetrics();
        int lh = fm.getHeight();
        int maxW = 0;
        for (String ln : art)
            maxW = Math.max(maxW, fm.stringWidth(ln));
        int startX = ax + Math.max(0, (aw - maxW) / 2);
        int totalH = art.length * lh;
        int startY = ay + Math.max(0, (ah - totalH) / 2);
        g2d.setColor(ARC_TEXT);
        for (int i = 0; i < art.length; i++) {
            g2d.drawString(art[i], startX, startY + (i + 1) * lh);
        }
    }

    // Return the Correct ASCII Art Array for the Given Door Type
    private String[] artForDoor(Door door) {
        if (door instanceof RewardDoor)
            return CHEST_ASCII;
        if (door instanceof PenaltyDoor)
            return POISON_ASCII;
        if (door instanceof NothingDoor)
            return NOTHING_ASCII;
        if (door instanceof MinigameDoor mg) {
            return "PONG".equals(mg.getGameType()) ? PONG_ASCII : SPACEINVADERS_ASCII;
        }
        return NOTHING_ASCII;
    }

    // Open the Selected Door, Apply EXP Changes, and Play the Correct Sounds
    private void openSelectedDoor() {
        if (selectedDoorIndex < 0 || selectedDoorIndex >= availableDoors.size())
            return;
        Door door = availableDoors.get(selectedDoorIndex);
        Player player = controller.getCurrentPlayer();
        if (player == null)
            return;

        SoundManager.playOnce(SoundManager.DOOR_OPEN);
        door.interact(player);

        if (door instanceof RewardDoor r) {
            SoundManager.playOnce(SoundManager.CHEST_SHINE);
            SoundManager.playOnce(SoundManager.REWARD_POINTS);
            resultMessage = "You Found a Shiny Chest!  +" + r.getExpValue() + " EXP!";

        } else if (door instanceof PenaltyDoor pen) {
            SoundManager.playOnce(SoundManager.POISON_SMOKE);
            SoundManager.playOnce(SoundManager.PENALTY_POINTS);
            resultMessage = "Toxic Fumes!  " + Math.abs(pen.getExpValue()) + " EXP Lost!";

        } else if (door instanceof NothingDoor) {
            SoundManager.playOnce(SoundManager.DOOR_CLOSE);
            resultMessage = "The Door Reveals Nothing but an Empty Void...";

        } else if (door instanceof MinigameDoor mg) {
            SoundManager.playOnce(SoundManager.MENU_SELECT);
            minigamePending = true;
            pendingMinigameType = mg.getGameType();
            String gName = "PONG".equals(mg.getGameType()) ? "PONG" : "SPACE INVADERS";
            resultMessage = "A Challenge Awaits!  Press ENTER to Play " + gName + "!";
        }

        doorRevealed = true;
    }

    // Handle All Key Press Events for Navigation and Door Opening
    private void handleKeyPress(int keyCode) {
        if (doorRevealed) {
            if (keyCode == KeyEvent.VK_ENTER) {
                if (minigamePending) {
                    controller.startMinigame(pendingMinigameType);
                    return;
                }
                Player p = controller.getCurrentPlayer();
                if (p != null && (p.getExp() >= 500 || p.getLives() <= 0 || p.getExp() < 0)) {
                    controller.showScreen("GAMEPLAY");
                    return;
                }
                initializeDoors();
                repaint();
            }
            return;
        }

        switch (keyCode) {
            case KeyEvent.VK_LEFT, KeyEvent.VK_A -> {
                selectedDoorIndex = (selectedDoorIndex - 1 + 5) % 5;
                SoundManager.playOnce(SoundManager.DOOR_NAVIGATE);
                repaint();
            }
            case KeyEvent.VK_RIGHT, KeyEvent.VK_D -> {
                selectedDoorIndex = (selectedDoorIndex + 1) % 5;
                SoundManager.playOnce(SoundManager.DOOR_NAVIGATE);
                repaint();
            }
            case KeyEvent.VK_ENTER -> {
                openSelectedDoor();
                repaint();
            }
            case KeyEvent.VK_ESCAPE -> controller.showScreen("GAMEPLAY");
        }
    }

    @Override
    public void keyPressed(KeyEvent e) {
        handleKeyPress(e.getKeyCode());
    }

    @Override
    public void keyReleased(KeyEvent e) {
    }

    @Override
    public void keyTyped(KeyEvent e) {
    }
}