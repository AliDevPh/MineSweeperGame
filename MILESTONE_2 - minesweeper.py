import signal
import sys
import itertools
import random as rand
from string import ascii_uppercase

# Function to generate random mines on the board
def generate_mines():
    return [ascii_uppercase[a] + str(b + 1) for a, b in rand.sample(list(itertools.product(range(7), repeat=2)), k=8)]

# Function to create the game board
def create_board(mines):
    board = [['.' for _ in range(7)] for _ in range(7)]
    for mine in mines:
        row = ord(mine[0]) - ord('A')
        col = int(mine[1]) - 1
        board[row][col] = '*'
    return board

# Counting adjacent mines for a cell
def count_adjacent_mines(board, row, col):
    count = 0
    for i in range(max(0, row - 1), min(7, row + 2)):
        for j in range(max(0, col - 1), min(7, col + 2)):
            if board[i][j] == '*':
                count += 1
    return count

# Function to print the game board
def print_board(board, flagged, opened):
    print("    A B C D E F G")

    for i in range(7):
        new_row = []
        for j in range(7):
            coordinate = chr(j + ord('A')) + str(i + 1)
            if coordinate in opened:
                adjacent_mines = count_adjacent_mines(board, i, j)
                new_row.append(str(adjacent_mines) if adjacent_mines > 0 else '0')
            else:
                if coordinate in flagged:
                    new_row.append('?')
                else:
                    new_row.append('.')
        print(f"[{i + 1}]", " ".join(new_row))
    print()
    
 


# Function to validate user input coordinates
def is_valid_input(coord):
    return len(coord) == 2 and coord[0].isalpha() and coord[1].isdigit() and 'A' <= coord[0] <= 'G' and '1' <= coord[1] <= '7'

def expand_zeros(board, opened, row, col):
    if board[row][col] == '0':
        for i in range(max(0, row - 1), min(7, row + 2)):
            for j in range(max(0, col - 1), min(7, col + 2)):
                coord = chr(j + ord('A')) + str(i + 1)
                if coord not in opened:
                    opened.add(coord)
                    expand_zeros(board, opened, i, j)

# Main game function
def game():
    mines = generate_mines()
    board = create_board(mines)
    flagged = set()
    opened = set()
    remaining_mines = 8
    
 # Function to handle interrupt signal (Ctrl+C)
    def exit_game(signal, frame):
        print("\nExiting the game...")
        sys.exit(0)

    signal.signal(signal.SIGINT, exit_game)

    print("\n   MINESWEEPER!\n")
    
    while True:
        print_board(board, flagged, opened)
        print("Mines left:", remaining_mines)
        choice = input("\nControls\n[o] Open a cell\n[f] Flag/unflag a cell\n[CTRL+C] Exit the game\nEnter choice: ")
        
        if choice == 'o':
            while True:
                coordinate = input("Give a coordinate ([A-G][1-7]): ").upper()
                if is_valid_input(coordinate):
                    break
                else:
                    print("Invalid input!")
            
            if coordinate in flagged:
                print("Cannot open a flagged cell.")
                continue
            
            row = ord(coordinate[0]) - ord('A')
            col = int(coordinate[1]) - 1

            if board[row][col] == '*':
                print("You opened a mine! Game Over!")
                break

            # Handling opening of '0' cells and checking for flagged adjacent cells
            if coordinate in opened:
                flagged_count = 0
                for i in range(max(0, row - 1), min(7, row + 2)):
                    for j in range(max(0, col - 1), min(7, col + 2)):
                        if (i, j) != (row, col) and chr(j + ord('A')) + str(i + 1) in flagged:
                            flagged_count += 1
                if flagged_count == count_adjacent_mines(board, row, col) and board[row][col] != '0':
                    for i in range(max(0, row - 1), min(7, row + 2)):
                        for j in range(max(0, col - 1), min(7, col + 2)):
                            if (i, j) != (row, col) and chr(j + ord('A')) + str(i + 1) not in flagged and chr(j + ord('A')) + str(i + 1) not in opened:
                                opened.add(chr(j + ord('A')) + str(i + 1))
                                if board[i][j] == '*':
                                    print("You lose!")
                                    break
                elif board[row][col] == '0' and coordinate in opened:
                    expand_zeros(board, opened, row, col)
                continue

            opened.add(coordinate)
            
            if board[row][col] == '0':
                expand_zeros(board, opened, row, col)
            
        elif choice == 'f':
            while True:
                coordinate = input("Give a coordinate ([A-G][1-7]): ").upper()
                if is_valid_input(coordinate):
                    break
                else:
                    print("Invalid input!")
            
            if coordinate in opened:
                print("Cannot flag an opened cell.")
                continue

            if coordinate in flagged:
                flagged.remove(coordinate)
                remaining_mines += 1
            else:
                flagged.add(coordinate)
                remaining_mines -= 1
            
        else:
            print("Invalid choice. Please enter 'o' for open or 'f' for flag.")
            continue
        
        if len(opened) == 49 - 8:  # If all non-mine cells are opened
            print("Congratulations! You won the game!")
            break

game()
