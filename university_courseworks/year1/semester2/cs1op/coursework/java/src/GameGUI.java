// GameGUI Class - Main Application Window Using CardLayout for Screen Management
// Registers All Core Screens at Startup Including CRT_SCREEN
// Stops All Sounds When Navigating to the Main Menu

import java.awt.CardLayout;
import java.awt.Color;
import java.awt.Dimension;
import javax.swing.JFrame;
import javax.swing.JOptionPane;
import javax.swing.JPanel;
import javax.swing.SwingUtilities;
import javax.swing.UIManager;
import java.util.HashMap;
import java.util.Map;

public class GameGUI extends JFrame {

    // Layout Manager for Switching Between Screens
    private final CardLayout cardLayout;

    // The Main Content Panel Holding All Screens
    private final JPanel mainPanel;

    // The Controller Connecting GUI to Game Logic
    private GameController gameController;

    // Map of Screen Name to Panel for Safe Management
    private final Map<String, JPanel> screenMap = new HashMap<>();

    // Constructor - Builds the Window and Registers Core Screens
    public GameGUI() {
        setTitle("Space Mission");
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        setMinimumSize(new Dimension(900, 650));
        setPreferredSize(new Dimension(1100, 750));
        setSize(1100, 750);
        setLocationRelativeTo(null);
        setResizable(true);

        gameController = new GameController(this);
        cardLayout = new CardLayout();
        mainPanel = new JPanel(cardLayout);
        mainPanel.setBackground(Color.BLACK);

        // Register All Core Screens
        addScreen(new MainMenuScreen(this, gameController), "MAIN_MENU");
        addScreen(new NameEntryScreen(this, gameController), "NAME_ENTRY");
        addScreen(new DialogueScreen(this, gameController), "DIALOGUE");
        addScreen(new GamePlayScreen(this, gameController), "GAMEPLAY");
        addScreen(new DoorSelectionScreen(this, gameController), "DOOR_SELECTION");

        add(mainPanel);

        // Request Permission to Run Before Showing the Window
        if (!showStartupPrompt()) {
            SoundManager.stopAll();
            dispose();
            System.exit(0);
            return;
        }

        setVisible(true);
        showScreen("MAIN_MENU");
    }

    // Show a Yes/No Permission Dialog Before Launching the Game
    private boolean showStartupPrompt() {
        try {
            UIManager.put("OptionPane.background", Color.BLACK);
            UIManager.put("Panel.background", Color.BLACK);
            UIManager.put("OptionPane.messageForeground", new Color(0, 255, 65));
        } catch (Exception ignored) {
            // UIManager Properties May Not Be Available on All Platforms
        }

        int result = JOptionPane.showConfirmDialog(
                this,
                "Allow Space Mission to run?",
                "Permission Request",
                JOptionPane.YES_NO_OPTION,
                JOptionPane.QUESTION_MESSAGE);

        return result == JOptionPane.YES_OPTION;
    }

    // Switch the Visible Screen by Name and Request Focus
    public void showScreen(String name) {
        if ("MAIN_MENU".equals(name)) {
            SoundManager.stopAll();
        }

        cardLayout.show(mainPanel, name);

        SwingUtilities.invokeLater(() -> {
            JPanel screen = screenMap.get(name);
            if (screen != null) {
                try {
                    screen.requestFocusInWindow();
                } catch (Exception ignored) {
                    // Focus Request May Fail if the Window Is Not Yet Visible
                }
            }
        });
    }

    // Add or Replace a Screen Registered Under the Given Name
    public void addScreen(JPanel screen, String name) {
        try {
            JPanel old = screenMap.get(name);
            if (old != null)
                mainPanel.remove(old);

            screen.setFocusable(true);
            mainPanel.add(screen, name);
            screenMap.put(name, screen);
            mainPanel.revalidate();
        } catch (Exception e) {
            // Silently Ignore Screen Addition Errors to Prevent Crashes
        }
    }

    // Remove a Screen by Its Registered Name
    public void removeScreen(String name) {
        try {
            JPanel screen = screenMap.remove(name);
            if (screen != null) {
                mainPanel.remove(screen);
                mainPanel.revalidate();
                mainPanel.repaint();
            }
        } catch (Exception e) {
            // Silently Ignore Screen Removal Errors
        }
    }

    // Application Entry Point
    public static void main(String[] args) {
        SwingUtilities.invokeLater(GameGUI::new);
    }
}