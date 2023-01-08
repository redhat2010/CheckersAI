import mover
import piece

# Determines next move via a "worth" system. Each outcome has a different "worth" which determines how valuable that outcome is. It them picks the most valuable move
class worth_ai_1:

    # Initialize a worth_ai_1
    # Takes in a specified color (red or black) and a set of "worth" values in the order: capture enemy, get kinged, get captured.
    def __init__(self, color, worth_list):
        self.color = color
        self.cap_worth, self.king_worth, self.threat_worth = worth_list # cap_worth and king_worth assumed positive, threat_worth assumed negative

    # Returns the color of the AI
    def get_color(self):
        return self.color
    
    # Determines the next move for the team
    # Note: When determining the move(s) with the best "worth", if the best worth is ever less than -1000 the program will fail.
    def next_move(self, board):
        best_worth = -1000
        best_sequences = []


        # Handle Black
        if self.color == "black":
            for i in range(8):
                for j in range(8):
                    current_piece = board[i][j]
                    if current_piece != 0 and current_piece != 1:
                        if current_piece.get_color() == "black":
                            new_worth, new_sequences, caps = self.sim_captures(board, current_piece, [(i,j)], 0)
                            if new_worth > best_worth:
                                best_sequences = new_sequences
                                best_worth = new_worth
                            elif new_worth == best_worth and caps != 0:
                                best_sequences.append(new_sequences)


    # Calculates the worth of the specified move
    def calc_worth(self, board, sequence):
        worth = 0
        # Add worth based on captures
        if len(sequence) > 2:
            worth += (len(sequence) - 1) * self.cap_worth
        else: # If the sequence only has the start and end points, needs to check if it is capturing or simply moving
            diff = sequence[0][0] - sequence[1][0]
            if diff == 2 or diff == -2:
                worth += self.cap_worth
        
        # Handle black
        if self.color == "black":
            if sequence[-1][0] == 7:
                current_piece = board[sequence[0][0]][sequence[0][1]]
                if not current_piece.get_kinged():
                    worth += self.king_worth
        else:
            if sequence[-1][0] == 0:
                current_piece = board[sequence[0][0]][sequence[0][1]]
                if not current_piece.get_kinged():
                    worth += self.king_worth

        # Check if the piece would be threatened
        # Currently doesn't care how many captures it would get the enemey
        was_threatened = False
        end_point_y,end_point_x = sequence[-1]
        if end_point_y < 7 and end_point_y > 0:
            if end_point_x > 0 and end_point_x < 7:
                if board[end_point_y + 1][end_point_x - 1] != 1 and board[end_point_y - 1][end_point_x + 1] == 1 and board[end_point_y + 1][end_point_x - 1].get_color() == self.color :
                    was_threatened = True
                    worth += self.threat_worth
                elif board[end_point_y + 1][end_point_x + 1] != 1 and board[end_point_y - 1][end_point_x - 1] == 1 and board[end_point_y + 1][end_point_x + 1].get_color() == self.color :
                    was_threatened = True
                    worth += self.threat_worth
                elif board[end_point_y - 1][end_point_x - 1] != 1 and board[end_point_y + 1][end_point_x + 1] == 1 and board[end_point_y - 1][end_point_x - 1].get_color() == self.color and board[end_point_y - 1][end_point_x - 1].get_kinged():
                    was_threatened = True
                    worth += self.threat_worth
                 elif board[end_point_y - 1][end_point_x + 1] != 1 and board[end_point_y + 1][end_point_x - 1] == 1 and board[end_point_y - 1][end_point_x + 1].get_color() == self.color and board[end_point_y - 1][end_point_x - 1].get_kinged():
                    was_threatened = True
                    worth += self.threat_worth

        return worth

    # Simulates the capturing of enemy pieces
    # Returns the best "worth" and all capture sequences with that worth
    def sim_captures(self, board, piece, current_sequence, current_worth):
        best_worth = -1000
        best_sequences = []
        total_caps, new_sequences = self.capture_sequence(board, piece, current_sequence, 0, False)
        for sequence in new_sequences:
            new_worth = self.cap_worth * total_caps
        
        return False

    # [(curr_worth,sequence)]


    # Find sequence of captures for current piece
    # Same code as from basic_ai
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


    # Simulates the enemy to determine captures based on the possible move
    # Returns the change to the "worth" and sequence used to reach it
    def sim_enemy(self, board, piece, end, captures):
        return False


