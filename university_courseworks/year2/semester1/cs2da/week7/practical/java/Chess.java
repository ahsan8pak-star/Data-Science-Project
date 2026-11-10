import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

/**
 * One immutable vertex in a simplified chess game graph.
 * Includes checkmate, stalemate and promotion. Omits castling, en passant
 * and all draws other than stalemate.
 */
public final class Chess {
    public enum Outcome {
        IN_PROGRESS, WHITE_WINS, BLACK_WINS, DRAW
    }

    private static final int SIZE = 8;
    private static final char EMPTY = ' ';
    private static final char[] PROMOTIONS = {'Q', 'R', 'B', 'N'};

    // Row order from a8 to h1. Uppercase is White and lowercase is Black.
    private final char[] board;
    private final boolean whiteToMove;

    /** Start from the standard initial position with White to move. */
    public Chess() {
        board = ("rnbqkbnr" + "pppppppp"
               + "        " + "        " + "        " + "        "
               + "PPPPPPPP" + "RNBQKBNR").toCharArray();
        whiteToMove = true;
    }

    private Chess(char[] board, boolean whiteToMove) {
        this.board = board;
        this.whiteToMove = whiteToMove;
    }

    public Outcome outcome() {
        if (!generateSuccessors(true).isEmpty()) {
            return Outcome.IN_PROGRESS;
        }
        if (!isAttacked(board, kingSquare(), !whiteToMove)) {
            return Outcome.DRAW; // stalemate
        }
        return whiteToMove ? Outcome.BLACK_WINS : Outcome.WHITE_WINS;
    }

    /** Generate one successor per legal move, including each promotion choice. */
    public List<Chess> nextStates() {
        return generateSuccessors(false);
    }

    private List<Chess> generateSuccessors(boolean firstOnly) {
        List<Chess> successors = new ArrayList<>();
        int king = kingSquare();
        for (int from = 0; from < board.length; from++) {
            char piece = board[from];
            if (piece == EMPTY || isWhite(piece) != whiteToMove) {
                continue;
            }
            for (int to = 0; to < board.length; to++) {
                if (!canMove(from, to)) {
                    continue;
                }

                char[] nextBoard = board.clone();
                nextBoard[from] = EMPTY;
                nextBoard[to] = piece;

                // A move is legal only if our king is safe afterwards.
                int nextKing = from == king ? to : king;
                if (isAttacked(nextBoard, nextKing, !whiteToMove)) {
                    continue;
                }
                int promotionRow = whiteToMove ? 0 : SIZE - 1;
                if (Character.toUpperCase(piece) == 'P' && to / SIZE == promotionRow) {
                    for (char promotion : PROMOTIONS) {
                        char[] promoted = nextBoard.clone();
                        promoted[to] = whiteToMove ? promotion : Character.toLowerCase(promotion);
                        successors.add(new Chess(promoted, !whiteToMove));
                    }
                } else {
                    successors.add(new Chess(nextBoard, !whiteToMove));
                }
                if (firstOnly) {
                    return successors;
                }
            }
        }
        return successors;
    }

    /** Check the piece's movement rules before considering king safety. */
    private boolean canMove(int from, int to) {
        char piece = board[from];
        char target = board[to];
        if (target != EMPTY) {
            // The game ends at checkmate, so a king is never captured.
            if (isWhite(piece) == isWhite(target) || Character.toUpperCase(target) == 'K') {
                return false;
            }
            return attacks(board, from, to);
        }

        if (Character.toUpperCase(piece) != 'P') {
            return attacks(board, from, to);
        }

        int step = whiteToMove ? -SIZE : SIZE;
        int homeRow = whiteToMove ? 6 : 1;
        return to == from + step
            || (from / SIZE == homeRow && to == from + 2 * step && board[from + step] == EMPTY);
    }

    private int kingSquare() {
        char king = whiteToMove ? 'K' : 'k';
        for (int square = 0; square < board.length; square++) {
            if (board[square] == king) {
                return square;
            }
        }
        throw new IllegalStateException("King is missing");
    }

    private static boolean isAttacked(char[] position, int square, boolean byWhite) {
        for (int from = 0; from < position.length; from++) {
            char piece = position[from];
            if (piece != EMPTY && isWhite(piece) == byWhite && attacks(position, from, square)) {
                return true;
            }
        }
        return false;
    }

    // Attack geometry ignores king safety. Even a pinned piece attacks squares.
    private static boolean attacks(char[] position, int from, int to) {
        if (from == to) {
            return false;
        }
        int rowChange = to / SIZE - from / SIZE;
        int colChange = to % SIZE - from % SIZE;
        int rows = Math.abs(rowChange);
        int cols = Math.abs(colChange);
        boolean straight = rows == 0 || cols == 0;
        boolean diagonal = rows == cols;
        char piece = position[from];

        switch (Character.toUpperCase(piece)) {
            case 'P':
                return rowChange == (isWhite(piece) ? -1 : 1) && cols == 1;
            case 'N':
                return (rows == 1 && cols == 2) || (rows == 2 && cols == 1);
            case 'K':
                return rows <= 1 && cols <= 1;
            case 'B':
                return diagonal && clearPath(position, from, to, rowChange, colChange);
            case 'R':
                return straight && clearPath(position, from, to, rowChange, colChange);
            case 'Q':
                return (straight || diagonal) && clearPath(position, from, to, rowChange, colChange);
            default:
                throw new IllegalStateException("Unknown piece " + piece);
        }
    }

    // Called only for distinct squares on the same rank, file or diagonal.
    private static boolean clearPath(char[] position, int from, int to, int rowChange, int colChange) {
        int step = SIZE * Integer.signum(rowChange) + Integer.signum(colChange);
        for (int square = from + step; square != to; square += step) {
            if (position[square] != EMPTY) {
                return false;
            }
        }
        return true;
    }

    private static boolean isWhite(char piece) {
        return Character.isUpperCase(piece);
    }

    @Override
    public boolean equals(Object other) {
        if (!(other instanceof Chess)) {
            return false;
        }
        Chess state = (Chess) other;
        return whiteToMove == state.whiteToMove && Arrays.equals(board, state.board);
    }

    @Override
    public int hashCode() {
        return 31 * Arrays.hashCode(board) + Boolean.hashCode(whiteToMove);
    }

    @Override
    public String toString() {
        StringBuilder result = new StringBuilder();
        result.append("  +-----------------+\n");
        for (int row = 0; row < SIZE; row++) {
            result.append(SIZE - row).append(" |");
            for (int col = 0; col < SIZE; col++) {
                result.append(' ').append(board[row * SIZE + col]);
            }
            result.append(" |\n");
        }
        result.append("  +-----------------+\n");
        result.append("    a b c d e f g h\n");
        result.append(whiteToMove ? "White to move" : "Black to move");
        return result.toString();
    }
}
