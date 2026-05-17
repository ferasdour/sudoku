import random
from z3 import Solver, Int, And, Or, Distinct, sat

def create_sudoku_solver():
    """Initializes a Z3 solver with standard Sudoku rules."""
    solver = Solver()
    
    # Create two parallel 9x9 grids of Z3 Integer variables
    grid_A = [[Int(f"A_{r}_{c}") for c in range(9)] for r in range(9)]
    grid_B = [[Int(f"B_{r}_{c}") for c in range(9)] for r in range(9)]
    
    # Value constraints: Every cell must be between 1 and 9
    for r in range(9):
        for c in range(9):
            solver.add(grid_A[r][c] >= 1, grid_A[r][c] <= 9)
            solver.add(grid_B[r][c] >= 1, grid_B[r][c] <= 9)
            
    # Structural constraints: Rows, Columns, and 3x3 Boxes must have distinct values
    for i in range(9):
        # Rows and Columns
        solver.add(Distinct([grid_A[i][j] for j in range(9)]))
        solver.add(Distinct([grid_A[j][i] for j in range(9)]))
        solver.add(Distinct([grid_B[i][j] for j in range(9)]))
        solver.add(Distinct([grid_B[j][i] for j in range(9)]))
        
    # 3x3 Boxes
    for r_box in range(3):
        for c_box in range(3):
            box_A = [grid_A[r_box*3 + r][c_box*3 + c] for r in range(3) for c in range(3)]
            box_B = [grid_B[r_box*3 + r][c_box*3 + c] for r in range(3) for c in range(3)]
            solver.add(Distinct(box_A))
            solver.add(Distinct(box_B))
            
    return solver, grid_A, grid_B

def generate_multi_solution_boards():
    """Generates continuous partial Sudoku puzzles that have multiple solutions."""
    count = 0
    
    while True:
        solver, grid_A, grid_B = create_sudoku_solver()
        
        # 1. Generate a seed: Choose a random amount of starter clues (e.g., 20 to 25 clues)
        # Fewer clues highly increases the likelihood of creating a multiple-solution board
        num_clues = random.randint(20, 25)
        clue_positions = [(random.randint(0, 8), random.randint(0, 8)) for _ in range(num_clues)]
        
        # 2. Force Grid A and Grid B to share the exact same starting clues
        puzzle_clues = {}
        for r, c in clue_positions:
            if (r, c) not in puzzle_clues:
                val = random.randint(1, 9)
                puzzle_clues[(r, c)] = val
                solver.add(grid_A[r][c] == val)
                solver.add(grid_B[r][c] == val)
                
        # 3. CRITICAL CONSTRAINT: Force Grid A and Grid B to differ somewhere!
        # This guarantees Z3 will ONLY find a solution if the clues allow two different final outcomes.
        different_cells = []
        for r in range(9):
            for c in range(9):
                different_cells.append(grid_A[r][c] != grid_B[r][c])
        solver.add(Or(different_cells))
        
        # 4. Check if a multi-solution puzzle exists for these clues
        if solver.check() == sat:
            count += 1
            model = solver.model()
            
            # Construct the puzzle string/matrix (0 = empty cell)
            display_puzzle = [[0 for _ in range(9)] for _ in range(9)]
            for (r, c), val in puzzle_clues.items():
                display_puzzle[r][c] = val
                
            print(f"\n=========================================")
            print(f" MULTI-SOLUTION PUZZLE FOUND #{count}")
            print(f"=========================================")
            for row in display_puzzle:
                print(" ".join(str(x) if x != 0 else "." for x in row))
                
            # Print Solution Option #1
            print("\n--- Solution Variant A ---")
            for r in range(9):
                print(" ".join(str(model.evaluate(grid_A[r][c])) for c in range(9)))
                
            # Print Solution Option #2
            print("\n--- Solution Variant B ---")
            for r in range(9):
                print(" ".join(str(model.evaluate(grid_B[r][c])) for c in range(9)))
                
            # To avoid generating the exact same puzzle layout again, we block this specific set of clues
            # (The loop continues indefinitely finding brand new invalid boards)
            print("\nTThe next board...")

if __name__ == "__main__":
    print("Starting continuous Z3 Sudoku Non-Uniqueness Generator...")
    generate_multi_solution_boards()
