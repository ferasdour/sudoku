from z3 import Solver, Int, Distinct, Or, And, sat

def analyze_ambiguity_patterns():
    solver = Solver()
    
    # 1. Setup two parallel boards
    A = [[Int(f"A_{r}_{c}") for c in range(9)] for r in range(9)]
    B = [[Int(f"B_{r}_{c}") for c in range(9)] for r in range(9)]
    
    # 2. Standard Sudoku Constraint Rules for both boards
    for r in range(9):
        for c in range(9):
            solver.add(A[r][c] >= 1, A[r][c] <= 9, B[r][c] >= 1, B[r][c] <= 9)
            
    for i in range(9):
        solver.add(Distinct([A[i][j] for j in range(9)]))
        solver.add(Distinct([A[j][i] for j in range(9)]))
        solver.add(Distinct([B[i][j] for j in range(9)]))
        solver.add(Distinct([B[j][i] for j in range(9)]))
        
    for br in range(3):
        for bc in range(3):
            solver.add(Distinct([A[br*3 + r][bc*3 + c] for r in range(3) for c in range(3)]))
            solver.add(Distinct([B[br*3 + r][bc*3 + c] for r in range(3) for c in range(3)]))

    # 3. ANALYSIS CONSTRAINT: 
    # Force the boards to be identical almost everywhere, but swap a few cells.
    # We restrict divergence to a maximum of 4 cells to catch minimal "Deadly Rectangles".
    divergent_cells = [A[r][c] != B[r][c] for r in range(9) for c in range(9)]
    solver.add(Or(divergent_cells)) # At least something must differ
    
    # Keep the rest of the 77 cells locked identical
    same_cells = [A[r][c] == B[r][c] for r in range(9) for c in range(9)]
    # We tell Z3 that AT MOST 4 cells can be different (meaning at least 77 must be identical)
    from z3 import PbGe
    solver.add(PbGe([(cell, 1) for cell in same_cells], 77))

    # 4. Process and interpret the structural failure
    if solver.check() == sat:
        model = solver.model()
        
        # Collect the coordinates where the discrepancy happened
        failed_coords = []
        for r in range(9):
            for c in range(9):
                val_A = model.evaluate(A[r][c]).as_long()
                val_B = model.evaluate(B[r][c]).as_long()
                if val_A != val_B:
                    failed_coords.append((r, c, val_A, val_B))
                    
        # Sort out rows, columns, and boxes involved
        rows = sorted(list(set(c[0] for c in failed_coords)))
        cols = sorted(list(set(c[1] for c in failed_coords)))
        boxes = sorted(list(set((c[0]//3)*3 + (c[1]//3) for c in failed_coords)))
        values = sorted(list(set(c[2] for c in failed_coords)))

        # Output a human-readable diagnosis
        print("🔍 [Z3 PATTERN ANALYSIS REPORT]")
        print("==================================================")
        print("⚠️ WARNING: Found a structural logic trap!")
        print(f"-> Pattern Type: Unique Rectangle / Deadly Pattern Loop")
        print(f"-> Involved Values: {values}")
        print(f"-> Affected Rows: {rows}")
        print(f"-> Affected Columns: {cols}")
        print(f"-> Total Boxes Trapped: {len(boxes)} (Box IDs: {boxes})")
        print("==================================================")
        print("\n📍 COORDINATE MAP OF THE DEADLY PATTERN:")
        
        # Display a mini text map of the pattern
        for r in range(9):
            row_str = []
            for c in range(9):
                match = [item for item in failed_coords if item[0] == r and item[1] == c]
                if match:
                    row_str.append(f"[{match[0][2]}/{match[0][3]}]") # Show the swapped candidates
                else:
                    row_str.append(" . ")
            print(" ".join(row_str))
            
        print("\n💡 HOW TO FIX OR WATCH OUT FOR THIS:")
        print(f"If these cells are stripped of clues, numbers {values} can be flipped seamlessly.")
        print(f"To ensure a unique solution, you MUST place at least one permanent starting clue")
        print(f"inside one of these specific coordinates: {[(c[0], c[1]) for c in failed_coords]}")
        
    else:
        print("No small localized deadly loops found under these settings.")

if __name__ == "__main__":
    analyze_ambiguity_patterns()
