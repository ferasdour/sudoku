from z3 import Solver, Int, Distinct, Or, And

def generate_sudoku_logic_expression():
    # Instantiate parallel symbolic board variables
    grid_A = [[Int(f"A_{r}_{c}") for c in range(9)] for r in range(9)]
    grid_B = [[Int(f"B_{r}_{c}") for c in range(9)] for r in range(9)]
    
    # Store all mathematical conditions in a list
    constraints = []
    
    # 1. Bounds Constraints: Values must be between 1 and 9
    for r in range(9):
        for c in range(9):
            constraints.append(grid_A[r][c] >= 1)
            constraints.append(grid_A[r][c] <= 9)
            constraints.append(grid_B[r][c] >= 1)
            constraints.append(grid_B[r][c] <= 9)
            
    # 2. Structural Sudoku Rules (Rows, Cols, 3x3 Boxes)
    for i in range(9):
        # Row uniqueness
        constraints.append(Distinct([grid_A[i][j] for j in range(9)]))
        constraints.append(Distinct([grid_B[i][j] for j in range(9)]))
        # Column uniqueness
        constraints.append(Distinct([grid_A[j][i] for j in range(9)]))
        constraints.append(Distinct([grid_B[j][i] for j in range(9)]))
        
    for r_box in range(3):
        for c_box in range(3):
            box_A = [grid_A[r_box*3 + r][c_box*3 + c] for r in range(3) for c in range(3)]
            box_B = [grid_B[r_box*3 + r][c_box*3 + c] for r in range(3) for c in range(3)]
            constraints.append(Distinct(box_A))
            constraints.append(Distinct(box_B))
            
    # 3. The Non-Uniqueness Paradox Formula
    # "There must exist at least one coordinate where Matrix A does not equal Matrix B"
    divergence_conditions = [grid_A[r][c] != grid_B[r][c] for r in range(9) for c in range(9)]
    constraints.append(Or(divergence_conditions))
    
    # 4. Compile all rules into one master formula expression
    master_formula = And(constraints)
    
    # Export the mathematical expression to standard SMT-LIB2 format
    solver = Solver()
    solver.add(master_formula)
    
    return solver.to_smt2()

# Print the mathematical structure
smt_expression = generate_sudoku_logic_expression()
print("--- FIRST 30 LINES OF THE MATHEMATICAL FORMULA ---")
print("\n".join(smt_expression.split("\n")[:30]))

# Save the full giant formula to a file
with open("sudoku_non_uniqueness.smt2", "w") as f:
    f.write(smt_expression)
print("\n[SUCCESS]: Full mathematical expression saved to 'sudoku_non_uniqueness.smt2'")
