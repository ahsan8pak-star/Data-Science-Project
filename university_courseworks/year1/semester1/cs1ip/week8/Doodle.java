import javax.swing.*;        
import java.awt.*;

// Your task:
//
// Create a greetings card using Java graphics.
// Use top-down design to split the problem of drawing the card into sub-problems that you can implement.
// Be creative!
//
// You can find a list of drawing functions available through the Java API here:
// https://docs.oracle.com/javase/8/docs/api/java/awt/Graphics.html
//
// Because this is a graphical program, the setup requires some more advanced Java features.
// You'll find out about them next semester, in Object Oriented Programming.
// For now, trust that the code at the bottom of the file works and don't edit it.

class DoodlePanel extends JPanel {

    @Override
    protected void paintComponent(Graphics g) {
        super.paintComponent(g);

        // YOUR CODE GOES HERE:

        // Set drawing color
        g.setColor(Color.BLUE);
        // Draw the circle
        // g.drawOval(x, y, width, height)
        // x and y are the coordinates of the top-left corner of the bounding box
        g.drawOval(50, 50, 100, 100); 

        // To draw a filled circle
        g.setColor(Color.RED);
        g.fillOval(200, 50, 150, 150);

    }

}

///////////////////////////////////////////////////////////////////////////////
// You can ignore everything below here.
// It just sets up a window pained using the code above.
///////////////////////////////////////////////////////////////////////////////

// Adapted from:
// https://docs.oracle.com/javase/tutorial/uiswing/examples/start/HelloWorldSwingProject/src/start/HelloWorldSwing.java

public class Doodle {

    // Create the GUI and show it.
    // For thread safety, this method should be invoked from the event-dispatching thread.
    private static void createAndShowGUI() {
        // Create and set up the window.
        JFrame frame = new JFrame("HelloWorldSwing");
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);

        // Add the drawing panel.
        JPanel panel = new DoodlePanel();
        frame.getContentPane().add(panel);
        // Set the size of the drawing panel.
        panel.setPreferredSize(new Dimension(640, 480));

        //Display the window.
        frame.pack();
        frame.setVisible(true);
    }

    public static void main(String[] args) {
        // Schedule a job for the event-dispatching thread:
        // creating and showing this application's GUI.
        javax.swing.SwingUtilities.invokeLater(new Runnable() {
            public void run() {
                createAndShowGUI();
            }
        });
    }

}
