// Main Entry Point for Space Mission Game

import javax.swing.SwingUtilities;

public class Main {
    public static void main(String[] args) {

        // Global Exception Handler to Prevent Crashes
        Thread.setDefaultUncaughtExceptionHandler((thread, error) -> {
            System.err.println("Error: " + error.getMessage());
            error.printStackTrace();
            System.exit(1);
        });

        // Launches GUI Game Version
        // Uses SwingUtilities to Ensure GUI Works Correctly to Avoid Potential
        // Threading Issues
        SwingUtilities.invokeLater(() -> new GameGUI());
    }
}