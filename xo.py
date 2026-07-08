board = [" " for _ in range(9)]
def print_board():
    print(f"{board[0]}|{board[1]}|{board[2]}\n-+-+-\n{board[3]}|{board[4]}|{board[5]}\n-+-+-\n{board[6]}|{board[7]}|{board[8]}")
def check_winner():
    win_coords = [(0,1,2), (3,4,5), (6,7,8), (0,3,6), (1,4,7), (2,5,8), (0,4,8), (2,4,6)]
    for a, b, c in win_coords:
        if board[a] == board[b] == board[c] and board[a] != " ": return board[a]
    return None
player = "X"
for turn in range(9):
    print_board()
    try:
        choice = int(input(f"Player {player}, enter (1-9): ")) - 1
        if board[choice] == " ":
            board[choice] = player
            if check_winner(): print_board(); print(f"Winner: {player}"); break
            player = "O" if player == "X" else "X"
        else: print("Spot taken!")
    except: print("Invalid input!")
else: print("Tie!")

