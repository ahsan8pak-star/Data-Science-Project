// PongMinigame Class - Smooth Pong with CPU AI and Difficulty Scaling
// All Colors Are Arcade Green on Black - No Red Anywhere
// Hit Sound Cooldowns Prevent Duplicate Sounds When Ball Lingers Inside a Paddle
// Sounds Load via SoundManager Multi-Path Resolution for Reliable Registration
// ESC Opens the Pause Menu Overlay with CRT and Sound Volume Controls

import java.awt.BasicStroke;
import java.awt.Color;
import java.awt.Font;
import java.awt.FontMetrics;
import java.awt.Graphics;
import java.awt.Graphics2D;
import java.awt.Rectangle;
import java.awt.RenderingHints;
import java.awt.event.KeyEvent;
import java.awt.event.KeyListener;
import java.awt.event.MouseEvent;
import java.awt.event.MouseListener;
import java.awt.event.MouseMotionListener;
import java.util.HashMap;
import java.util.HashSet;
import java.util.Map;
import java.util.Random;
import java.util.Set;
import javax.swing.JPanel;

public class PongMinigame extends JPanel implements KeyListener, MouseListener, MouseMotionListener {

    // Arcade Color Palette - Green on Black
    private static final Color ARC_NEON = new Color(0, 255, 65);
    private static final Color ARC_LIME = new Color(100, 255, 60);
    private static final Color ARC_TEXT = new Color(0, 215, 0);
    private static final Color ARC_DIM = new Color(0, 145, 0);
    private static final Color ARC_PANEL = new Color(0, 45, 0);
    private static final Color ARC_GLOW = new Color(0, 200, 0, 70);

    // Logical Game Dimensions
    private static final int GW = 800, GH = 600;
    private static final int PW = 12, PH = 100, BS = 12;
    private static final int PS = 8;
    private static final int BALL_BASE = 5;
    private static final int LEFT_X = 24;
    private static final int RIGHT_X = GW - 24 - PW;

    // Game State
    private int leftY = GH / 2 - PH / 2;
    private int rightY = GH / 2 - PH / 2;
    private double bx = GW / 2.0, by = GH / 2.0;
    private double vx = BALL_BASE, vy = BALL_BASE;
    private int leftScore = 0, rightScore = 0, winScore = 3;

    // Held Keys for Smooth Movement
    private final Set<Integer> keys = new HashSet<>();

    // Game Flow Flags
    private boolean active = true;
    private boolean paused = false;
    private boolean gameEnded = false;
    private boolean playerWon = false;
    private boolean endSoundPlayed = false;
    private String endMsg = "";
    private Thread loop;

    // Hit Cooldown Flags - Prevent Duplicate Sounds per Paddle Contact
    private boolean playerHitActive = false;
    private boolean cpuHitActive = false;

    // AI Variables
    private final Random rng = new Random();
    private double aiTargetY = GH / 2.0;
    private int aiUpdateTick = 0;

    // Controller and Name
    private GameController controller;
    private String playerName = "PLAYER";

    // Pause Menu State
    private boolean showPauseMenu = false;
    private PauseTab pauseTab = PauseTab.MAIN;

    private enum PauseTab {
        MAIN, SOUND
    }

    private String draggingSlider = null;
    private final HashMap<String, Rectangle> sliderRects = new HashMap<>();
    private Rectangle crtSliderRect = null;
    private Rectangle resumeRect = null;
    private Rectangle quitRect = null;
    private Rectangle soundTabRect = null;
    private Rectangle mainTabRect = null;

    // Difficulty Helpers
    private int aiSpeed() {
        return switch (GameSettings.getDifficulty()) {
            case EASY -> 3;
            case NORMAL -> 5;
            case HARD -> 7;
        };
    }

    private int aiDeadZone() {
        return switch (GameSettings.getDifficulty()) {
            case EASY -> 55;
            case NORMAL -> 18;
            case HARD -> 5;
        };
    }

    private int aiReactionDelay() {
        return switch (GameSettings.getDifficulty()) {
            case EASY -> 12;
            case NORMAL -> 6;
            case HARD -> 2;
        };
    }

    private float aiMissChance() {
        return switch (GameSettings.getDifficulty()) {
            case EASY -> 0.30f;
            case NORMAL -> 0.07f;
            case HARD -> 0.01f;
        };
    }

    // Constructors
    public PongMinigame(GameController controller) {
        this.controller = controller;
        if (controller != null && controller.getCurrentPlayer() != null) {
            playerName = controller.getCurrentPlayer().getName();
            int exp = controller.getCurrentPlayer().getExp();
            winScore = exp <= 200 ? 3 : exp <= 350 ? 5 : 7;
        }
        initGame();
    }

    public PongMinigame() {
        this(0);
    }

    public PongMinigame(int exp) {
        winScore = exp <= 200 ? 3 : exp <= 350 ? 5 : 7;
        initGame();
    }

    // Initialise and Start the Game Loop
    private void initGame() {
        setBackground(Color.BLACK);
        setFocusable(true);
        addKeyListener(this);
        addMouseListener(this);
        addMouseMotionListener(this);
        startLoop();
    }

    // Main Game Loop at ~60 FPS
    private void startLoop() {
        loop = new Thread(() -> {
            while (active) {
                if (!paused && !gameEnded && !showPauseMenu) {
                    movePlayerPaddle();
                    moveAI();
                    moveBall();
                    checkScore();
                }
                repaint();
                try {
                    Thread.sleep(16);
                } catch (InterruptedException ex) {
                    break;
                }
            }
        }, "pong-loop");
        loop.setDaemon(true);
        loop.start();
    }

    // Move Player Paddle from Held Keys
    private void movePlayerPaddle() {
        if (keys.contains(KeyEvent.VK_W) || keys.contains(KeyEvent.VK_UP))
            leftY = Math.max(0, leftY - PS);
        if (keys.contains(KeyEvent.VK_S) || keys.contains(KeyEvent.VK_DOWN))
            leftY = Math.min(GH - PH, leftY + PS);
    }

    // CPU AI Paddle Movement with Difficulty Scaling
    private void moveAI() {
        if (keys.contains(KeyEvent.VK_I)) {
            rightY = Math.max(0, rightY - PS);
            return;
        }
        if (keys.contains(KeyEvent.VK_K)) {
            rightY = Math.min(GH - PH, rightY + PS);
            return;
        }
        if (vx > 0) {
            aiUpdateTick++;
            if (aiUpdateTick >= aiReactionDelay()) {
                aiUpdateTick = 0;
                aiTargetY = rng.nextFloat() < aiMissChance() ? GH / 2.0 : by + BS / 2.0;
            }
            int mid = rightY + PH / 2;
            int target = (int) aiTargetY;
            if (target < mid - aiDeadZone())
                rightY = Math.max(0, rightY - aiSpeed());
            else if (target > mid + aiDeadZone())
                rightY = Math.min(GH - PH, rightY + aiSpeed());
        } else {
            int centre = GH / 2 - PH / 2;
            if (rightY < centre)
                rightY = Math.min(centre, rightY + 2);
            else if (rightY > centre)
                rightY = Math.max(centre, rightY - 2);
        }
    }

    // Ball Movement and Collision with Cooldown-Guarded Sounds
    private void moveBall() {
        bx += vx;
        by += vy;

        if (by <= 0) {
            by = 0;
            vy = Math.abs(vy);
        }
        if (by >= GH - BS) {
            by = GH - BS;
            vy = -Math.abs(vy);
        }

        boolean touchingLeft = vx < 0
                && bx <= LEFT_X + PW && bx >= LEFT_X - Math.abs(vx)
                && by + BS >= leftY && by <= leftY + PH;

        if (touchingLeft) {
            if (!playerHitActive) {
                playerHitActive = true;
                bx = LEFT_X + PW;
                vx = -vx;
                vy = ((by + BS / 2.0) - (leftY + PH / 2.0)) / (PH / 2.0) * BALL_BASE * 1.5;
                SoundManager.playOnce(SoundManager.PONG_PLAYER_HIT);
            }
        } else {
            playerHitActive = false;
        }

        boolean touchingRight = vx > 0
                && bx + BS >= RIGHT_X && bx + BS <= RIGHT_X + PW + Math.abs(vx)
                && by + BS >= rightY && by <= rightY + PH;

        if (touchingRight) {
            if (!cpuHitActive) {
                cpuHitActive = true;
                bx = RIGHT_X - BS;
                vx = -vx;
                vy = ((by + BS / 2.0) - (rightY + PH / 2.0)) / (PH / 2.0) * BALL_BASE * 1.5;
                SoundManager.playOnce(SoundManager.PONG_CPU_HIT);
            }
        } else {
            cpuHitActive = false;
        }
    }

    // Score and End Game Check
    private void checkScore() {
        if (bx < -BS) {
            rightScore++;
            SoundManager.playOnce(SoundManager.PONG_CPU_POINT);
            resetBall(-1);
        } else if (bx > GW) {
            leftScore++;
            SoundManager.playOnce(SoundManager.PONG_PLAYER_POINT);
            resetBall(1);
        }

        if (!gameEnded && (leftScore >= winScore || rightScore >= winScore)) {
            active = false;
            gameEnded = true;
            playerWon = (leftScore >= winScore);
            endMsg = playerWon ? playerName.toUpperCase() + " WINS!" : "CPU WINS!";

            if (!endSoundPlayed) {
                endSoundPlayed = true;
                if (playerWon)
                    SoundManager.playOnce(SoundManager.PONG_WIN);
                else
                    SoundManager.playLoop(SoundManager.PONG_LOSE);
            }
        }
    }

    // Reset Ball After a Point with Brief Pause
    private void resetBall(int dir) {
        bx = GW / 2.0;
        by = GH / 2.0;
        vx = dir * BALL_BASE;
        vy = (rng.nextDouble() - 0.5) * BALL_BASE;
        aiTargetY = GH / 2.0;
        playerHitActive = false;
        cpuHitActive = false;
        paused = true;
        new Thread(() -> {
            try {
                Thread.sleep(750);
            } catch (InterruptedException ignored) {
            }
            paused = false;
        }).start();
    }

    // Render Game Field with All Arcade Colors
    @Override
    protected void paintComponent(Graphics g) {
        super.paintComponent(g);
        Graphics2D g2d = (Graphics2D) g;
        g2d.setRenderingHint(RenderingHints.KEY_ANTIALIASING, RenderingHints.VALUE_ANTIALIAS_ON);

        int pw = getWidth(), ph = getHeight();
        double sx = pw / (double) GW, sy = ph / (double) GH;

        // Centre Dashed Line
        g2d.setColor(ARC_DIM);
        g2d.setStroke(new BasicStroke(2, BasicStroke.CAP_BUTT, BasicStroke.JOIN_BEVEL,
                0, new float[] { (float) (10 * sy), (float) (10 * sy) }, 0));
        g2d.drawLine(pw / 2, 0, pw / 2, ph);
        g2d.setStroke(new BasicStroke(1));

        // Paddles and Ball in Neon Green
        g2d.setColor(ARC_NEON);
        g2d.fillRect(s(LEFT_X, sx), s(leftY, sy), s(PW, sx), s(PH, sy));
        g2d.fillRect(s(RIGHT_X, sx), s(rightY, sy), s(PW, sx), s(PH, sy));
        g2d.fillOval(s((int) bx, sx), s((int) by, sy), s(BS, sx), s(BS, sx));

        // Scores in Lime Green
        g2d.setFont(new Font("Monospaced", Font.BOLD, (int) (36 * Math.min(sx, sy))));
        g2d.setColor(ARC_LIME);
        g2d.drawString(String.valueOf(leftScore), (int) (pw * 0.25), (int) (50 * sy));
        g2d.drawString(String.valueOf(rightScore), (int) (pw * 0.72), (int) (50 * sy));

        // Labels in Standard Text Green
        g2d.setFont(new Font("Monospaced", Font.PLAIN, (int) (14 * Math.min(sx, sy))));
        g2d.setColor(ARC_TEXT);
        g2d.drawString(playerName.toUpperCase(), (int) (pw * 0.07), (int) (50 * sy));
        g2d.drawString("CPU [" + GameSettings.difficultyLabel() + "]", (int) (pw * 0.60), (int) (50 * sy));

        // Win Target in Dim Green
        g2d.setColor(ARC_DIM);
        String targetH = "First to " + winScore;
        FontMetrics fm = g2d.getFontMetrics();
        g2d.drawString(targetH, (pw - fm.stringWidth(targetH)) / 2, (int) (30 * sy));

        // Controls Hint
        g2d.setColor(new Color(0, 80, 0));
        g2d.setFont(new Font("Monospaced", Font.PLAIN, (int) (11 * Math.min(sx, sy))));
        g2d.drawString("W / Up  S / Down: Paddle   I / K: Override CPU   P: Pause   ESC: Menu",
                (int) (16 * sx), ph - (int) (10 * sy));

        CRTSettings.drawCRT(g2d, pw, ph);

        // Game Over Overlay - All Green No Red
        if (gameEnded) {
            g2d.setColor(new Color(0, 0, 0, 170));
            g2d.fillRect(0, 0, pw, ph);
            g2d.setColor(playerWon ? ARC_LIME : ARC_TEXT);
            g2d.setFont(new Font("Monospaced", Font.BOLD, (int) (50 * Math.min(sx, sy))));
            fm = g2d.getFontMetrics();
            g2d.drawString(endMsg, (pw - fm.stringWidth(endMsg)) / 2, ph / 2);
            g2d.setColor(ARC_NEON);
            g2d.setFont(new Font("Monospaced", Font.PLAIN, (int) (20 * Math.min(sx, sy))));
            String sub = "Press ENTER to Continue";
            fm = g2d.getFontMetrics();
            g2d.drawString(sub, (pw - fm.stringWidth(sub)) / 2, ph / 2 + (int) (65 * sy));
            return;
        }

        if (showPauseMenu)
            drawPauseMenu(g2d, pw, ph);
    }

    // Render Pause Menu with CRT and Sound Tabs - All Green
    private void drawPauseMenu(Graphics2D g2d, int pw, int ph) {
        g2d.setColor(new Color(0, 0, 0, 210));
        g2d.fillRect(0, 0, pw, ph);

        int boxW = Math.min(620, pw - 80);
        int boxH = ph - 80;
        int boxX = (pw - boxW) / 2;
        int boxY = 40;

        g2d.setColor(ARC_NEON);
        g2d.setStroke(new BasicStroke(3));
        g2d.drawRect(boxX, boxY, boxW, boxH);
        g2d.setStroke(new BasicStroke(1));

        g2d.setFont(new Font("Monospaced", Font.BOLD, 28));
        FontMetrics fm = g2d.getFontMetrics();
        g2d.setColor(ARC_LIME);
        String title = "PAUSED";
        g2d.drawString(title, boxX + (boxW - fm.stringWidth(title)) / 2, boxY + 38);

        int tabY = boxY + 56, tabW = boxW / 2 - 20, tabH = 30;
        mainTabRect = new Rectangle(boxX + 10, tabY, tabW, tabH);
        soundTabRect = new Rectangle(boxX + boxW / 2 + 10, tabY, tabW, tabH);

        drawPauseTab(g2d, "CRT / DISPLAY", mainTabRect, pauseTab == PauseTab.MAIN);
        drawPauseTab(g2d, "SOUND VOLUMES", soundTabRect, pauseTab == PauseTab.SOUND);

        int contentY = tabY + tabH + 16;
        int contentH = boxH - (contentY - boxY) - 60;

        if (pauseTab == PauseTab.MAIN)
            drawCRTPanel(g2d, boxX + 10, contentY, boxW - 20, contentH);
        else
            drawSoundPanel(g2d, boxX + 10, contentY, boxW - 20, contentH);

        int btnY = boxY + boxH - 48, btnW = boxW / 2 - 20;
        resumeRect = new Rectangle(boxX + 10, btnY, btnW, 36);
        quitRect = new Rectangle(boxX + boxW / 2 + 10, btnY, btnW, 36);

        // Resume - Neon Green Button
        g2d.setColor(ARC_TEXT);
        g2d.fillRect(resumeRect.x, resumeRect.y, resumeRect.width, resumeRect.height);
        g2d.setColor(ARC_NEON);
        g2d.setStroke(new BasicStroke(2));
        g2d.drawRect(resumeRect.x, resumeRect.y, resumeRect.width, resumeRect.height);
        g2d.setStroke(new BasicStroke(1));
        g2d.setFont(new Font("Monospaced", Font.BOLD, 16));
        fm = g2d.getFontMetrics();
        g2d.setColor(Color.BLACK);
        g2d.drawString("RESUME", resumeRect.x + (resumeRect.width - fm.stringWidth("RESUME")) / 2,
                resumeRect.y + resumeRect.height / 2 + fm.getAscent() / 2 - 2);

        // Quit - Dark Green Button (No Red)
        g2d.setColor(ARC_PANEL);
        g2d.fillRect(quitRect.x, quitRect.y, quitRect.width, quitRect.height);
        g2d.setColor(ARC_DIM);
        g2d.setStroke(new BasicStroke(2));
        g2d.drawRect(quitRect.x, quitRect.y, quitRect.width, quitRect.height);
        g2d.setStroke(new BasicStroke(1));
        g2d.setColor(ARC_TEXT);
        g2d.drawString("QUIT", quitRect.x + (quitRect.width - fm.stringWidth("QUIT")) / 2,
                quitRect.y + quitRect.height / 2 + fm.getAscent() / 2 - 2);
    }

    // Draw a Pause Menu Tab Button
    private void drawPauseTab(Graphics2D g2d, String label, Rectangle r, boolean active) {
        g2d.setColor(active ? ARC_TEXT : ARC_PANEL);
        g2d.fillRect(r.x, r.y, r.width, r.height);
        g2d.setColor(ARC_NEON);
        g2d.setStroke(new BasicStroke(1));
        g2d.drawRect(r.x, r.y, r.width, r.height);
        g2d.setFont(new Font("Monospaced", Font.BOLD, 13));
        FontMetrics fm = g2d.getFontMetrics();
        g2d.setColor(active ? Color.BLACK : ARC_DIM);
        g2d.drawString(label, r.x + (r.width - fm.stringWidth(label)) / 2,
                r.y + r.height / 2 + fm.getAscent() / 2 - 2);
    }

    // Draw the CRT Settings Panel Inside the Pause Menu
    private void drawCRTPanel(Graphics2D g2d, int x, int y, int w, int h) {
        sliderRects.clear();
        int cy = y + 14;

        g2d.setFont(new Font("Monospaced", Font.BOLD, 15));
        g2d.setColor(ARC_TEXT);
        g2d.drawString("CRT Effect:", x, cy + 14);

        int togX = x + 120;
        Rectangle onRect = new Rectangle(togX, cy, 56, 26);
        Rectangle offRect = new Rectangle(togX + 64, cy, 56, 26);

        // ON Button
        boolean enabled = CRTSettings.isEnabled();
        g2d.setColor(enabled ? ARC_TEXT : ARC_PANEL);
        g2d.fillRect(onRect.x, onRect.y, onRect.width, onRect.height);
        g2d.setColor(enabled ? ARC_NEON : ARC_DIM);
        g2d.drawRect(onRect.x, onRect.y, onRect.width, onRect.height);
        g2d.setFont(new Font("Monospaced", Font.BOLD, 12));
        g2d.setColor(enabled ? Color.BLACK : ARC_DIM);
        g2d.drawString("ON", onRect.x + 14, onRect.y + 17);

        // OFF Button - Dark Green Not Red
        g2d.setColor(!enabled ? ARC_PANEL : new Color(0, 25, 0));
        g2d.fillRect(offRect.x, offRect.y, offRect.width, offRect.height);
        g2d.setColor(!enabled ? ARC_NEON : ARC_DIM);
        g2d.drawRect(offRect.x, offRect.y, offRect.width, offRect.height);
        g2d.setColor(!enabled ? ARC_LIME : ARC_DIM);
        g2d.drawString("OFF", offRect.x + 8, offRect.y + 17);

        sliderRects.put("CRT_ON", onRect);
        sliderRects.put("CRT_OFF", offRect);
        cy += 44;

        // CRT Intensity Slider
        g2d.setFont(new Font("Monospaced", Font.BOLD, 15));
        g2d.setColor(enabled ? ARC_TEXT : ARC_DIM);
        g2d.drawString("Intensity:", x, cy + 14);

        int sX = x + 120, sW = w - 160, sH = 16;
        crtSliderRect = new Rectangle(sX, cy, sW, sH);
        float fill = CRTSettings.getIntensity() / 100.0f;

        g2d.setColor(ARC_PANEL);
        g2d.fillRect(sX, cy, sW, sH);
        g2d.setColor(enabled ? ARC_TEXT : new Color(0, 40, 0));
        g2d.fillRect(sX, cy, (int) (sW * fill), sH);
        g2d.setColor(enabled ? ARC_NEON : ARC_DIM);
        g2d.drawRect(sX, cy, sW, sH);

        int thumbX = sX + (int) (sW * fill) - 4;
        g2d.setColor(ARC_LIME);
        g2d.fillRect(thumbX, cy - 3, 8, sH + 6);

        g2d.setFont(new Font("Monospaced", Font.BOLD, 13));
        g2d.setColor(ARC_NEON);
        g2d.drawString(CRTSettings.getIntensity() + "%", sX + sW + 8, cy + 13);
        cy += 36;

        g2d.setFont(new Font("Monospaced", Font.PLAIN, 12));
        g2d.setColor(ARC_DIM);
        g2d.drawString("0-33: Scanlines Only   34-66: Plus Vignette   67-100: Plus Flicker", x, cy + 14);
    }

    // Draw Sound Volume Sliders Inside the Pause Menu
    private void drawSoundPanel(Graphics2D g2d, int x, int y, int w, int h) {
        String[] pongSounds = SoundSettings.getSoundFilesForCategory("Pong");
        String[] generalSounds = SoundSettings.getGeneralSoundFiles();

        int cy = y, labelW = 180, sX = x + labelW, sW = w - labelW - 60, rowH = 26;
        Font lf = new Font("Monospaced", Font.BOLD, 12);
        Font vf = new Font("Monospaced", Font.PLAIN, 11);

        g2d.setFont(new Font("Monospaced", Font.BOLD, 13));
        g2d.setColor(ARC_TEXT);
        g2d.drawString("PONG SOUNDS", x, cy + 13);
        cy += 20;

        for (String sf : pongSounds) {
            drawSoundRow(g2d, sf, x, cy, labelW, sX, sW, rowH, lf, vf);
            cy += rowH;
        }

        cy += 8;
        g2d.setFont(new Font("Monospaced", Font.BOLD, 13));
        g2d.setColor(ARC_TEXT);
        g2d.drawString("GENERAL SOUNDS", x, cy + 13);
        cy += 20;

        int maxRows = (h - (cy - y)) / rowH, shown = 0;
        for (String sf : generalSounds) {
            if (shown >= maxRows)
                break;
            drawSoundRow(g2d, sf, x, cy, labelW, sX, sW, rowH, lf, vf);
            cy += rowH;
            shown++;
        }
    }

    // Draw a Single Sound Slider Row
    private void drawSoundRow(Graphics2D g2d, String sf, int x, int cy,
            int labelW, int sX, int sW, int rowH, Font lf, Font vf) {
        String name = SoundSettings.getDisplayName(sf);
        int vol = SoundSettings.getVolume(sf);

        g2d.setFont(lf);
        g2d.setColor(ARC_TEXT);
        String shortName = name.length() > 20 ? name.substring(0, 19) + "." : name;
        g2d.drawString(shortName, x, cy + rowH - 8);

        Rectangle r = new Rectangle(sX, cy + 4, sW, rowH - 10);
        sliderRects.put(sf, r);

        g2d.setColor(ARC_PANEL);
        g2d.fillRect(r.x, r.y, r.width, r.height);
        g2d.setColor(ARC_TEXT);
        g2d.fillRect(r.x, r.y, (int) (r.width * vol / 100.0), r.height);
        g2d.setColor(ARC_NEON);
        g2d.drawRect(r.x, r.y, r.width, r.height);

        int tx = r.x + (int) (r.width * vol / 100.0) - 3;
        g2d.setColor(ARC_LIME);
        g2d.fillRect(tx, r.y - 2, 6, r.height + 4);

        g2d.setFont(vf);
        g2d.setColor(ARC_DIM);
        g2d.drawString(vol + "%", r.x + r.width + 6, cy + rowH - 7);
    }

    // Key Pressed Handler
    @Override
    public void keyPressed(KeyEvent e) {
        keys.add(e.getKeyCode());

        if (gameEnded) {
            if (e.getKeyCode() == KeyEvent.VK_ENTER && controller != null) {
                SoundManager.stopSound(SoundManager.PONG_LOSE);
                SoundManager.stopAll();
                if (playerWon)
                    controller.onMinigameWon("PONG", 50);
                else
                    controller.onMinigameLost();
            }
            return;
        }

        if (showPauseMenu) {
            if (e.getKeyCode() == KeyEvent.VK_ESCAPE) {
                showPauseMenu = false;
                repaint();
            }
            return;
        }

        if (e.getKeyCode() == KeyEvent.VK_P)
            paused = !paused;
        if (e.getKeyCode() == KeyEvent.VK_ESCAPE) {
            showPauseMenu = true;
            pauseTab = PauseTab.MAIN;
            repaint();
        }
    }

    @Override
    public void keyReleased(KeyEvent e) {
        keys.remove(e.getKeyCode());
    }

    @Override
    public void keyTyped(KeyEvent e) {
    }

    // Mouse Pressed Handler for Pause Menu Interactions
    @Override
    public void mousePressed(MouseEvent e) {
        if (!showPauseMenu)
            return;
        java.awt.Point p = e.getPoint();

        if (mainTabRect != null && mainTabRect.contains(p)) {
            pauseTab = PauseTab.MAIN;
            repaint();
            return;
        }
        if (soundTabRect != null && soundTabRect.contains(p)) {
            pauseTab = PauseTab.SOUND;
            repaint();
            return;
        }
        if (resumeRect != null && resumeRect.contains(p)) {
            showPauseMenu = false;
            repaint();
            return;
        }

        if (quitRect != null && quitRect.contains(p)) {
            active = false;
            SoundManager.stopSound(SoundManager.PONG_LOSE);
            if (controller != null)
                controller.showScreen("DOOR_SELECTION");
            return;
        }

        if (pauseTab == PauseTab.MAIN) {
            Rectangle onR = sliderRects.get("CRT_ON");
            Rectangle offR = sliderRects.get("CRT_OFF");
            if (onR != null && onR.contains(p)) {
                CRTSettings.setEnabled(true);
                repaint();
                return;
            }
            if (offR != null && offR.contains(p)) {
                CRTSettings.setEnabled(false);
                repaint();
                return;
            }
            if (crtSliderRect != null && crtSliderRect.contains(p)) {
                draggingSlider = "CRT";
                updateCRTFromMouse(p.x);
            }
        }

        if (pauseTab == PauseTab.SOUND) {
            for (Map.Entry<String, Rectangle> entry : sliderRects.entrySet()) {
                String key = entry.getKey();
                Rectangle r = entry.getValue();
                if (key.startsWith("CRT") || !r.contains(p))
                    continue;
                draggingSlider = key;
                updateVolumeFromMouse(key, r, p.x);
                break;
            }
        }
    }

    @Override
    public void mouseDragged(MouseEvent e) {
        if (!showPauseMenu || draggingSlider == null)
            return;
        java.awt.Point p = e.getPoint();
        if ("CRT".equals(draggingSlider) && crtSliderRect != null)
            updateCRTFromMouse(p.x);
        else {
            Rectangle r = sliderRects.get(draggingSlider);
            if (r != null)
                updateVolumeFromMouse(draggingSlider, r, p.x);
        }
    }

    @Override
    public void mouseReleased(MouseEvent e) {
        draggingSlider = null;
    }

    @Override
    public void mouseClicked(MouseEvent e) {
    }

    @Override
    public void mouseEntered(MouseEvent e) {
    }

    @Override
    public void mouseExited(MouseEvent e) {
    }

    @Override
    public void mouseMoved(MouseEvent e) {
    }

    private void updateCRTFromMouse(int mouseX) {
        if (crtSliderRect == null)
            return;
        CRTSettings.setIntensity((int) (100.0 * (mouseX - crtSliderRect.x) / crtSliderRect.width));
        repaint();
    }

    private void updateVolumeFromMouse(String sf, Rectangle r, int mouseX) {
        SoundSettings.setVolume(sf, (int) (100.0 * (mouseX - r.x) / r.width));
        repaint();
    }

    private static int s(int v, double scale) {
        return (int) Math.round(v * scale);
    }

    // Stop Loop and Clean Up
    public void stopGame() {
        active = false;
        SoundManager.stopSound(SoundManager.PONG_LOSE);
        if (loop != null)
            loop.interrupt();
    }
}