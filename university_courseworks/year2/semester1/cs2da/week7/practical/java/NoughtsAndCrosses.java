import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

/** One immutable vertex in the Noughts and Crosses game graph. */
public final class NoughtsAndCrosses {
    public enum Outcome {
        IN_PROGRESS, X_WINS, O_WINS, DRAW
    }

    private static final char EMPTY = ' ';

    // Square indices in row order. Each triple is a winning line.
    private static final int[][] WINNING_LINES = {
        {0, 1, 2}, {3, 4, 5}, {6, 7, 8}, // rows
        {0, 3, 6}, {1, 4, 7}, {2, 5, 8}, // columns
        {0, 4, 8}, {2, 4, 6}             // diagonals
    };

    private final char[] board;
    private final boolean xToMove;

    /** Start with an empty board and Crosses to move. */
    public NoughtsAndCrosses() {
        board = new char[9];
        Arrays.fill(board, EMPTY);
        xToMove = true;
    }

    // Each successor owns its own copy of the board.
    private NoughtsAndCrosses(char[] board, boolean xToMove) {
        this.board = board;
        this.xToMove = xToMove;
    }

    public Outcome outcome() {
        for (int[] line : WINNING_LINES) {
            char mark = board[line[0]];
            if (mark != EMPTY && mark == board[line[1]] && mark == board[line[2]]) {
                return mark == 'X' ? Outcome.X_WINS : Outcome.O_WINS;
            }
        }
        for (char square : board) {
            if (square == EMPTY) {
                return Outcome.IN_PROGRESS;
            }
        }
        return Outcome.DRAW;
    }

    /** Generate one successor per legal move, in row order. */
    public List<NoughtsAndCrosses> nextStates() {
        List<NoughtsAndCrosses> successors = new ArrayList<>();
        if (outcome() != Outcome.IN_PROGRESS) {
            return successors;
        }

        char mark = xToMove ? 'X' : 'O';
        for (int i = 0; i < board.length; i++) {
            if (board[i] == EMPTY) {
                char[] nextBoard = board.clone();
                nextBoard[i] = mark;
                successors.add(new NoughtsAndCrosses(nextBoard, !xToMove));
            }
        }
        return successors;
    }

    // Different move sequences can reach the same vertex.
    @Override
    public boolean equals(Object other) {
        if (!(other instanceof NoughtsAndCrosses)) {
            return false;
        }
        NoughtsAndCrosses state = (NoughtsAndCrosses) other;
        return xToMove == state.xToMove && Arrays.equals(board, state.board);
    }

    @Override
    public int hashCode() {
        return 31 * Arrays.hashCode(board) + Boolean.hashCode(xToMove);
    }

    @Override
    public String toString() {
        StringBuilder result = new StringBuilder();
        for (int row = 0; row < 3; row++) {
            if (row > 0) {
                result.append("\n---+---+---\n");
            }
            int first = 3 * row;
            result.append(' ').append(board[first])
                  .append(" | ").append(board[first + 1])
                  .append(" | ").append(board[first + 2]).append(' ');
        }
        return result.toString();
    }
}
