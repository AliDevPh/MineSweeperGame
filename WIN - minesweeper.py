# Function to generate random mine locations
def generate_mines():
    import random
    return random.sample([(i, j) for i in range(7) for j in range(7)], k=8)

# Function to display the grid
def display_grid(grid):
    print("  A B C D E F G")
    for i in range(len(grid)):
        print(f"{i + 1} ", end="")
        for j in range(len(grid[i])):
            if grid[i][j][0] == ".":   # If cell is not revealed
                print(".", end=" ")
            else:
                print(grid[i][j][1], end=" ") # Print the cell content
        print()

# Function to count adjacent mines to a cell
def count_adjacent_mines(grid, row, col):
    count = 0
    for i in range(-1, 2):
        for j in range(-1, 2):
            if (0 <= row + i < 7) and (0 <= col + j < 7) and grid[row + i][col + j][1] == "!":
                count += 1
    return count

# Function to reveal a cell based on user input
def reveal_cell(grid, row, col, mines):
    if grid[row][col][0] == ".":
        count = count_adjacent_mines(grid, row, col)
        if count > 0:
            grid[row][col] = (" ", str(count))   # Reveal the cell with adjacent mine count
        else:
            grid[row][col] = (" ", "0") # If no adjacent mines, mark as "0"

# Main game function
def main():
    mines = generate_mines()
    grid = [[(".", " ") for _ in range(7)] for _ in range(7)]

    for mine in mines:
        row, col = mine
        grid[row][col] = (".", "!")  # Place the mines in the grid

    game_over = False

    print("\n   MINESWEEPER!\n")
    while not game_over:
        display_grid(grid) # Display the grid for the player
        coordinate = input("Give a coordinate ([A-G][1-7]):  ") # Ask for user input

        if len(coordinate) != 2 or not (coordinate[0].isalpha() and coordinate[1].isdigit()):
            print("Invalid input.")
            continue

        col = ord(coordinate[0].upper()) - ord('A') # Convert input to grid column index
        row = int(coordinate[1]) - 1

        if row < 0 or row > 6 or col < 0 or col > 6:  # Check if the coordinate is within the grid range
            print("Coordinate out of range.")
            continue

        if grid[row][col][0] == "!": # If the selected cell has a mine
            game_over = True
            grid[row][col] = (" ", "!")  # Show the hit mine
        else:
            reveal_cell(grid, row, col, mines) # Reveal the selected cell
            if grid[row][col][1] == "0": # If selected cell has no adjacent mines
                reveal_cell(grid, row, col, mines) # Reveal surrounding cells without mines

        revealed_count = sum(row.count(' ') for row in grid)
        if revealed_count == 49 - len(mines): # Check if all non-mine cells are revealed
            all_revealed = all(grid[i][j][0] != "." or grid[i][j][1] == "!" for i in range(7) for j in range(7))
            if all_revealed:
                game_over = True
                print("Congratulations! You've won the game.")
            else:
                game_over = True

    display_grid(grid) # Display final grid
    print("Game Over! You hit a mine.")

if __name__ == "__main__":
    main()
