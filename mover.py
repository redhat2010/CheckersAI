import piece

# Verifieds a sequence of moves
def validator(board, turn, move_sequence):
    if len(move_sequence) <= 1:
        return False

    moved_piece_y, moved_piece_x = move_sequence[0]
    moved_piece = board[moved_piece_y][moved_piece_x]
    if moved_piece == 0 or moved_piece == 1:
        return False
    elif moved_piece.get_color() != turn:
        return False
    
    jumped = []
    
    #print(moved_piece.get_kinged())
    was_kinged = moved_piece.get_kinged()
    for i in range(1,len(move_sequence)):
        move_y, move_x = move_sequence[i]
        if board[move_y][move_x] != 1 and move_x != moved_piece_x and move_y != moved_piece_y:
            return False
        previous_y, previous_x = move_sequence[i-1]
        

        if moved_piece.get_color() == "black":
            if move_y == 7:
                was_kinged = True
            if (previous_y + 1) == move_y and ((previous_x + 1) == move_x or (previous_x - 1) == move_x):
                if len(move_sequence) > 2:
                    return False
            elif (previous_y + 2) == move_y and (previous_x + 2) == move_x:
                if board[previous_y + 1][previous_x + 1] != 0 and board[previous_y + 1][previous_x + 1] != 1:
                    if board[previous_y + 1][previous_x + 1].get_color() != "red":
                        return False
                    elif (previous_y + 1, previous_x + 1) in jumped:
                        return False
                    else:
                        jumped.append((previous_y + 1, previous_x + 1))

                else:
                    return False
            elif (previous_y + 2) == move_y and (previous_x - 2) == move_x:
                if board[previous_y + 1][previous_x - 1] != 0 and board[previous_y + 1][previous_x - 1] != 1:
                    if board[previous_y + 1][previous_x - 1].get_color() != "red":
                        return False
                    elif (previous_y + 1, previous_x - 1) in jumped:
                        return False
                    else:
                        jumped.append((previous_y + 1, previous_x - 1))
                else:
                    return False
            elif moved_piece.get_kinged() or was_kinged:
                print(moved_piece.get_kinged())
                if (previous_y - 1) == move_y and ((previous_x + 1) == move_x or (previous_x - 1) == move_x):
                    print("here!!!!")
                    if len(move_sequence) > 2:
                        return False
                elif (previous_y - 2) == move_y and (previous_x + 2) == move_x:
                    if board[previous_y - 1][previous_x + 1] != 0 and board[previous_y - 1][previous_x + 1] != 1:
                        if board[previous_y - 1][previous_x + 1].get_color() != "red":
                            return False
                        elif (previous_y - 1, previous_x + 1) in jumped:
                            return False
                        else:
                            jumped.append((previous_y - 1, previous_x + 1))
                    else:
                        return False
                elif (previous_y - 2) == move_y and (previous_x - 2) == move_x:
                    if board[previous_y - 1][previous_x - 1] != 0 and board[previous_y - 1][previous_x - 1] != 1:
                        if board[previous_y - 1][previous_x - 1].get_color() != "red":
                            return False
                        elif (previous_y - 1, previous_x - 1) in jumped:
                            return False
                        else:
                            jumped.append((previous_y - 1, previous_x - 1))
                    else:
                        return False
            else:
                return False
            
            #if move_sequence[i][0] == 7:
                #moved_piece.king()
            
        elif moved_piece.get_color() == "red":
            if move_y == 7:
                was_kinged = True
            if (previous_y - 1) == move_y and ((previous_x + 1) == move_x or (previous_x - 1) == move_x):
                if len(move_sequence) > 2:
                    return False
            elif (previous_y - 2) == move_y and (previous_x + 2) == move_x:
                if board[previous_y - 1][previous_x + 1] != 0 and board[previous_y - 1][previous_x + 1] != 1:
                    if board[previous_y - 1][previous_x + 1].get_color() != "black":
                        return False
                    elif (previous_y - 1, previous_x + 1) in jumped:
                        return False
                    else:
                        jumped.append((previous_y - 1, previous_x + 1))
                else:
                    return False
            elif (previous_y - 2) == move_y and (previous_x - 2) == move_x:
                if board[previous_y - 1][previous_x - 1] != 0 and board[previous_y - 1][previous_x - 1] != 1:
                    if board[previous_y - 1][previous_x - 1].get_color() != "black":
                        return False
                    elif (previous_y - 1, previous_x - 1) in jumped:
                        return False
                    else:
                        jumped.append((previous_y - 1, previous_x - 1))
                else:
                    return False
            elif moved_piece.get_kinged() or was_kinged:
                if (previous_y + 1) == move_y and ((previous_x + 1) == move_x or (previous_x - 1) == move_x):
                    if len(move_sequence) > 2:
                        return False
                elif (previous_y + 2) == move_y and (previous_x + 2) == move_x:
                    if board[previous_y + 1][previous_x + 1] != 0 and board[previous_y + 1][previous_x + 1] != 1:
                        if board[previous_y + 1][previous_x + 1].get_color() != "black":
                            return False
                        elif (previous_y + 1, previous_x + 1) in jumped:
                            return False
                        else:
                            jumped.append((previous_y + 1, previous_x + 1))
                    else:
                        return False
                elif (previous_y + 2) == move_y and (previous_x - 2) == move_x:
                    if board[previous_y + 1][previous_x - 1] != 0 and board[previous_y + 1][previous_x - 1] != 1:
                        if board[previous_y + 1][previous_x - 1].get_color() != "black":
                            return False
                        elif (previous_y + 1, previous_x - 1) in jumped:
                            return False
                        else:
                            jumped.append((previous_y + 1, previous_x - 1))
                    else:
                        return False
            else:
                return False
            
            #if move_sequence[i][0] == 0:
                #moved_piece.king()
            
    return True
        
# Executes the specified series of moves
# Assumes that the move_sequence has been verified
def execute(board, move_sequence):
    moved_piece_y, moved_piece_x = move_sequence[0]
    moved_piece = board[moved_piece_y][moved_piece_x]
    jumps = 0


    for i in range(1,len(move_sequence)):
        move_y, move_x = move_sequence[i]
        
        previous_y, previous_x = move_sequence[i-1]
        

        if moved_piece.get_color() == "black":
            #print(move_y)
            if (previous_y + 1) == move_y and ((previous_x + 1) == move_x or (previous_x - 1) == move_x):
                #board[move_y][move_x] = moved_piece
                board[moved_piece_y][moved_piece_x] = 1
                move_y = moved_piece_y
                move_x = moved_piece_x
            elif (previous_y + 2) == move_y and (previous_x + 2) == move_x:
                board[previous_y + 1][previous_x + 1] = 1
                #board[move_y][move_x] = moved_piece
                board[moved_piece_y][moved_piece_x] = 1
                move_y = moved_piece_y
                move_x = moved_piece_x
                jumps = jumps + 1
            elif (previous_y + 2) == move_y and (previous_x - 2) == move_x:
                board[previous_y + 1][previous_x - 1] = 1
                #board[move_y][move_x] = moved_piece
                board[moved_piece_y][moved_piece_x] = 1
                move_y = moved_piece_y
                move_x = moved_piece_x
                jumps = jumps + 1
            elif moved_piece.get_kinged():
                if (previous_y - 1) == move_y and ((previous_x + 1) == move_x or (previous_x - 1) == move_x):
                    #board[move_y][move_x] = moved_piece
                    board[moved_piece_y][moved_piece_x] = 1
                    move_y = moved_piece_y
                    move_x = moved_piece_x
                elif (previous_y - 2) == move_y and (previous_x + 2) == move_x:
                    board[previous_y - 1][previous_x + 1] = 1
                    #board[move_y][move_x] = moved_piece
                    board[moved_piece_y][moved_piece_x] = 1
                    move_y = moved_piece_y
                    move_x = moved_piece_x
                    jumps = jumps + 1
                elif (previous_y - 2) == move_y and (previous_x - 2) == move_x:
                    board[previous_y - 1][previous_x - 1] = 1
                    #board[move_y][move_x] = moved_piece
                    board[moved_piece_y][moved_piece_x] = 1
                    move_y = moved_piece_y
                    move_x = moved_piece_x
                    jumps = jumps + 1
            else:
                return False

            if move_sequence[i][0] == 7:
                moved_piece.king()

            
        elif moved_piece.get_color() == "red":
            if (previous_y - 1) == move_y and ((previous_x + 1) == move_x or (previous_x - 1) == move_x):
                #board[move_y][move_x] = moved_piece
                board[moved_piece_y][moved_piece_x] = 1
                move_y = moved_piece_y
                move_x = moved_piece_x
            elif (previous_y - 2) == move_y and (previous_x + 2) == move_x:
                board[previous_y - 1][previous_x + 1] = 1
                #board[move_y][move_x] = moved_piece
                board[moved_piece_y][moved_piece_x] = 1
                move_y = moved_piece_y
                move_x = moved_piece_x
                jumps = jumps + 1
            elif (previous_y - 2) == move_y and (previous_x - 2) == move_x:
                board[previous_y - 1][previous_x - 1] = 1
                #board[move_y][move_x] = moved_piece
                board[moved_piece_y][moved_piece_x] = 1
                move_y = moved_piece_y
                move_x = moved_piece_x
                jumps = jumps + 1
            elif moved_piece.get_kinged():
                if (previous_y + 1) == move_y and ((previous_x + 1) == move_x or (previous_x - 1) == move_x):
                    #board[move_y][move_x] = moved_piece
                    board[moved_piece_y][moved_piece_x] = 1
                    move_y = moved_piece_y
                    move_x = moved_piece_x
                elif (previous_y + 2) == move_y and (previous_x + 2) == move_x:
                    board[previous_y + 1][previous_x + 1] = 1
                    print(board[previous_y + 1][previous_x + 1])
                    #board[move_y][move_x] = moved_piece
                    board[moved_piece_y][moved_piece_x] = 1
                    move_y = moved_piece_y
                    move_x = moved_piece_x
                    jumps = jumps + 1
                elif (previous_y + 2) == move_y and (previous_x - 2) == move_x:
                    board[previous_y + 1][previous_x - 1] = 1
                    print(board[previous_y + 1][previous_x - 1])
                    #board[move_y][move_x] = moved_piece
                    board[moved_piece_y][moved_piece_x] = 1
                    move_y = moved_piece_y
                    move_x = moved_piece_x
                    jumps = jumps + 1
            
            if move_sequence[i][0] == 0:
                moved_piece.king()
    
    board[moved_piece_y][moved_piece_x] = 1
    dest_y, dest_x = move_sequence[-1]
    board[dest_y][dest_x] = moved_piece

    return jumps
