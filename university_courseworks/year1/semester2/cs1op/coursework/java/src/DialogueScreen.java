// DialogueScreen Class - CAPTAIN Dialogue with Astronaut Helmet ASCII Art
// Sound: DIALOGUE_YES on Y, DIALOGUE_NO on N, HORROR_LOOP on Rejection

import java.awt.BasicStroke;
import java.awt.Color;
import java.awt.Font;
import java.awt.FontMetrics;
import java.awt.Graphics;
import java.awt.Graphics2D;
import java.awt.event.KeyAdapter;
import java.awt.event.KeyEvent;
import java.util.ArrayList;
import java.util.List;

public class DialogueScreen extends BaseGameScreen {

    // Introduction Dialogue Lines
    private static final String[] INTRO_LINES = {
        "WELCOME, <USER>!",
        "You look a bit confused.",
        "Don't worry. I'll explain everything.",
        "Basically, you were sent on a mission.",
        "A SPACE MISSION!",
        "Seems obvious but all you got to do is to get enough EXP to go back home.",
        "If you want to know why you're here and everything else.",
        "Beats me, not my problem...",
        "BUT!",
        "At least I'll help you go back.",
        "Deal?"
    };

    // Continuation After Yes to the Deal
    private static final String[] DICE_LINES = {
        "Hey...",
        "I got something to show you...",
        "A lucky dice. A space dice to be exact.",
        "Looks a bit weird... so shiny...",
        "Wanna have a roll?"
    };

    // After Declining the Dice Offer
    private static final String[] DICE_DECLINED_LINES = {
        "Alright then...",
        "We'll manage without it."
    };

    // Rejection Sequence After No to the Deal
    private static final String[] REJECTION_LINES = {
        "Suit yourself...",
        "You drift off into space, contemplating if you agreed to whatever it said to you.",
        "Before you even get to deepen everything about this and whatever comes to your mind.",
        "You simply passed out.",
        "That quick.",
        "Too bad."
    };

    private enum State { INTRODUCTION, DICE_PROMPT, DICE_RESULT, DICE_DECLINED, REJECTION }

    private State state = State.INTRODUCTION;
    private final List<String> lines = new ArrayList<>();
    private int lineIdx = 0;
    private boolean awaitingYN = false;
    private final DiceSystem diceSystem = new DiceSystem();
    private int startingHP = 100;

    // Astronaut Helmet ASCII Art
    private static final String[] HELMET = {
        "                             ##################",
        "                         #####                #####",
        "                      ####                        #####",
        "                   ####                               ####",
        "                 ###           ##############           ###",
        "               ###        #####              #####        ###",
        "             ###    ######                        #######   ###",
        "            ##    ##           ##############           ##   ###",
        "           ##  ###        ########################        ##   ##",
        "          ### ##       ########         #####   #####       ##  ##",
        "         ##  ##    #########            ###       ######     ##  ##",
        "        ##  ##    #######        ##########       ########    ##  ##",
        "        ## ##   #####         ###############   ############   ## ##",
        "        ## ## #####       ####################################  ## ##",
        "        ## ## ####   #########################################   ## ##",
        "  ###### ##  ####    ##########################################  ## ######",
        " ##   ## ##  ####    ##########################################  ## ##   ##",
        " ##   ## ##  ##################################################  ## ##   ##",
        " ##   ## ##  #####   ##########################################  ## ##   ##",
        " ##   ## ##  #####   ##########################################  ## ##   ##",
        " ##   ## ##  ##################################################  ## ##   ##",
        " ##   ## ##  ##########################################   #####  ## ##   ##",
        " ##   ## ##  ########################################       ###  ## ##   ##",
        "  ###### ##  ########################################       ###  ## ######",
        "      ##   ## #########################################   ### #     ##",
        "      ##     ## ################################   ######## ###     ##",
        "        ##    ##  ##############################   ######  ###    ##",
        "        #####   ###  ##################################  ####  #####",
        "        ## ###     ####  ###########################  ####   #### ##",
        "        ## #######     #####                    #####     ####### ##",
        "         ###      ###       ####################       ####     ###",
        "           ####      ####                          ####      ####",
        "              ##        ######                ######        ##",
        "                ####         ##################         ####",
        "                   ####                              ####",
        "                       #######                #######",
        "                              ################",
        "                                                                           ",
        "                                                                           ",
        "                                                                           "
    };

    // Constructor
    public DialogueScreen(GameGUI gui, GameController controller) {
        super(gui, controller);
        loadLines(INTRO_LINES);
        setupKeys();
    }

    // Reset Dialogue to the Start for a New Game
    public void reset() {
        SoundManager.stopSound(SoundManager.HORROR_LOOP);
        state      = State.INTRODUCTION;
        lineIdx    = 0;
        awaitingYN = false;
        startingHP = 100;
        loadLines(INTRO_LINES);
        repaint();
    }

    // Load a Dialogue Array into the Active Line Buffer
    private void loadLines(String[] src) {
        lines.clear();
        String name = controller.getCurrentPlayer() != null
                ? controller.getCurrentPlayer().getName().toUpperCase()
                : "CAPTAIN";
        for (String l : src) lines.add(l.replace("<USER>", name));
        lineIdx    = 0;
        awaitingYN = false;
    }

    private boolean isDecisionState() {
        return state == State.INTRODUCTION || state == State.DICE_PROMPT;
    }

    // Setup Key Input for Advancing Dialogue and Yes/No Responses
    private void setupKeys() {
        addKeyListener(new KeyAdapter() {
            @Override
            public void keyPressed(KeyEvent e) {
                handle(e);
            }
        });
    }

    private void handle(KeyEvent e) {
        char ch   = Character.toUpperCase(e.getKeyChar());
        int  code = e.getKeyCode();

        if (code == KeyEvent.VK_ESCAPE && state == State.REJECTION) {
            SoundManager.stopSound(SoundManager.HORROR_LOOP);
            controller.showScreen("MAIN_MENU");
            return;
        }

        if (awaitingYN) {
            if (ch == 'Y') { onYes(); repaint(); return; }
            if (ch == 'N') { onNo();  repaint(); return; }
            return;
        }

        if (code == KeyEvent.VK_ENTER) {
            SoundManager.playOnce(SoundManager.MENU_NAVIGATE);
            if (lineIdx < lines.size() - 1) {
                lineIdx++;
                if (lineIdx == lines.size() - 1 && isDecisionState()) awaitingYN = true;
            } else {
                onEndOfLines();
            }
            repaint();
        }
    }

    private void onYes() {
        awaitingYN = false;
        SoundManager.playOnce(SoundManager.DIALOGUE_YES);
        switch (state) {
            case INTRODUCTION -> { state = State.DICE_PROMPT; loadLines(DICE_LINES); }
            case DICE_PROMPT -> {
                diceSystem.roll();
                startingHP = diceSystem.getHPFromRoll(diceSystem.getLastRoll());
                state = State.DICE_RESULT;
                lines.clear();
                lines.add("Alright!");
                lines.add("You rolled a " + diceSystem.getLastRoll() + "!  Starting EXP: " + startingHP + ".");
                lines.add("Let's get started!");
                lineIdx = 0;
            }
            default -> {}
        }
    }

    private void onNo() {
        awaitingYN = false;
        SoundManager.playOnce(SoundManager.DIALOGUE_NO);
        switch (state) {
            case INTRODUCTION -> {
                state = State.REJECTION;
                loadLines(REJECTION_LINES);
                SoundManager.playLoop(SoundManager.HORROR_LOOP);
            }
            case DICE_PROMPT -> { state = State.DICE_DECLINED; loadLines(DICE_DECLINED_LINES); }
            default -> {}
        }
    }

    private void onEndOfLines() {
        switch (state) {
            case DICE_RESULT, DICE_DECLINED -> {
                if (controller.getCurrentPlayer() != null)
                    controller.getCurrentPlayer().setExp(startingHP);
                controller.startDoorSelection();
            }
            case REJECTION -> {
                SoundManager.stopSound(SoundManager.HORROR_LOOP);
                controller.showScreen("MAIN_MENU");
            }
            default -> {}
        }
    }

    // Render the Dialogue Screen
    @Override
    protected void paintComponent(Graphics g) {
        super.paintComponent(g);
        Graphics2D g2d = (Graphics2D) g;
        enableAntiAliasing(g2d);
        int W = getWidth(), H = getHeight();
        if (state == State.REJECTION) drawFullScreen(g2d, W, H);
        else                          drawHelmetScene(g2d, W, H);
    }

    // Rejection Sequence - Full Screen No Helmet
    private void drawFullScreen(Graphics2D g2d, int W, int H) {
        int bx = 30, by = 50, bw = W - 60, bh = H - 100;
        pokeBorder(g2d, bx, by, bw, bh);
        g2d.setColor(new Color(0, 0, 0, 200));
        g2d.fillRect(bx + 4, by + 4, bw - 8, bh - 8);
        g2d.setColor(ARC_TEXT);
        g2d.setFont(new Font("Monospaced", Font.PLAIN, 22));
        drawWrapped(g2d, lineIdx < lines.size() ? lines.get(lineIdx) : "", bx + 30, by + 60, bw - 60, 30);
        if (lineIdx < lines.size() - 1) drawHint(g2d, bx + bw - 14, by + bh - 14);

        g2d.setFont(new Font("Monospaced", Font.PLAIN, 11));
        g2d.setColor(ARC_DIM);
        g2d.drawString("[ ESC ] Return to Menu", bx + 10, by + bh - 10);
    }

    // Main Scene with Helmet Art
    private void drawHelmetScene(Graphics2D g2d, int W, int H) {
        int bubbleH = Math.max(125, H / 6);
        int bx = 10, by = 8, bw = W - 20;
        pokeBorder(g2d, bx, by, bw, bubbleH);
        g2d.setColor(new Color(0, 0, 0, 215));
        g2d.fillRect(bx + 4, by + 4, bw - 8, bubbleH - 8);

        String text = lineIdx < lines.size() ? lines.get(lineIdx) : "";
        g2d.setColor(ARC_TEXT);
        g2d.setFont(new Font("Monospaced", Font.BOLD, 18));
        drawWrapped(g2d, text, bx + 20, by + 45, bw - 40, 28);

        if (awaitingYN) {
            g2d.setFont(new Font("Monospaced", Font.BOLD, 16));
            g2d.setColor(ARC_LIME);
            String prompt = "[ Y ] Yes                         [ N ] No";
            FontMetrics fm = g2d.getFontMetrics();
            g2d.drawString(prompt, bx + (bw - fm.stringWidth(prompt)) / 2, by + bubbleH - 14);
        } else if (lineIdx < lines.size() - 1 || state == State.DICE_RESULT) {
            drawHint(g2d, bx + bw - 12, by + bubbleH - 10);
        }

        // Player Name Box
        String playerName = controller.getCurrentPlayer() != null
                ? controller.getCurrentPlayer().getName().toUpperCase()
                : "CAPTAIN";
        if (playerName.length() > 15) playerName = playerName.substring(0, 15);

        int nameFS = playerName.length() <= 8 ? 22 : (playerName.length() <= 12 ? 17 : 14);
        g2d.setFont(new Font("Monospaced", Font.BOLD, nameFS));
        FontMetrics nFm = g2d.getFontMetrics();
        int nW = nFm.stringWidth(playerName);
        int nPad = 14;
        int nBW  = nW + nPad * 2, nBH = nameFS + 12;
        int nBX  = W / 2 - nBW / 2;
        int nBY  = by + bubbleH + 10;
        g2d.setColor(ARC_NEON);
        g2d.setStroke(new BasicStroke(2));
        g2d.drawRect(nBX, nBY, nBW, nBH);
        g2d.drawString(playerName, nBX + nPad, nBY + nameFS + 1);

        // Helmet or Dice Art in Lower Area
        int artTop = nBY + nBH + 20;
        int artH   = H - artTop - 5;

        if (state == State.DICE_RESULT) drawDiceArt(g2d, W, artTop, artH);
        else                            drawHelmet(g2d, W, artTop, artH);
    }

    // Render Dice Face Art
    private void drawDiceArt(Graphics2D g2d, int W, int artTop, int artH) {
        int roll = Math.max(1, Math.min(6, diceSystem.getLastRoll()));
        String[] face = diceSystem.getDiceFaceArray(roll);
        if (face == null || face.length == 0) return;

        int fsize = Math.min(52, artH / (face.length + 3));
        while (fsize > 8) {
            g2d.setFont(new Font("Monospaced", Font.PLAIN, fsize));
            FontMetrics fm = g2d.getFontMetrics();
            int maxW = 0;
            for (String l : face) maxW = Math.max(maxW, fm.stringWidth(l));
            if (maxW <= W - 40) break;
            fsize--;
        }
        g2d.setFont(new Font("Monospaced", Font.PLAIN, fsize));
        FontMetrics fm = g2d.getFontMetrics();
        int lh = fm.getHeight();
        int maxW = 0;
        for (String l : face) maxW = Math.max(maxW, fm.stringWidth(l));
        int startX = (W - maxW) / 2;
        int totalH = face.length * lh;
        int startY = artTop + (artH - totalH) / 2;

        g2d.setColor(ARC_TEXT);
        for (int i = 0; i < face.length; i++) g2d.drawString(face[i], startX, startY + (i + 1) * lh);

        g2d.setFont(new Font("Monospaced", Font.BOLD, Math.max(14, fsize / 2)));
        g2d.setColor(ARC_DIM);
        String cap = "Rolled: " + roll + "   |   Starting EXP: " + startingHP;
        fm = g2d.getFontMetrics();
        g2d.drawString(cap, (W - fm.stringWidth(cap)) / 2, startY + totalH + lh + 4);
    }

    // Render Helmet ASCII Art
    private void drawHelmet(Graphics2D g2d, int W, int artTop, int artH) {
        int fsize = Math.max(7, artH / (HELMET.length + 2));
        while (fsize > 7) {
            g2d.setFont(new Font("Monospaced", Font.PLAIN, fsize));
            FontMetrics fm = g2d.getFontMetrics();
            int maxW = 0;
            for (String l : HELMET) maxW = Math.max(maxW, fm.stringWidth(l));
            if (maxW <= W - 8) break;
            fsize--;
        }
        g2d.setFont(new Font("Monospaced", Font.PLAIN, fsize));
        FontMetrics fm = g2d.getFontMetrics();
        int lh     = fsize + 2;
        int maxW   = 0;
        for (String l : HELMET) maxW = Math.max(maxW, fm.stringWidth(l));
        int startX = Math.max(4, (W - maxW) / 2);
        int totalH = HELMET.length * lh;
        int startY = artTop + Math.max(0, (artH - totalH) / 2);

        g2d.setColor(ARC_TEXT);
        for (int i = 0; i < HELMET.length; i++) g2d.drawString(HELMET[i], startX, startY + (i + 1) * lh);
    }

    // Draw Decorative Border with Corner Accents
    private void pokeBorder(Graphics2D g2d, int x, int y, int w, int h) {
        g2d.setColor(ARC_NEON);
        g2d.setStroke(new BasicStroke(3));
        g2d.drawRect(x, y, w, h);
        g2d.setStroke(new BasicStroke(1));
        int cs = 6;
        g2d.drawRect(x + 4, y + 4, cs, cs);
        g2d.drawRect(x + w - cs - 4, y + 4, cs, cs);
        g2d.drawRect(x + 4, y + h - cs - 4, cs, cs);
        g2d.drawRect(x + w - cs - 4, y + h - cs - 4, cs, cs);
        g2d.setStroke(new BasicStroke(2));
    }

    // Draw Enter Hint Arrow
    private void drawHint(Graphics2D g2d, int rx, int ry) {
        g2d.setFont(new Font("Monospaced", Font.PLAIN, 12));
        g2d.setColor(ARC_DIM);
        String s = "[ENTER \u25ba]";
        FontMetrics fm = g2d.getFontMetrics();
        g2d.drawString(s, rx - fm.stringWidth(s), ry);
    }

    // Word-Wrapped Text Drawing
    private void drawWrapped(Graphics2D g2d, String text, int x, int y, int maxW, int lh) {
        FontMetrics fm = g2d.getFontMetrics();
        int cx = x, cy = y;
        for (String word : text.split(" ")) {
            int ww = fm.stringWidth(word + " ");
            if (cx + ww > x + maxW) { cy += lh; cx = x; }
            g2d.drawString(word, cx, cy);
            cx += ww;
        }
    }
}