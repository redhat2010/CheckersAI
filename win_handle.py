import mover

# Checks if there are any moves left for the specified color
def move_check(board,color):
    for i in range(8):
        for j in range(8):
            if board[i][j] != 0 and board[i][j] != 1:
                if board[i][j].get_color() == color:
                    if i != 7:
                        if j != 7:
                            trial1 = mover.validator(board, color, [(i,j),(i+1,j+1)])
                            if trial1:
                                return True
                        if j != 0:
                            trial2 = mover.validator(board, color, [(i,j),(i+1,j-1)])
                            if trial2:
                                return True
                    if i != 0:
                        if j != 7:
                            trial3 = mover.validator(board, color, [(i,j),(i-1,j+1)])
                            if trial3:
                                return True
                        if j != 0:
                            trial4 = mover.validator(board, color, [(i,j),(i-1,j-1)])
                            if trial4:
                                return True
                    if i < 6:
                        if j < 6:
                            trial5 = mover.validator(board, color, [(i,j),(i+2,j+2)])
                            if trial5:
                                return True
                        if j > 1:
                            trial6 = mover.validator(board, color, [(i,j),(i+2,j-2)])
                            if trial6:
                                return True
                    if i > 1:
                        if j < 6:
                            trial7 = mover.validator(board, color, [(i,j),(i-2,j+2)])
                            if trial7:
                                return True
                        if j > 1:
                            trial8 = mover.validator(board, color, [(i,j),(i-2,j-2)])
                            if trial8:
                                return True
    return False

# Determines if someone won
# Counts contains the count of red pieces and black pieces, in that order
def loss_check(board,counts):
    if counts[0] == 0:
        return "RED"
    elif counts[1] == 0:
        return "BLACK"
    
    red_can_move = move_check(board.copy(), "red")
    black_can_move = move_check(board.copy(), "black")

    if not red_can_move and not black_can_move:
        return "DRAW"
    elif not red_can_move:
        return "RED"
    elif not black_can_move:
        return "BLACK"
    else:
        return "CONTINUE"