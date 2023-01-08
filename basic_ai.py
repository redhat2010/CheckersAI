import mover
import piece

# Counts the number of possible moves the specified color has
def move_count(board, color):
    moves = 0
    
    for i in range(8):
        for j in range(8):
            if board[i][j] != 0 and board[i][j] != 1:
                if board[i][j].get_color() == color:
                    if i != 7:
                        if j != 7:
                            trial1 = mover.validator(board, color, [(i,j),(i+1,j+1)])
                            if trial1:
                                moves = moves + 1
                        if j != 0:
                            trial2 = mover.validator(board, color, [(i,j),(i+1,j-1)])
                            if trial2:
                                moves = moves + 1
                    if i != 0:
                        if j != 7:
                            trial3 = mover.validator(board, color, [(i,j),(i-1,j+1)])
                            if trial3:
                                moves = moves + 1
                        if j != 0:
                            trial4 = mover.validator(board, color, [(i,j),(i-1,j-1)])
                            if trial4:
                                moves = moves + 1
                    if i < 6:
                        if j < 6:
                            trial5 = mover.validator(board, color, [(i,j),(i+2,j+2)])
                            if trial5:
                                moves = moves + 1
                        if j > 1:
                            trial6 = mover.validator(board, color, [(i,j),(i+2,j-2)])
                            if trial6:
                                moves = moves + 1
                    if i > 1:
                        if j < 6:
                            trial7 = mover.validator(board, color, [(i,j),(i-2,j+2)])
                            if trial7:
                                moves = moves + 1
                        if j > 1:
                            trial8 = mover.validator(board, color, [(i,j),(i-2,j-2)])
                            if trial8:
                                moves = moves + 1
    return moves


# Type 1 AI
# Chooses next move with following priority: Most captures, will king, any valid move
class AI_1:
    
    # Initialize an AI_1 for the specified color
    def __init__(self, color):
        self.color = color

    # Returns the color for the ai
    def get_color(self):
        return self.color

    # Finds and executes the next move
    # Chooses next move with following priority: Most captures, will king, any valid move
    def next_move(self, board):
        best_caps = 0
        best_sequences = []
        best_will_king = False

        # Handle Black
        if self.color == "black":
            moves = move_count(board, "black")
            
            for i in range(8):
                for j in range(8):
                    current_piece = board[i][j]
                    if current_piece != 0 and current_piece != 1:
                        if current_piece.get_color() == "black": # Makes sure the current piece is black
                            # Checks if the current piece can capture anything
                            new_caps, new_sequences = self.capture_sequence(board, current_piece, [(i,j)], 0)
                            # If the new move captures more pieces than the old move(s), then best_sequences changes to contain only the current sequence
                            if new_caps > best_caps:
                                best_sequences = new_sequences
                                best_caps = new_caps
                            # If the new sequence is as good as the best, it adds it to the sequence list
                            elif new_caps == best_caps and best_caps != 0:
                                for sequence in new_sequences:
                                    best_sequences.append(sequence)
                            elif new_caps == 0 and best_caps == 0:
                                # If the current piece cannot capture, it checks normal moves, starting with kinged pieces
                                if current_piece.get_kinged():
                                    if i > 0:
                                        if j > 0:
                                            if board[i-1][j-1] == 1:
                                                best_sequences.append([(i,j),(i-1,j-1)])
                                                #moves = moves - 1
                                        if j < 7:
                                            if board[i-1][j+1] == 1:
                                                best_sequences.append([(i,j),(i-1,j+1)])
                                                #moves = moves - 1
                                if i < 7:
                                    if j > 0:
                                        if board[i+1][j-1] == 1:
                                            if i == 6 and not current_piece.get_kinged():
                                                if best_will_king:
                                                    best_sequences.append([(i,j),(i+1,j-1)])
                                                    #moves = moves - 1
                                                else:
                                                    best_sequences = [[(i,j),(i+1,j-1)]]
                                                    best_will_king = True
                                            else:
                                                if not best_will_king:
                                                    best_sequences.append([(i,j),(i+1,j-1)])
                                                    #moves = moves - 1
                                    if j < 7:
                                        if board[i+1][j+1] == 1:
                                            if i == 6 and not current_piece.get_kinged():
                                                if best_will_king:
                                                    best_sequences.append([(i,j),(i+1,j+1)])
                                                    #moves = moves - 1
                                                else:
                                                    best_sequences = [[(i,j),(i+1,j+1)]]
                                                    best_will_king = True
                                            else:
                                                if not best_will_king:
                                                    best_sequences.append([(i,j),(i+1,j+1)])
                                                    #moves = moves - 1
            
        # Handle Red Piece
        else: 
            moves = move_count(board, "red")
            for i in range(8):
                for j in range(8):
                    current_piece = board[i][j]
                    if current_piece != 0 and current_piece != 1:
                        if current_piece.get_color() == "red":
                            new_caps, new_sequences = self.capture_sequence(board, current_piece, [(i,j)], 0)
                            if new_caps > best_caps:
                                best_sequences = new_sequences
                                best_caps = new_caps
                            elif new_caps == best_caps and best_caps != 0:
                                for sequence in new_sequences:
                                    best_sequences.append(sequence)
                            elif new_caps == 0 and best_caps == 0:
                                if current_piece.get_kinged():
                                    if i < 7:
                                        if j > 0:
                                            if board[i+1][j-1] == 1:
                                                best_sequences.append([(i,j),(i+1,j-1)])
                                                #moves = moves - 1
                                        if j < 7:
                                            if board[i+1][j+1] == 1:
                                                best_sequences.append([(i,j),(i+1,j+1)])
                                                #moves = moves - 1
                                if i > 0:
                                    if j > 0:
                                        if board[i-1][j-1] == 1:
                                            if i == 1 and not current_piece.get_kinged():
                                                if best_will_king:
                                                    best_sequences.append([(i,j),(i-1,j-1)])
                                                    #moves = moves - 1
                                                else:
                                                    best_sequences = [[(i,j),(i-1,j-1)]]
                                                    best_will_king = True
                                            else:
                                                if not best_will_king:
                                                    best_sequences.append([(i,j),(i-1,j-1)])
                                                    #moves = moves - 1
                                    if j < 7:
                                        if board[i-1][j+1] == 1:
                                            if i == 1 and not current_piece.get_kinged():
                                                if best_will_king:
                                                    best_sequences.append([(i,j),(i-1,j+1)])
                                                    #moves = moves - 1
                                                else:
                                                    best_sequences = [[(i,j),(i-1,j+1)]]
                                                    best_will_king = True
                                            else:
                                                if not best_will_king:
                                                    best_sequences.append([(i,j),(i-1,j+1)])
                                                    #moves = moves - 1
        return best_sequences


    # Find sequence of captures for current piece
    def capture_sequence(self, board, piece, current_sequence, current_caps):
        sequence = current_sequence.copy()
        best_sequences = []
        most_caps = current_caps
        current_y, current_x = sequence[-1]
        
        # Handle black piece
        if self.color == "black":
            if piece.get_kinged():
                if current_y > 1:
                    if current_x > 1:
                        if board[current_y-1][current_x-1] != 1 and board[current_y-2][current_x-2] == 1 and not (current_y - 2, current_x - 2) in sequence:
                            if board[current_y-1][current_x-1].get_color() == "red":
                                new_sequence = sequence.copy()
                                new_sequence.append((current_y-2,current_x-2))
                                new_board = board.copy()
                                new_caps, newer_sequences = self.capture_sequence(new_board, piece, new_sequence, most_caps)
                                if new_caps > most_caps:
                                    most_caps = new_caps
                                    best_sequences = newer_sequences
                                elif new_caps == most_caps:
                                    for seq in newer_sequences:
                                        best_sequences.append(seq)
                    if current_x < 6:
                        if board[current_y-1][current_x+1] != 1 and board[current_y-2][current_x+2] == 1 and not (current_y - 2, current_x - 2) in sequence:
                            if board[current_y-1][current_x+1].get_color() == "red":
                                new_sequence = sequence.copy()
                                new_sequence.append((current_y-2,current_x+2))
                                new_board = board.copy()
                                new_caps, newer_sequences = self.capture_sequence(new_board, piece, new_sequence, most_caps + 1)
                                if new_caps > most_caps:
                                    most_caps = new_caps
                                    best_sequences = newer_sequences
                                elif new_caps == most_caps:
                                    for seq in newer_sequences:
                                        best_sequences.append(seq)
            if current_y < 6:
                if current_x > 1:
                    if board[current_y+1][current_x-1] != 1 and board[current_y+2][current_x-2] == 1 and not (current_y + 2, current_x - 2) in sequence:
                        if board[current_y+1][current_x-1].get_color() == "red":
                            new_sequence = sequence.copy()
                            new_sequence.append((current_y+2,current_x-2))
                            new_board = board.copy()
                            new_caps, newer_sequences = self.capture_sequence(new_board, piece, new_sequence, most_caps + 1)
                            if new_caps > most_caps and len(newer_sequences) != 0:
                                most_caps = new_caps
                                best_sequences = newer_sequences
                            elif new_caps == most_caps and len(newer_sequences) != 0:
                                for seq in newer_sequences:
                                    best_sequences.append(seq)
                if current_x < 6:
                    if board[current_y+1][current_x+1] != 1 and board[current_y+2][current_x+2] == 1 and not (current_y + 2, current_x - 2) in sequence:
                        if board[current_y+1][current_x+1].get_color() == "red":
                            new_sequence = sequence.copy()
                            new_sequence.append((current_y+2,current_x+2))
                            new_board = board.copy()
                            new_caps, newer_sequences = self.capture_sequence(new_board, piece, new_sequence, most_caps + 1)
                            if new_caps > most_caps and len(newer_sequences) != 0:
                                most_caps = new_caps
                                best_sequences = newer_sequences
                            elif new_caps == most_caps and len(newer_sequences) != 0:
                                for seq in newer_sequences:
                                    best_sequences.append(seq)
        
        # Handle red piece
        else:
            if piece.get_kinged():
                if current_y < 6:
                    if current_x > 1:
                        if board[current_y+1][current_x-1] != 1 and board[current_y+2][current_x-2] == 1 and not (current_y + 2, current_x - 2) in sequence:
                            if board[current_y+1][current_x-1].get_color() == "black":
                                new_sequence = sequence.copy()
                                new_sequence.append((current_y+2,current_x-2))
                                new_board = board.copy()
                                new_caps, newer_sequences = self.capture_sequence(new_board, piece, new_sequence, most_caps)
                                if new_caps > most_caps:
                                    most_caps = new_caps
                                    best_sequences = newer_sequences
                                elif new_caps == most_caps:
                                    for seq in newer_sequences:
                                        best_sequences.append(seq)
                    if current_x < 6:
                        if board[current_y+1][current_x+1] != 1 and board[current_y+2][current_x+2] == 1 and not (current_y + 2, current_x - 2) in sequence:
                            if board[current_y+1][current_x+1].get_color() == "black":
                                new_sequence = sequence.copy()
                                new_sequence.append((current_y+2,current_x+2))
                                new_board = board.copy()
                                new_caps, newer_sequences = self.capture_sequence(new_board, piece, new_sequence, most_caps + 1)
                                if new_caps > most_caps:
                                    most_caps = new_caps
                                    best_sequences = newer_sequences
                                elif new_caps == most_caps:
                                    for seq in newer_sequences:
                                        best_sequences.append(seq)
            if current_y > 1:
                if current_x > 1:
                    if board[current_y-1][current_x-1] != 1 and board[current_y-2][current_x-2] == 1 and not (current_y - 2, current_x - 2) in sequence:
                        if board[current_y-1][current_x-1].get_color() == "black":
                            new_sequence = sequence.copy()
                            new_sequence.append((current_y-2,current_x-2))
                            new_board = board.copy()
                            new_caps, newer_sequences = self.capture_sequence(new_board, piece, new_sequence, most_caps + 1)
                            if new_caps > most_caps and len(newer_sequences) != 0:
                                most_caps = new_caps
                                best_sequences = newer_sequences
                            elif new_caps == most_caps and len(newer_sequences) != 0:
                                for seq in newer_sequences:
                                    best_sequences.append(seq)
                if current_x < 6:
                    if board[current_y-1][current_x+1] != 1 and board[current_y-2][current_x+2] == 1 and not (current_y - 2, current_x - 2) in sequence:
                        if board[current_y-1][current_x+1].get_color() == "black":
                            new_sequence = sequence.copy()
                            new_sequence.append((current_y-2,current_x+2))
                            new_board = board.copy()
                            new_caps, newer_sequences = self.capture_sequence(new_board, piece, new_sequence, most_caps + 1)
                            if new_caps > most_caps and len(newer_sequences) != 0:
                                most_caps = new_caps
                                best_sequences = newer_sequences
                            elif new_caps == most_caps and len(newer_sequences) != 0:
                                for seq in newer_sequences:
                                    best_sequences.append(seq)

        if len(best_sequences) == 0:
            best_sequences = [current_sequence]
        return (most_caps, best_sequences)




# Type 2 AI
# Chooses next move with following priority: Most captures, will king, aviod being captured, any valid move
class AI_2:
    
    # Initialize an AI_2 for the specified color
    def __init__(self, color):
        self.color = color

    # Returns the color for the ai
    def get_color(self):
        return self.color

    # Finds and executes the next move
    # Chooses next move with following priority: Most captures, will king, aviod being captured, any valid move
    def next_move(self, board):
        best_caps = 0
        best_sequences = []
        best_will_king = False
        best_will_threat = True

        # Handle Black
        if self.color == "black":
            moves = move_count(board, "black")
            
            for i in range(8):
                for j in range(8):
                    #print(best_will_threat)
                    current_piece = board[i][j]
                    if current_piece != 0 and current_piece != 1:
                        if current_piece.get_color() == "black":
                            new_caps, new_sequences = self.capture_sequence(board, current_piece, [(i,j)], 0, False)
                            if new_caps > best_caps:
                                best_sequences = new_sequences
                                best_caps = new_caps
                            elif new_caps == best_caps and best_caps != 0:
                                for sequence in new_sequences:
                                    best_sequences.append(sequence)
                            elif new_caps == 0 and best_caps == 0:
                                if current_piece.get_kinged():
                                    if i > 0:
                                        if j > 0:
                                            if board[i-1][j-1] == 1:
                                                will_threaten = self.check_threat(board, (i,j), (i-1,j-1))
                                                if best_will_threat:
                                                    if will_threaten:
                                                        best_sequences.append([(i,j),(i-1,j-1)])
                                                    else:
                                                        best_sequences = [[(i,j),(i-1,j-1)]]
                                                        best_will_threat = False
                                                        #print(here)
                                                else:
                                                    if not will_threaten:
                                                        best_sequences.append([(i,j),(i-1,j-1)])
                                                #moves = moves - 1
                                        if j < 7:
                                            if board[i-1][j+1] == 1:
                                                will_threaten = self.check_threat(board, (i,j), (i-1,j+1))
                                                if best_will_threat:
                                                    if will_threaten:
                                                        best_sequences.append([(i,j),(i-1,j+1)])
                                                    else:
                                                        best_sequences = [[(i,j),(i-1,j+1)]]
                                                        best_will_threat = False
                                                        #print(here)
                                                else:
                                                    if not will_threaten:
                                                        
                                                        best_sequences.append([(i,j),(i-1,j+1)])
                                                #moves = moves - 1
                                if i < 7:
                                    if j > 0:
                                        if board[i+1][j-1] == 1:
                                            if i == 6:
                                                if best_will_king:
                                                    best_sequences.append([(i,j),(i+1,j-1)])
                                                    #moves = moves - 1
                                                else:
                                                    best_sequences = [[(i,j),(i+1,j-1)]]
                                                    best_will_king = True
                                            else:
                                                if not best_will_king:
                                                    will_threaten = self.check_threat(board, (i,j), (i+1,j-1))
                                                    print(best_will_threat)
                                                    print(will_threaten)
                                                    print()
                                                    if best_will_threat:
                                                        if will_threaten:
                                                            best_sequences.append([(i,j),(i+1,j-1)])
                                                        else:
                                                            best_sequences = [[(i,j),(i+1,j-1)]]
                                                            best_will_threat = False
                                                            print("here")
                                                    else:
                                                        if not will_threaten:
                                                            #print(will_threaten)
                                                            best_sequences.append([(i,j),(i+1,j-1)])
                                                        else:
                                                            print("rejected")
                                                    #moves = moves - 1
                                    if j < 7:
                                        if board[i+1][j+1] == 1:
                                            if i == 6:
                                                if best_will_king:
                                                    best_sequences.append([(i,j),(i+1,j+1)])
                                                    #moves = moves - 1
                                                else:
                                                    best_sequences = [[(i,j),(i+1,j+1)]]
                                                    best_will_king = True
                                            else:
                                                if not best_will_king:
                                                    will_threaten = self.check_threat(board, (i,j), (i+1,j+1))
                                                    print(best_will_threat)
                                                    print(will_threaten)
                                                    print()
                                                    if best_will_threat:
                                                        if will_threaten:
                                                            best_sequences.append([(i,j),(i+1,j+1)])
                                                        else:
                                                            best_sequences = [[(i,j),(i+1,j+1)]]
                                                            best_will_threat = False
                                                            print("here")
                                                    else:
                                                        if not will_threaten:
                                                            #print(will_threaten)
                                                            best_sequences.append([(i,j),(i+1,j+1)])
                                                        else:
                                                            print("rejected")
                                                    #moves = moves - 1
            
        # Handle Red Piece
        else: 
            moves = move_count(board, "red")
            for i in range(8):
                for j in range(8):
                    current_piece = board[i][j]
                    if current_piece != 0 and current_piece != 1:
                        if current_piece.get_color() == "red":
                            new_caps, new_sequences = self.capture_sequence(board, current_piece, [(i,j)], 0, False)
                            if new_caps > best_caps:
                                best_sequences = new_sequences
                                best_caps = new_caps
                            elif new_caps == best_caps and best_caps != 0:
                                for sequence in new_sequences:
                                    best_sequences.append(sequence)
                            elif new_caps == 0 and best_caps == 0:
                                if current_piece.get_kinged():
                                    if i < 7:
                                        if j > 0:
                                            if board[i+1][j-1] == 1:
                                                will_threaten = self.check_threat(board, (i,j), (i+1,j-1))
                                                if best_will_threat:
                                                    if will_threaten:
                                                        best_sequences.append([(i,j),(i+1,j-1)])
                                                    else:
                                                        best_sequences = [[(i,j),(i+1,j-1)]]
                                                        best_will_threat = False
                                                else:
                                                    if not will_threaten:
                                                        best_sequences.append([(i,j),(i+1,j-1)])
                                               #moves = moves - 1
                                        if j < 7:
                                            if board[i+1][j+1] == 1:
                                                will_threaten = self.check_threat(board, (i,j), (i+1,j+1))
                                                if best_will_threat:
                                                    if will_threaten:
                                                        best_sequences.append([(i,j),(i+1,j+1)])
                                                    else:
                                                        best_sequences = [[(i,j),(i+1,j+1)]]
                                                        best_will_threat = False
                                                        #print(here)
                                                else:
                                                    if not will_threaten:
                                                        best_sequences.append([(i,j),(i+1,j+1)])
                                                #moves = moves - 1
                                if i > 0:
                                    if j > 0:
                                        if board[i-1][j-1] == 1:
                                            if i == 1:
                                                if best_will_king:
                                                    best_sequences.append([(i,j),(i-1,j-1)])
                                                    #moves = moves - 1
                                                else:
                                                    best_sequences = [[(i,j),(i-1,j-1)]]
                                                    best_will_king = True
                                            else:
                                                #will_threaten = self.check_threat(board, (i-1,j-1))
                                                if not best_will_king:
                                                    will_threaten = self.check_threat(board, (i,j), (i-1,j-1))
                                                    print(best_will_threat)
                                                    if best_will_threat:
                                                        if will_threaten:
                                                            best_sequences.append([(i,j),(i-1,j-1)])
                                                        else:
                                                            best_sequences = [[(i,j),(i-1,j-1)]]
                                                            best_will_threat = False
                                                            print(will_threaten)
                                                    else:
                                                        if not will_threaten:
                                                            best_sequences.append([(i,j),(i-1,j-1)])
                                                    #moves = moves - 1
                                    if j < 7:
                                        if board[i-1][j+1] == 1:
                                            if i == 1:
                                                if best_will_king:
                                                    best_sequences.append([(i,j),(i-1,j+1)])
                                                    #moves = moves - 1
                                                else:
                                                    best_sequences = [[(i,j),(i-1,j+1)]]
                                                    best_will_king = True
                                            else:
                                                #will_threaten = self.check_threat(board, (i-1,j+1))
                                                if not best_will_king:
                                                    will_threaten = self.check_threat(board, (i,j), (i-1,j+1))
                                                    if best_will_threat:
                                                        if will_threaten:
                                                            best_sequences.append([(i,j),(i-1,j+1)])
                                                        else:
                                                            best_sequences = [[(i,j),(i-1,j+1)]]
                                                            best_will_threat = False
                                                            print(will_threaten)
                                                    else:
                                                        if not will_threaten:
                                                            best_sequences.append([(i,j),(i-1,j+1)])
                                                    #moves = moves - 1
        
        print("")
        print("")
        return best_sequences


    # Find sequence of captures for current piece
    def capture_sequence(self, board, piece, current_sequence, current_caps, has_kinged):
        sequence = current_sequence.copy()
        best_sequences = []
        most_caps = current_caps
        current_y, current_x = sequence[-1]
        print("Current Sequence " + str(sequence))
        print("Y " + str(current_y))
        # Handle black piece
        if self.color == "black":
            if current_y == 7:
                has_kinged = True
            if piece.get_kinged() or has_kinged:
                print("using king")
                if current_y > 1:
                    if current_x > 1:
                        #print("Sequence check: " + str((current_y - 2, current_x - 2) in sequence))
                        if board[current_y-1][current_x-1] != 1 and board[current_y-2][current_x-2] == 1 and not (current_y - 2, current_x - 2) in sequence:
                            if board[current_y-1][current_x-1].get_color() == "red":
                                new_sequence = sequence.copy()
                                new_sequence.append((current_y-2,current_x-2))
                                new_board = board.copy()
                                new_caps, newer_sequences = self.capture_sequence(new_board, piece, new_sequence, most_caps + 1, has_kinged)
                                if new_caps > most_caps:
                                    most_caps = new_caps
                                    best_sequences = newer_sequences
                                elif new_caps == most_caps:
                                    for seq in newer_sequences:
                                        best_sequences.append(seq)
                    if current_x < 6:
                        #print("Sequence check: " + str((current_y - 2, current_x + 2) in sequence))
                        if board[current_y-1][current_x+1] != 1 and board[current_y-2][current_x+2] == 1 and not (current_y - 2, current_x + 2) in sequence:
                            if board[current_y-1][current_x+1].get_color() == "red":
                                new_sequence = sequence.copy()
                                new_sequence.append((current_y-2,current_x+2))
                                new_board = board.copy()
                                new_caps, newer_sequences = self.capture_sequence(new_board, piece, new_sequence, most_caps + 1, has_kinged)
                                if new_caps > most_caps:
                                    most_caps = new_caps
                                    best_sequences = newer_sequences
                                elif new_caps == most_caps:
                                    for seq in newer_sequences:
                                        best_sequences.append(seq)
            if current_y < 6:
                if current_x > 1:
                    if board[current_y+1][current_x-1] != 1 and board[current_y+2][current_x-2] == 1 and not (current_y + 2, current_x - 2) in sequence:
                        if board[current_y+1][current_x-1].get_color() == "red":
                            new_sequence = sequence.copy()
                            new_sequence.append((current_y+2,current_x-2))
                            new_board = board.copy()
                            new_caps, newer_sequences = self.capture_sequence(new_board, piece, new_sequence, most_caps + 1, has_kinged)
                            if new_caps > most_caps and len(newer_sequences) != 0:
                                most_caps = new_caps
                                best_sequences = newer_sequences
                            elif new_caps == most_caps and len(newer_sequences) != 0:
                                for seq in newer_sequences:
                                    best_sequences.append(seq)
                if current_x < 6:
                    if board[current_y+1][current_x+1] != 1 and board[current_y+2][current_x+2] == 1 and not (current_y + 2, current_x + 2) in sequence:
                        if board[current_y+1][current_x+1].get_color() == "red":
                            new_sequence = sequence.copy()
                            new_sequence.append((current_y+2,current_x+2))
                            new_board = board.copy()
                            new_caps, newer_sequences = self.capture_sequence(new_board, piece, new_sequence, most_caps + 1, has_kinged)
                            if new_caps > most_caps and len(newer_sequences) != 0:
                                most_caps = new_caps
                                best_sequences = newer_sequences
                            elif new_caps == most_caps and len(newer_sequences) != 0:
                                for seq in newer_sequences:
                                    best_sequences.append(seq)
        
        # Handle red piece
        else:
            if current_y == 0:
                has_kinged = True
            if piece.get_kinged() or has_kinged:
                if current_y < 6:
                    if current_x > 1:
                        if board[current_y+1][current_x-1] != 1 and board[current_y+2][current_x-2] == 1 and not (current_y + 2, current_x - 2) in sequence:
                            if board[current_y+1][current_x-1].get_color() == "black":
                                new_sequence = sequence.copy()
                                new_sequence.append((current_y+2,current_x-2))
                                new_board = board.copy()
                                new_caps, newer_sequences = self.capture_sequence(new_board, piece, new_sequence, most_caps + 1, has_kinged)
                                if new_caps > most_caps:
                                    most_caps = new_caps
                                    best_sequences = newer_sequences
                                elif new_caps == most_caps:
                                    for seq in newer_sequences:
                                        best_sequences.append(seq)
                    if current_x < 6:
                        if board[current_y+1][current_x+1] != 1 and board[current_y+2][current_x+2] == 1 and not (current_y + 2, current_x + 2) in sequence:
                            if board[current_y+1][current_x+1].get_color() == "black":
                                new_sequence = sequence.copy()
                                new_sequence.append((current_y+2,current_x+2))
                                new_board = board.copy()
                                new_caps, newer_sequences = self.capture_sequence(new_board, piece, new_sequence, most_caps + 1, has_kinged)
                                if new_caps > most_caps:
                                    most_caps = new_caps
                                    best_sequences = newer_sequences
                                elif new_caps == most_caps:
                                    for seq in newer_sequences:
                                        best_sequences.append(seq)
            if current_y > 1:
                if current_x > 1:
                    if board[current_y-1][current_x-1] != 1 and board[current_y-2][current_x-2] == 1 and not (current_y - 2, current_x - 2) in sequence:
                        if board[current_y-1][current_x-1].get_color() == "black":
                            new_sequence = sequence.copy()
                            new_sequence.append((current_y-2,current_x-2))
                            new_board = board.copy()
                            new_caps, newer_sequences = self.capture_sequence(new_board, piece, new_sequence, most_caps + 1, has_kinged)
                            if new_caps > most_caps and len(newer_sequences) != 0:
                                most_caps = new_caps
                                best_sequences = newer_sequences
                            elif new_caps == most_caps and len(newer_sequences) != 0:
                                for seq in newer_sequences:
                                    best_sequences.append(seq)
                if current_x < 6:
                    if board[current_y-1][current_x+1] != 1 and board[current_y-2][current_x+2] == 1 and not (current_y - 2, current_x + 2) in sequence:
                        if board[current_y-1][current_x+1].get_color() == "black":
                            new_sequence = sequence.copy()
                            new_sequence.append((current_y-2,current_x+2))
                            new_board = board.copy()
                            new_caps, newer_sequences = self.capture_sequence(new_board, piece, new_sequence, most_caps + 1, has_kinged)
                            if new_caps > most_caps and len(newer_sequences) != 0:
                                most_caps = new_caps
                                best_sequences = newer_sequences
                            elif new_caps == most_caps and len(newer_sequences) != 0:
                                for seq in newer_sequences:
                                    best_sequences.append(seq)

        if len(best_sequences) == 0:
            best_sequences = [current_sequence]
        return (most_caps, best_sequences)

    # Check if the piece is going to be threatened
    def check_threat(self, board, current, dest):
        i,j = dest

        print(dest)
        # Handle Black
        if self.color == "black":
            if i > 0 and i < 7:
                if j > 0 and j < 7:
                    print("here3")
                    if board[i+1][j+1] != 1 and (board[i-1][j-1] == 1 or (i-1,j-1) == current):
                        print("here2")
                        if board[i+1][j+1].get_color() == "red":
                            return True
                    if board[i+1][j-1] != 1 and (board[i-1][j+1] == 1 or (i-1,j+1) == current):
                        print("here2")
                        if board[i+1][j-1].get_color() == "red":
                            return True
                    if board[i-1][j+1] != 1 and (board[i+1][j-1] == 1 or (i+1,j-1) == current):
                        if board[i-1][j+1].get_color() == "red" and board[i-1][j+1].get_kinged():
                            return True
                    if board[i-1][j-1] != 1 and (board[i+1][j+1] == 1 or (i+1,j+1) == current):
                        if board[i-1][j-1].get_color() == "red"and board[i-1][j-1].get_kinged():
                            return True
        
        # Handle Red
        else:
            if i > 0 and i < 7:
                if j > 0 and j < 7:
                    if board[i-1][j+1] != 1 and (board[i+1][j-1] == 1 or (i+1,j-1) == current):
                        if board[i-1][j+1].get_color() == "black":
                            return True
                    if board[i-1][j-1] != 1 and (board[i+1][j+1] == 1 or (i+1,j+1) == current):
                        if board[i-1][j-1].get_color() == "black":
                            return True
                    if board[i+1][j+1] != 1 and (board[i-1][j-1] == 1 or (i-1,j-1) == current):
                        if board[i+1][j+1].get_color() == "black" and board[i+1][j+1].get_kinged():
                            return True
                    if board[i+1][j-1] != 1 and (board[i-1][j+1] == 1 or (i-1,j+1) == current):
                        if board[i+1][j-1].get_color() == "black"and board[i+1][j-1].get_kinged():
                            return True
        
        return False





