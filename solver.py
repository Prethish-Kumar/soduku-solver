import tkinter as tk
import time
import customtkinter

grid = [[None for _ in range(9)] for _ in range(9)]
grid_values = []

def get_bg_color(row, col):
    color1 = 'light yellow'
    color2 = 'light cyan'
    
    sub_grid_row = row // 3
    sub_grid_col = col // 3

    if (sub_grid_row + sub_grid_col) % 2 == 0:
        return color1
    else:
        return color2

def create_grid(root):
    frame = customtkinter.CTkFrame(root)
    frame.pack()

    for i in range(9):
        for j in range(9):
            bg_color = get_bg_color(i, j)
            cell = customtkinter.CTkEntry(frame, height=40, width=40, justify='center', font=('Arial', 18), fg_color=bg_color, text_color='black')
            cell.grid(row=i, column=j, padx=5, pady=5)
            grid[i][j] = cell

    return grid

def read_grid(grid):
    global grid_values 
    grid_values = [[grid[i][j].get() for j in range(9)] for i in range(9)]

def clear_grid(grid):
    for row in grid:
        for cell in row:
            cell.delete(0, tk.END)


def is_valid(row,col,guess):
    global grid_values

    guess = str(guess)
    
    # Check If Guess Is In The Row
    if guess in grid_values[row]:
        return False
    
    #Check If Guess Is In The Coloumn
    for r in range(9):
        if grid_values[r][col] == guess:
            return False
        
    #Check in 3*3 Subgrid
    subgrid_row = row // 3 * 3
    subgrid_col = col // 3 * 3

    for r in range(subgrid_row, subgrid_row+3):
        for c in range(subgrid_col, subgrid_col+3):
            if guess == grid_values[r][c]: 
                return False
    return True

def solve(grid_values,visualise):
    global grid
    for row in range(9):
        for col in range(9):
            if grid_values[row][col] == '':
                for guess in range(1,10):
                    if is_valid(row,col,guess):
                        
                        grid_values[row][col] = str(guess)
                        grid[row][col].delete(0, tk.END)
                        grid[row][col].insert(0, grid_values[row][col]) 
                        if(visualise):
                            time.sleep(0.15)
                            grid[row][col].update_idletasks()

                        if solve(grid_values,visualise):
                            return True
                        grid_values[row][col] = ''
                        grid[row][col].delete(0, tk.END)
                        if(visualise):
                            grid[row][col].update_idletasks()

                return False
    return True

def solve_time(grid,visualise):
    start_time = time.time()
    solve(grid,visualise)
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f'Time Taken = {elapsed_time}')

def main():
    root = customtkinter.CTk()
    root.title("Sudoku Solver")

    create_grid(root)


    clear_button = customtkinter.CTkButton(root, text="Clear Grid", command=lambda: clear_grid(grid))
    clear_button.pack(side='top',pady=10) 

    fast_solve_button = customtkinter.CTkButton(root, text="Solve Sudoku", command=lambda: [read_grid(grid), solve_time(grid_values,False)])
    fast_solve_button.pack(side='top',pady=10)

    visualise_solve_button = customtkinter.CTkButton(root, text=" Visually Solve Sudoku", command=lambda: [read_grid(grid), solve_time(grid_values, True)])
    visualise_solve_button.pack(side='top',pady=10)
        
    root.mainloop()

if __name__ == "__main__":
    main()