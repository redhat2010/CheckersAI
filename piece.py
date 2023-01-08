class Piece:
    
    # Initialize a Piece, with the specified color and as not kinged
    def __init__(self, color):
        self.color = color
        self.kinged = False
        self.tempKinged = False

    # King the piece
    def king(self):
        self.kinged = True

    # Sets the piece to king temporarily
    def setSelfKing(self, state):
        self.tempKinged = state

    # Get whether the piece is kinged
    def get_kinged(self):
        return self.kinged
    
    # Get the color of the piece
    def get_color(self):
        return self.color

    # Gets if the piece is temporarily kinged
    def get_temp_king(self):
        return self.tempKinged