
def get_candidates(board, row, col):
    """Returns a set of all valid numbers (1-9) that can fit in a specific cell."""
    if board[row][col] != 0:
        return set()
    
    candidates = set(range(1, 10))
    
    # Remove numbers already in the same row and column
    for i in range(9):
        candidates.discard(board[row][i])
        candidates.discard(board[i][col])
        
    # Remove numbers already in the same 3x3 box
    box_row, box_col = 3 * (row // 3), 3 * (col // 3)
    for r in range(box_row, box_row + 3):
        for c in range(box_col, box_col + 3):
            candidates.discard(board[r][c])
            
    return candidates

def find_naked_single(board):
    """Strategy 1: Find a cell with the least requirements left (exactly 1 candidate)."""
    for r in range(9):
        for c in range(9):
            if board[r][c] == 0:
                candidates = get_candidates(board, r, c)
                if len(candidates) == 1:
                    return r, c, list(candidates)[0]
    return None

def find_hidden_single(board):
    """Strategy 2: Find a number that has only one possible home in a row, col, or box."""
    # Check Rows
    for r in range(9):
        for num in range(1, 10):
            possible_cols = [c for c in range(9) if board[r][c] == 0 and num in get_candidates(board, r, c)]
            if len(possible_cols) == 1:
                return r, possible_cols[0], num

    # Check Columns
    for c in range(9):
        for num in range(1, 10):
            possible_rows = [r for r in range(9) if board[r][c] == 0 and num in get_candidates(board, r, c)]
            if len(possible_rows) == 1:
                return possible_rows[0], c, num

    # Check 3x3 Boxes
    for box_i in range(3):
        for box_j in range(3):
            for num in range(1, 10):
                possible_cells = []
                for r in range(box_i * 3, box_i * 3 + 3):
                    for c in range(box_j * 3, box_j * 3 + 3):
                        if board[r][c] == 0 and num in get_candidates(board, r, c):
                            possible_cells.append((r, c))
                if len(possible_cells) == 1:
                    r, c = possible_cells[0]
                    return r, c, num
                    
    return None

def solve_sudoku_human_style(board):
    """Solves the Sudoku by repeatedly applying human deduction strategies."""
    while True:
        # Step 1: Scan for Naked Singles (cells with only 1 option left)
        move = find_naked_single(board)
        
        # Step 2: If none found, scan for Hidden Singles (only 1 valid spot left for a number)
        if not move:
            move = find_hidden_single(board)
            
        # Step 3: If a deduction was made, fill the cell and restart the loop
        if move:
            row, col, val = move
            board[row][col] = val
            print(f"Human logic filled cell ({row},{col}) with {val}")
        else:
            # If no single positions can be deduced, break the loop
            break

    # Check if the board is completely filled
    return all(board[r][c] != 0 for r in range(9) for c in range(9))

# Example Puzzle (Easy to Medium difficulty)
board = [
    [8, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 3, 6, 0, 0, 0, 0, 0],
    [0, 7, 0, 0, 9, 0, 2, 0, 0],
    [0, 5, 0, 0, 0, 7, 0, 0, 0],
    [0, 0, 0, 0, 4, 5, 7, 0, 0],
    [0, 0, 0, 1, 0, 0, 0, 3, 0],
    [0, 0, 1, 0, 0, 0, 0, 6, 8],
    [0, 0, 8, 5, 0, 0, 0, 1, 0],
    [0, 9, 0, 0, 0, 0, 4, 0, 0]
]

if solve_sudoku_human_style(board):
    print("\nPuzzle solved entirely using human logic!")
else:
    print("\nPuzzle stalled. Human logic requires advanced strategies (e.g., Naked Pairs, X-Wing).")
