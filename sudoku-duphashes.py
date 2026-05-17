import sys
import random
import hashlib
from z3 import Solver, Int, Or, Distinct, sat

def create_sudoku_solver():
    """Initializes a Z3 solver with strictly verified Sudoku rules."""
    solver = Solver()
    
    grid_A = [[Int(f"A_{r}_{c}") for c in range(9)] for r in range(9)]
    grid_B = [[Int(f"B_{r}_{c}") for c in range(9)] for r in range(9)]
    
    # Boundary constraints (1-9)
    for r in range(9):
        for c in range(9):
            solver.add(grid_A[r][c] >= 1, grid_A[r][c] <= 9)
            solver.add(grid_B[r][c] >= 1, grid_B[r][c] <= 9)
            
    # Row and Column uniqueness constraints
    for i in range(9):
        solver.add(Distinct([grid_A[i][j] for j in range(9)]))
        solver.add(Distinct([grid_A[j][i] for j in range(9)]))
        solver.add(Distinct([grid_B[i][j] for j in range(9)]))
        solver.add(Distinct([grid_B[j][i] for j in range(9)]))
        
    # FIXED: Exact 3x3 Box uniqueness constraints mapping all 9 distinct sectors
    for r_box in range(0, 9, 3):
        for c_box in range(0, 9, 3):
            box_A = [grid_A[r_box + r][c_box + c] for r in range(3) for c in range(3)]
            box_B = [grid_B[r_box + r][c_box + c] for r in range(3) for c in range(3)]
            solver.add(Distinct(box_A))
            solver.add(Distinct(box_B))
            
    return solver, grid_A, grid_B

def stream_multi_solution_hashes():
    """Streams cryptographically valid non-unique Sudoku board hashes."""
    sys.stdout.reconfigure(line_buffering=True)
    
    while True:
        solver, grid_A, grid_B = create_sudoku_solver()
        
        # Safe random clue generation range
        num_clues = random.randint(22, 28)
        clue_positions = [(random.randint(0, 8), random.randint(0, 8)) for _ in range(num_clues)]
        
        puzzle_clues = {}
        for r, c in clue_positions:
            if (r, c) not in puzzle_clues:
                val = random.randint(1, 9)
                puzzle_clues[(r, c)] = val
                solver.add(grid_A[r][c] == val)
                solver.add(grid_B[r][c] == val)
                
        # Force a parallel fork path
        different_cells = [grid_A[r][c] != grid_B[r][c] for r in range(9) for c in range(9)]
        solver.add(Or(different_cells))
        
        if solver.check() == sat:
            dot_notation = []
            zero_notation = []
            
            for r in range(9):
                for c in range(9):
                    if (r, c) in puzzle_clues:
                        digit = str(puzzle_clues[(r, c)])
                        dot_notation.append(digit)
                        zero_notation.append(digit)
                    else:
                        dot_notation.append(".")
                        zero_notation.append("0")
            
            str_dot = "".join(dot_notation)
            str_zero = "".join(zero_notation)
            
            hash_dot = hashlib.sha1(str_dot.encode('utf-8')).hexdigest()
            hash_zero = hashlib.sha1(str_zero.encode('utf-8')).hexdigest()
            
            print(f"BLACKLIST_HASH_DOT:{hash_dot} | BLACKLIST_HASH_ZERO:{hash_zero}")

if __name__ == "__main__":
    try:
        stream_multi_solution_hashes()
    except KeyboardInterrupt:
        sys.exit(0)
