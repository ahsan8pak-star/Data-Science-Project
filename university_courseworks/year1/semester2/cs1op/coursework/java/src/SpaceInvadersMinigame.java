// SpaceInvadersMinigame Class
// 3 Enemy Types with 2-Frame Animations, Difficulty-Based Speed & Shooting
// ESC Behaviour:
// - ESC during active game -> opens pause menu overlay
// - Pause menu has two tabs: CRT / DISPLAY and SOUND VOLUMES
// - CRT tab: On/Off toggle + 0-100 intensity slider
// - Sound tab: Per-sound volume sliders for SI sounds + general sounds
// - ESC again while paused -> resumes game
// Sound fix: per-frame throttle flags prevent same enemy-type shoot sound
// Firing multiple times in one update. endSoundPlayed guards end-game sounds.
// No sound calls inside paintComponent.

import java.awt.*;
import java.awt.event.*;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.Iterator;
import java.util.List;
import java.util.Map;
import java.util.Random;
import javax.swing.JPanel;

public class SpaceInvadersMinigame extends JPanel implements KeyListener, MouseListener, MouseMotionListener {

    // Logical Dimensions
    private static final int GW = 800, GH = 600;
    private static final int PW = 34, PH = 26;
    private static final int ES = 32;
    private static final int PBW = 4, PBH = 14;
    private static final int EBW = 5, EBH = 10;
    private static final int PLAYER_SPEED = 8;
    private static final int P_BULLET_SPEED = 13;
    private static final int E_BULLET_SPEED = 5;
    private static final long SHOOT_COOLDOWN = 180;

    private enum EType {
        UFO, SPACECRAFT, ALIEN
    }

    private static class Enemy {
        float x, y;
        EType type;

        Enemy(float x, float y, EType t) {
            this.x = x;
            this.y = y;
            this.type = t;
        }
    }

    private static class PBullet {
        float x, y;

        PBullet(float x, float y) {
            this.x = x;
            this.y = y;
        }
    }

    private static class EBullet {
        float x, y;

        EBullet(float x, float y) {
            this.x = x;
            this.y = y;
        }
    }

    // Game State
    private int playerX = GW / 2 - PW / 2;
    private final int playerY = GH - 60;
    private List<Enemy> enemies = new ArrayList<>();
    private List<PBullet> pBullets = new ArrayList<>();
    private List<EBullet> eBullets = new ArrayList<>();
    private float enemyDir = 1;
    private float currentSpeed = 1.0f;
    private float currentShootChance = 0.0f;

    private int animTick = 0, animFrame = 0;
    private static final int ANIM_TICKS = 22;

    private int currentWave = 1, totalWaves = 5;
    private int miniLives = 3;
    private String hitMsg = "";
    private int hitTimer = 0;

    private boolean gameActive = true;
    private boolean gameEnded = false;
    private boolean playerWon = false;
    private boolean endSoundPlayed = false;
    private boolean gamePaused = false;
    private boolean showMsg = true;
    private String msgText = "";
    private String endMsg = "";

    // Input flags - set only in keyPressed/keyReleased
    private boolean moveLeft = false, moveRight = false, doShoot = false;
    private long lastShootMs = 0;

    // Per-frame shoot throttle flags
    private boolean ufoShootThisFrame = false;
    private boolean spacecraftShootThisFrame = false;
    private boolean alienShootThisFrame = false;

    // Loop sound presence tracking
    private boolean ufoRowPresent = false;
    private boolean alienRowPresent = false;

    private Thread gameThread;
    private final Random rng = new Random();
    private GameController controller;
    private int playerExp = 0;

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

    // Constructors
    public SpaceInvadersMinigame(GameController controller) {
        this.controller = controller;
        if (controller != null && controller.getCurrentPlayer() != null)
            playerExp = controller.getCurrentPlayer().getExp();
        setWavesFromExp();
        msgText = "Press ENTER to start Wave 1 / " + totalWaves;
        setBackground(Color.BLACK);
        setFocusable(true);
        addKeyListener(this);
        addMouseListener(this);
        addMouseMotionListener(this);
    }

    public SpaceInvadersMinigame() {
        this(null);
    }

    // Difficulty
    private void setWavesFromExp() {
        if (playerExp <= 200)
            totalWaves = 5;
        else if (playerExp <= 350)
            totalWaves = 10;
        else
            totalWaves = 15;
    }

    private float calcSpeed(int wave) {
        int p = (wave - 1) % 5;
        return switch (GameSettings.getDifficulty()) {
            case EASY -> 0.0f + p * 0.4f;
            case NORMAL -> 1.0f + p * 0.5f;
            case HARD -> 2.0f + p * 0.5f;
        };
    }

    private float calcShootChance(int wave) {
        int p = (wave - 1) % 5;
        return switch (GameSettings.getDifficulty()) {
            case EASY -> 0.0f;
            case NORMAL -> 0.0008f + p * 0.00016f;
            case HARD -> 0.002f + p * 0.0004f;
        };
    }

    // Wave Management
    private void spawnWave() {
        enemies.clear();
        eBullets.clear();
        pBullets.clear();
        animTick = 0;
        animFrame = 0;
        currentSpeed = calcSpeed(currentWave);
        currentShootChance = calcShootChance(currentWave);
        enemyDir = 1;
        int cols = 8, spacing = GW / (cols + 1);
        spawnRow(EType.UFO, cols, spacing, 0);
        if (currentWave >= 6)
            spawnRow(EType.SPACECRAFT, cols, spacing, 1);
        if (currentWave >= 11)
            spawnRow(EType.ALIEN, cols, spacing, 2);
        updateLoopSounds();
    }

    private void spawnRow(EType type, int cols, int spacing, int rowIdx) {
        for (int c = 0; c < cols; c++)
            enemies.add(new Enemy((c + 1) * spacing - ES / 2f, 45 + rowIdx * 54, type));
    }

    private void updateLoopSounds() {
        boolean hasUFO = false, hasAlien = false;
        for (Enemy e : enemies) {
            switch (e.type) {
                case UFO -> hasUFO = true;
                case SPACECRAFT -> {
                } // Spacecraft Has No Loop Sound - No Action Needed
                case ALIEN -> hasAlien = true;
            }
        }
        if (hasUFO && !ufoRowPresent)
            SoundManager.playLoop(SoundManager.SI_UFO_FLY);
        else if (!hasUFO && ufoRowPresent)
            SoundManager.stopSound(SoundManager.SI_UFO_FLY);

        if (hasAlien && !alienRowPresent)
            SoundManager.playLoop(SoundManager.SI_ALIEN_SHOOT);
        else if (!hasAlien && alienRowPresent)
            SoundManager.stopSound(SoundManager.SI_ALIEN_SHOOT);

        ufoRowPresent = hasUFO;
        // spacecraftRow removed - unused
        alienRowPresent = hasAlien;
    }

    // Game Loop
    private void startGameLoop() {
        spawnWave();
        showMsg = false;
        gameThread = new Thread(() -> {
            while (gameActive) {
                if (!gamePaused && !gameEnded && !showMsg && !showPauseMenu)
                    update();
                repaint();
                try {
                    Thread.sleep(16);
                } catch (InterruptedException ex) {
                    break;
                }
            }
        }, "si-loop");
        gameThread.setDaemon(true);
        gameThread.start();
    }

    // Update
    private void update() {
        ufoShootThisFrame = false;
        spacecraftShootThisFrame = false;
        alienShootThisFrame = false;

        animTick++;
        if (animTick >= ANIM_TICKS) {
            animTick = 0;
            animFrame = 1 - animFrame;
        }

        if (moveLeft && playerX > 0)
            playerX -= PLAYER_SPEED;
        if (moveRight && playerX < GW - PW)
            playerX += PLAYER_SPEED;

        long now = System.currentTimeMillis();
        if (doShoot && now - lastShootMs > SHOOT_COOLDOWN) {
            pBullets.add(new PBullet(playerX + PW / 2f - PBW / 2f, playerY - PBH));
            lastShootMs = now;
            SoundManager.playOnce(SoundManager.SI_PLAYER_SHOOT);
        }

        for (Iterator<PBullet> it = pBullets.iterator(); it.hasNext();) {
            PBullet b = it.next();
            b.y -= P_BULLET_SPEED;
            if (b.y < 0)
                it.remove();
        }

        boolean goDown = false;
        for (Enemy e : enemies) {
            e.x += currentSpeed * enemyDir;
            if (e.x <= 0 || e.x + ES >= GW)
                goDown = true;
        }
        if (goDown) {
            enemyDir = -enemyDir;
            for (Enemy e : enemies) {
                e.y += 18;
                e.x += currentSpeed * enemyDir;
                if (e.y + ES >= playerY) {
                    triggerGameOver();
                    return;
                }
            }
        }

        if (currentShootChance > 0 && !enemies.isEmpty()) {
            for (Enemy e : enemies) {
                if (rng.nextFloat() < currentShootChance) {
                    eBullets.add(new EBullet(e.x + ES / 2f - EBW / 2f, e.y + ES));
                    switch (e.type) {
                        case UFO -> {
                            if (!ufoShootThisFrame) {
                                SoundManager.playOnce(SoundManager.SI_UFO_SHOOT);
                                ufoShootThisFrame = true;
                            }
                        }
                        case SPACECRAFT -> {
                            if (!spacecraftShootThisFrame) {
                                SoundManager.playOnce(SoundManager.SI_SPACECRAFT_SHOOT);
                                spacecraftShootThisFrame = true;
                            }
                        }
                        case ALIEN -> {
                            if (!alienShootThisFrame) {
                                SoundManager.playOnce(SoundManager.SI_ALIEN_SHOOT);
                                alienShootThisFrame = true;
                            }
                        }
                    }
                }
            }
        }

        for (Iterator<EBullet> it = eBullets.iterator(); it.hasNext();) {
            EBullet b = it.next();
            b.y += E_BULLET_SPEED;
            if (b.y > GH) {
                it.remove();
                continue;
            }
            if (b.x < playerX + PW && b.x + EBW > playerX && b.y < playerY + PH && b.y + EBH > playerY) {
                it.remove();
                onPlayerHit();
                return;
            }
        }

        outer: for (Iterator<PBullet> bIt = pBullets.iterator(); bIt.hasNext();) {
            PBullet b = bIt.next();
            for (Iterator<Enemy> eIt = enemies.iterator(); eIt.hasNext();) {
                Enemy e = eIt.next();
                if (b.x < e.x + ES && b.x + PBW > e.x && b.y < e.y + ES && b.y + PBH > e.y) {
                    bIt.remove();
                    switch (e.type) {
                        case UFO -> SoundManager.playOnce(SoundManager.SI_UFO_DIE);
                        case SPACECRAFT -> SoundManager.playOnce(SoundManager.SI_SPACECRAFT_DIE);
                        case ALIEN -> SoundManager.playOnce(SoundManager.SI_ALIEN_DIE);
                    }
                    eIt.remove();
                    updateLoopSounds();
                    continue outer;
                }
            }
        }

        if (enemies.isEmpty()) {
            stopAllEnemyLoops();
            if (currentWave >= totalWaves) {
                if (!endSoundPlayed) {
                    endSoundPlayed = true;
                    gameEnded = true;
                    playerWon = true;
                    endMsg = "MISSION COMPLETE!";
                    SoundManager.playOnce(SoundManager.SI_WIN);
                }
            } else {
                SoundManager.playOnce(SoundManager.SI_NEXT_WAVE);
                currentWave++;
                showMsg = true;
                msgText = "Wave " + (currentWave - 1) + " cleared!\nPress ENTER for Wave "
                        + currentWave + " / " + totalWaves
                        + "   Speed: " + String.format("%.1f", calcSpeed(currentWave));
            }
        }
        if (hitTimer > 0)
            hitTimer--;
    }

    private void onPlayerHit() {
        miniLives--;
        SoundManager.playOnce(SoundManager.SI_MINI_LIFE_LOST);
        if (miniLives <= 0) {
            stopAllEnemyLoops();
            if (!endSoundPlayed) {
                endSoundPlayed = true;
                gameEnded = true;
                playerWon = false;
                endMsg = "OUT OF MINIGAME LIVES!";
                SoundManager.playLoop(SoundManager.SI_LOSE);
            }
        } else {
            hitMsg = "HIT \u2013 " + miniLives + " minigame life" + (miniLives == 1 ? "" : "s") + " remaining";
            hitTimer = 160;
            eBullets.clear();
            pBullets.clear();
            spawnWave();
        }
    }

    private void triggerGameOver() {
        stopAllEnemyLoops();
        if (!endSoundPlayed) {
            endSoundPlayed = true;
            gameEnded = true;
            playerWon = false;
            endMsg = "WAVE " + currentWave + " FAILED";
            SoundManager.playLoop(SoundManager.SI_LOSE);
        }
    }

    private void stopAllEnemyLoops() {
        SoundManager.stopSound(SoundManager.SI_UFO_FLY);
        SoundManager.stopSound(SoundManager.SI_ALIEN_SHOOT);
        ufoRowPresent = false;
        alienRowPresent = false;
    }

    // Rendering
    @Override
    protected void paintComponent(Graphics g) {
        super.paintComponent(g);
        Graphics2D g2d = (Graphics2D) g;
        g2d.setRenderingHint(RenderingHints.KEY_ANTIALIASING, RenderingHints.VALUE_ANTIALIAS_ON);

        int pw = getWidth(), ph = getHeight();
        double sx = pw / (double) GW, sy = ph / (double) GH;

        if (showMsg && !gameEnded) {
            g2d.setColor(new Color(0, 255, 0));
            g2d.setFont(new Font("Monospaced", Font.BOLD, (int) (22 * Math.min(sx, sy))));
            String[] ls = msgText.split("\n");
            int lh = (int) (32 * Math.min(sx, sy));
            int ty = ph / 2 - ls.length * lh / 2;
            for (String ln : ls) {
                FontMetrics fm = g2d.getFontMetrics();
                g2d.drawString(ln, (pw - fm.stringWidth(ln)) / 2, ty);
                ty += lh;
            }
            CRTSettings.drawCRT(g2d, pw, ph);
            return;
        }

        // Player ship
        g2d.setColor(new Color(0, 255, 0));
        int px = sc(playerX, sx), py = sc(playerY, sy), psw = sc(PW, sx), psh = sc(PH, sy);
        g2d.fillPolygon(new int[] { px + psw / 2, px, px + psw }, new int[] { py, py + psh, py + psh }, 3);

        for (Enemy e : enemies)
            drawEnemy(g2d, e, sc(e.x, sx), sc(e.y, sy), sc(ES, sx), sc(ES, sy), animFrame);

        g2d.setColor(Color.YELLOW);
        for (PBullet b : pBullets)
            g2d.fillRect(sc(b.x, sx), sc(b.y, sy), sc(PBW, sx), sc(PBH, sy));

        g2d.setColor(new Color(255, 80, 80));
        for (EBullet b : eBullets)
            g2d.fillRect(sc(b.x, sx), sc(b.y, sy), sc(EBW, sx), sc(EBH, sy));

        // HUD
        g2d.setColor(new Color(0, 255, 0));
        g2d.setFont(new Font("Monospaced", Font.BOLD, (int) (14 * Math.min(sx, sy))));
        g2d.drawString(
                "WAVE: " + currentWave + "/" + totalWaves + "   Speed: " + String.format("%.1f", currentSpeed)
                        + "   Mini-lives: " + miniLives + "   [" + GameSettings.difficultyLabel() + "]",
                sc(10, sx), sc(24, sy));

        int bw = sc(200, sx), bh2 = sc(9, sy), bx2 = sc(10, sx), barY = sc(30, sy);
        g2d.setColor(new Color(40, 40, 40));
        g2d.fillRect(bx2, barY, bw, bh2);
        g2d.setColor(new Color(0, 200, 0));
        g2d.fillRect(bx2, barY, (currentWave - 1) * bw / totalWaves, bh2);

        if (hitTimer > 0) {
            g2d.setColor(new Color(255, 220, 0));
            g2d.setFont(new Font("Monospaced", Font.BOLD, (int) (17 * Math.min(sx, sy))));
            FontMetrics hfm = g2d.getFontMetrics();
            g2d.drawString(hitMsg, (pw - hfm.stringWidth(hitMsg)) / 2, ph / 2 - sc(55, sy));
        }

        g2d.setColor(new Color(0, 120, 0));
        g2d.setFont(new Font("Monospaced", Font.PLAIN, (int) (11 * Math.min(sx, sy))));
        g2d.drawString("LEFT/RIGHT: Move   SPACE: Shoot   P: Pause   ESC: Menu", sc(10, sx), ph - sc(8, sy));

        // CRT overlay before any popup
        CRTSettings.drawCRT(g2d, pw, ph);

        // Game-Over overlay
        if (gameEnded) {
            g2d.setColor(new Color(0, 0, 0, 185));
            g2d.fillRect(0, 0, pw, ph);
            g2d.setColor(playerWon ? new Color(0, 255, 0) : new Color(255, 0, 0));
            g2d.setFont(new Font("Monospaced", Font.BOLD, (int) (36 * Math.min(sx, sy))));
            FontMetrics fm = g2d.getFontMetrics();
            g2d.drawString(endMsg, (pw - fm.stringWidth(endMsg)) / 2, ph / 2);
            g2d.setColor(new Color(0, 255, 0));
            g2d.setFont(new Font("Monospaced", Font.PLAIN, (int) (18 * Math.min(sx, sy))));
            String sub = "Press ENTER to continue";
            fm = g2d.getFontMetrics();
            g2d.drawString(sub, (pw - fm.stringWidth(sub)) / 2, ph / 2 + sc(55, sy));
            return;
        }

        // Pause menu overlay
        if (showPauseMenu)
            drawPauseMenu(g2d, pw, ph);
    }

    // Pause Menu (identical structure to Pong, SI-specific sounds shown)
    private void drawPauseMenu(Graphics2D g2d, int pw, int ph) {
        g2d.setColor(new Color(0, 0, 0, 210));
        g2d.fillRect(0, 0, pw, ph);

        int boxW = Math.min(620, pw - 60), boxH = ph - 80;
        int boxX = (pw - boxW) / 2, boxY = 40;

        g2d.setColor(new Color(0, 255, 0));
        g2d.setStroke(new BasicStroke(3));
        g2d.drawRect(boxX, boxY, boxW, boxH);
        g2d.setStroke(new BasicStroke(1));

        g2d.setFont(new Font("Monospaced", Font.BOLD, 28));
        FontMetrics fm = g2d.getFontMetrics();
        String title = "PAUSED";
        g2d.drawString(title, boxX + (boxW - fm.stringWidth(title)) / 2, boxY + 38);

        int tabY = boxY + 56, tabW = boxW / 2 - 20, tabH = 30;
        mainTabRect = new Rectangle(boxX + 10, tabY, tabW, tabH);
        soundTabRect = new Rectangle(boxX + boxW / 2 + 10, tabY, tabW, tabH);
        drawTabBtn(g2d, "CRT / DISPLAY", mainTabRect, pauseTab == PauseTab.MAIN);
        drawTabBtn(g2d, "SOUND VOLUMES", soundTabRect, pauseTab == PauseTab.SOUND);

        int contentY = tabY + tabH + 16;
        int contentH = boxH - (contentY - boxY) - 60;

        if (pauseTab == PauseTab.MAIN)
            drawCRTPanel(g2d, boxX + 10, contentY, boxW - 20, contentH);
        else
            drawSoundPanel(g2d, boxX + 10, contentY, boxW - 20, contentH);

        int btnY = boxY + boxH - 48, btnW = boxW / 2 - 20;
        resumeRect = new Rectangle(boxX + 10, btnY, btnW, 36);
        quitRect = new Rectangle(boxX + boxW / 2 + 10, btnY, btnW, 36);
        drawMenuBtn(g2d, "RESUME", resumeRect, new Color(0, 200, 0));
        drawMenuBtn(g2d, "QUIT", quitRect, new Color(180, 0, 0));
    }

    private void drawTabBtn(Graphics2D g, String label, Rectangle r, boolean active) {
        g.setColor(active ? new Color(0, 200, 0) : new Color(0, 60, 0));
        g.fillRect(r.x, r.y, r.width, r.height);
        g.setColor(new Color(0, 255, 0));
        g.setStroke(new BasicStroke(1));
        g.drawRect(r.x, r.y, r.width, r.height);
        g.setFont(new Font("Monospaced", Font.BOLD, 13));
        FontMetrics fm = g.getFontMetrics();
        g.setColor(active ? Color.BLACK : new Color(0, 200, 0));
        g.drawString(label, r.x + (r.width - fm.stringWidth(label)) / 2, r.y + r.height / 2 + fm.getAscent() / 2 - 2);
    }

    private void drawMenuBtn(Graphics2D g, String label, Rectangle r, Color col) {
        g.setColor(col);
        g.fillRect(r.x, r.y, r.width, r.height);
        g.setColor(new Color(0, 255, 0));
        g.setStroke(new BasicStroke(2));
        g.drawRect(r.x, r.y, r.width, r.height);
        g.setFont(new Font("Monospaced", Font.BOLD, 16));
        FontMetrics fm = g.getFontMetrics();
        g.setColor(Color.WHITE);
        g.drawString(label, r.x + (r.width - fm.stringWidth(label)) / 2, r.y + r.height / 2 + fm.getAscent() / 2 - 2);
    }

    private void drawCRTPanel(Graphics2D g2d, int x, int y, int w, int h) {
        sliderRects.clear();
        int cy = y + 14;

        g2d.setFont(new Font("Monospaced", Font.BOLD, 15));
        g2d.setColor(new Color(0, 255, 0));
        g2d.drawString("CRT Effect:", x, cy + 14);

        int togX = x + 130;
        Rectangle onR = new Rectangle(togX, cy, 56, 26);
        Rectangle offR = new Rectangle(togX + 64, cy, 56, 26);

        g2d.setColor(CRTSettings.isEnabled() ? new Color(0, 200, 0) : new Color(0, 50, 0));
        g2d.fillRect(onR.x, onR.y, onR.width, onR.height);
        g2d.setColor(new Color(0, 255, 0));
        g2d.drawRect(onR.x, onR.y, onR.width, onR.height);
        g2d.setFont(new Font("Monospaced", Font.BOLD, 12));
        g2d.setColor(CRTSettings.isEnabled() ? Color.BLACK : new Color(0, 200, 0));
        g2d.drawString("ON", onR.x + 14, onR.y + 17);

        g2d.setColor(!CRTSettings.isEnabled() ? new Color(150, 0, 0) : new Color(30, 0, 0));
        g2d.fillRect(offR.x, offR.y, offR.width, offR.height);
        g2d.setColor(new Color(0, 255, 0));
        g2d.drawRect(offR.x, offR.y, offR.width, offR.height);
        g2d.setColor(!CRTSettings.isEnabled() ? Color.WHITE : new Color(180, 0, 0));
        g2d.drawString("OFF", offR.x + 8, offR.y + 17);

        sliderRects.put("CRT_ON", onR);
        sliderRects.put("CRT_OFF", offR);
        cy += 44;

        g2d.setFont(new Font("Monospaced", Font.BOLD, 15));
        g2d.setColor(CRTSettings.isEnabled() ? new Color(0, 255, 0) : new Color(0, 80, 0));
        g2d.drawString("Intensity:", x, cy + 14);

        int sX = x + 130, sW = w - 170;
        crtSliderRect = new Rectangle(sX, cy, sW, 16);
        float fill = CRTSettings.getIntensity() / 100.0f;

        g2d.setColor(new Color(0, 40, 0));
        g2d.fillRect(sX, cy, sW, 16);
        g2d.setColor(CRTSettings.isEnabled() ? new Color(0, 200, 0) : new Color(0, 60, 0));
        g2d.fillRect(sX, cy, (int) (sW * fill), 16);
        g2d.setColor(new Color(0, 255, 0));
        g2d.drawRect(sX, cy, sW, 16);

        int thumbX = sX + (int) (sW * fill) - 4;
        g2d.fillRect(thumbX, cy - 3, 8, 22);
        g2d.setFont(new Font("Monospaced", Font.BOLD, 13));
        g2d.drawString(CRTSettings.getIntensity() + "%", sX + sW + 8, cy + 13);
        cy += 36;

        g2d.setFont(new Font("Monospaced", Font.PLAIN, 12));
        g2d.setColor(new Color(0, 160, 0));
        g2d.drawString("0-33: Scanlines only   34-66: + Vignette   67-100: + Flicker", x, cy + 14);
        cy += 30;
        g2d.setFont(new Font("Monospaced", Font.PLAIN, 11));
        g2d.setColor(new Color(0, 120, 0));
        g2d.drawString("Reference: perchance.org/text-adventure-template", x, cy + 12);
    }

    private void drawSoundPanel(Graphics2D g2d, int x, int y, int w, int h) {
        String[] siSounds = SoundSettings.getSoundFilesForCategory("Invaders");
        String[] generalSounds = SoundSettings.getGeneralSoundFiles();

        int cy = y, labelW = 200, sX = x + labelW, sW = w - labelW - 60, rowH = 26;
        Font lf = new Font("Monospaced", Font.BOLD, 12);
        Font vf = new Font("Monospaced", Font.PLAIN, 11);

        g2d.setFont(new Font("Monospaced", Font.BOLD, 13));
        g2d.setColor(new Color(0, 200, 0));
        g2d.drawString("SPACE INVADERS SOUNDS", x, cy + 13);
        cy += 20;

        for (String sf : siSounds) {
            drawSoundRow(g2d, sf, x, cy, labelW, sX, sW, rowH, lf, vf);
            cy += rowH;
        }

        cy += 8;
        g2d.setFont(new Font("Monospaced", Font.BOLD, 13));
        g2d.setColor(new Color(0, 200, 0));
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

    private void drawSoundRow(Graphics2D g2d, String sf, int x, int cy,
            int labelW, int sX, int sW, int rowH, Font lf, Font vf) {
        String name = SoundSettings.getDisplayName(sf);
        int vol = SoundSettings.getVolume(sf);
        g2d.setFont(lf);
        g2d.setColor(new Color(0, 220, 0));
        String shortName = name.length() > 22 ? name.substring(0, 21) + "." : name;
        g2d.drawString(shortName, x, cy + rowH - 8);

        Rectangle r = new Rectangle(sX, cy + 4, sW, rowH - 10);
        sliderRects.put(sf, r);
        g2d.setColor(new Color(0, 40, 0));
        g2d.fillRect(r.x, r.y, r.width, r.height);
        g2d.setColor(new Color(0, 180, 0));
        g2d.fillRect(r.x, r.y, (int) (r.width * vol / 100.0), r.height);
        g2d.setColor(new Color(0, 255, 0));
        g2d.drawRect(r.x, r.y, r.width, r.height);
        int tx = r.x + (int) (r.width * vol / 100.0) - 3;
        g2d.fillRect(tx, r.y - 2, 6, r.height + 4);
        g2d.setFont(vf);
        g2d.setColor(new Color(0, 200, 0));
        g2d.drawString(vol + "%", r.x + r.width + 6, cy + rowH - 7);
    }

    // Enemy Drawing
    private void drawEnemy(Graphics2D g, Enemy e, int ex, int ey, int ew, int eh, int frame) {
        switch (e.type) {
            case UFO -> drawUFO(g, ex, ey, ew, eh, frame);
            case SPACECRAFT -> drawSpacecraft(g, ex, ey, ew, eh, frame);
            case ALIEN -> drawAlien(g, ex, ey, ew, eh, frame);
        }
    }

    private void drawUFO(Graphics2D g, int ex, int ey, int ew, int eh, int frame) {
        Color body = new Color(0, 255, 0);
        int u = Math.max(1, ew / 12);
        g.setColor(body);
        g.fillOval(ex + ew * 3 / 8, ey, ew / 4, eh / 4);
        g.fillOval(ex + u, ey + eh / 6, ew - 2 * u, eh * 2 / 5);
        g.fillRect(ex, ey + eh * 2 / 5, ew, eh / 3);
        int lr = u + 1, ly = ey + eh * 2 / 5 + u, nl = 5;
        for (int i = 0; i < nl; i++) {
            int lx = ex + u + i * (ew - 2 * u) / (nl - 1) - lr;
            g.setColor((i % 2 == frame) ? Color.WHITE : body);
            g.fillOval(lx, ly, lr * 2, lr * 2);
        }
        g.setColor(body);
        g.fillRect(ex + ew / 6, ey + eh * 2 / 3, ew * 2 / 3, u);
    }

    private void drawSpacecraft(Graphics2D g, int ex, int ey, int ew, int eh, int frame) {
        Color body = new Color(0, 0, 255);
        int u = Math.max(1, ew / 10), fw = ew * 2 / 5, fx = ex + (ew - fw) / 2;
        g.setColor(body);
        g.fillRect(fx, ey, fw, eh * 3 / 4);
        g.fillRect(fx + fw / 4, ey - u * 2, fw / 2, u * 2);
        g.fillRect(ex, ey + eh / 2, ew, eh / 5);
        g.fillRect(fx + fw / 4, ey + eh * 3 / 4, fw / 2, u * 2);
        g.setColor(frame == 0 ? Color.BLACK : Color.WHITE);
        g.fillRect(fx + fw / 4, ey + eh / 5, fw / 2, eh / 7);
        g.fillRect(fx + fw / 4, ey + eh / 5 + eh / 7 + u, fw / 2, eh / 7);
    }

    private void drawAlien(Graphics2D g, int ex, int ey, int ew, int eh, int frame) {
        Color body = new Color(255, 0, 0);
        int u = Math.max(1, ew / 11);
        g.setColor(body);
        if (frame == 0) {
            g.fillRect(ex + 2 * u, ey, u, 2 * u);
            g.fillRect(ex + 8 * u, ey, u, 2 * u);
        } else {
            g.fillRect(ex + u, ey, u, 2 * u);
            g.fillRect(ex + 9 * u, ey, u, 2 * u);
        }
        g.fillRect(ex + 2 * u, ey + 2 * u, 7 * u, 3 * u);
        g.setColor(Color.WHITE);
        g.fillRect(ex + 3 * u, ey + 2 * u + u / 2, 2 * u, 2 * u);
        g.fillRect(ex + 6 * u, ey + 2 * u + u / 2, 2 * u, 2 * u);
        g.setColor(body);
        g.fillRect(ex, ey + 5 * u, 11 * u, 3 * u);
        g.fillRect(ex + 3 * u, ey + 8 * u, 5 * u, 2 * u);
        g.fillRect(ex, ey + 5 * u, 2 * u, 2 * u);
        g.fillRect(ex + 9 * u, ey + 5 * u, 2 * u, 2 * u);
        if (frame == 0) {
            g.fillRect(ex + 2 * u, ey + 10 * u, 2 * u, 2 * u);
            g.fillRect(ex + 7 * u, ey + 10 * u, 2 * u, 2 * u);
        } else {
            g.fillRect(ex, ey + 10 * u, 2 * u, 2 * u);
            g.fillRect(ex + 9 * u, ey + 10 * u, 2 * u, 2 * u);
        }
    }

    private static int sc(float v, double s) {
        return (int) Math.round(v * s);
    }

    private static int sc(int v, double s) {
        return (int) Math.round(v * s);
    }

    // Key Handling
    @Override
    public void keyPressed(KeyEvent e) {
        if (gameEnded) {
            if (e.getKeyCode() == KeyEvent.VK_ENTER && controller != null) {
                SoundManager.stopSound(SoundManager.SI_LOSE);
                SoundManager.stopAll();
                if (playerWon)
                    controller.onMinigameWon("SPACE_INVADERS", 100);
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
        if (showMsg) {
            if (e.getKeyCode() == KeyEvent.VK_ENTER) {
                if (gameThread == null || !gameThread.isAlive())
                    startGameLoop();
                else {
                    showMsg = false;
                    spawnWave();
                }
            }
            return;
        }
        switch (e.getKeyCode()) {
            case KeyEvent.VK_LEFT -> moveLeft = true;
            case KeyEvent.VK_RIGHT -> moveRight = true;
            case KeyEvent.VK_SPACE -> doShoot = true;
            case KeyEvent.VK_P -> gamePaused = !gamePaused;
            case KeyEvent.VK_ESCAPE -> {
                showPauseMenu = true;
                pauseTab = PauseTab.MAIN;
                repaint();
            }
        }
    }

    @Override
    public void keyReleased(KeyEvent e) {
        switch (e.getKeyCode()) {
            case KeyEvent.VK_LEFT -> moveLeft = false;
            case KeyEvent.VK_RIGHT -> moveRight = false;
            case KeyEvent.VK_SPACE -> doShoot = false;
        }
    }

    @Override
    public void keyTyped(KeyEvent e) {
    }

    // Mouse Handling
    @Override
    public void mousePressed(MouseEvent e) {
        if (!showPauseMenu)
            return;
        Point p = e.getPoint();

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
            gameActive = false;
            stopAllEnemyLoops();
            SoundManager.stopSound(SoundManager.SI_LOSE);
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
        Point p = e.getPoint();
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

    public void stopGame() {
        gameActive = false;
        stopAllEnemyLoops();
        SoundManager.stopSound(SoundManager.SI_LOSE);
        if (gameThread != null)
            gameThread.interrupt();
    }
}