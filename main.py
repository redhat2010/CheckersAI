import pygame
import piece
import mover
import win_handle
import basic_ai
import random
import time



pygame.init()
pygame.display.init()

# Initilize the display
gameDisplay = pygame.display.set_mode((1000, 800))

# Load the board image and display it
board_img = pygame.image.load("images/board.png")
gameDisplay.blit(board_img, (0,0))

# Load the piece images
black_piece = pygame.image.load("images/black_piece.png")
black_king = pygame.image.load("images/black_king.png")
red_piece = pygame.image.load("images/red_piece.png")
red_king = pygame.image.load("images/red_king.png")

# Load additional images
select = pygame.image.load("images/select.png")
sidebar = pygame.image.load("images/sidebar.png")
confirm = pygame.image.load("images/confirm.png")
cancel = pygame.image.load("images/cancel.png")
blank_space = pygame.image.load("images/blank_space.png")

x = 0

# Generates the board and then populates it
# 0 indicates a space where pieces cannot be, 1 indicates a space where a piece can be but isn't
board = [[0 for i in range(8)] for j in range(8)]

for i in range(8):
    if (i % 2) == 0:
        for j in range(1,8,2):
            if i < 3:
                board[i][j] = piece.Piece("black")
            elif i > 4:
                board[i][j] = piece.Piece("red")
            else:
                board[i][j] = 1
    else:
        for j in range(0,8,2):
            if i < 3:
                board[i][j] = piece.Piece("black")
            elif i > 4:
                board[i][j] = piece.Piece("red")
            else:
                board[i][j] = 1

mouse1 = False
mouse2 = False
mouse3 = False

black_count = 12
red_count = 12

# Sets up the AI for the colors
black_has_ai = False
black_ai = basic_ai.AI_2("black")

red_has_ai = False
red_ai = basic_ai.AI_2("red")

#board[6][1] = piece.Piece("black")
#board[2][5] = piece.Piece("red")

moves = basic_ai.move_count(board, "black")

#print(moves)

turn = "red"

selections = []

# Runs the actual game
while x == 0:
    
    gameDisplay.blit(board_img, (0,0))
    gameDisplay.blit(sidebar, (800,0))
    
    # Displays an icon on the right to indicate the current turn
    if turn == "red":
        gameDisplay.blit(red_piece, (850, 135))
    else:
        gameDisplay.blit(black_piece, (850, 135))

    # Displays "confirm" and "cancel" buttons for making a move
    if len(selections) != 0:
        gameDisplay.blit(confirm, (800, 450))
        gameDisplay.blit(cancel, (800, 550))
        for select_pos in selections:
            gameDisplay.blit(select, (select_pos[1] * 100, select_pos[0] * 100))
    
    # Displays the game pieces
    for i in range(8):
        for j in range(8):
            if board[i][j] != 0 and board[i][j] != 1:
                if board[i][j].get_color() == "black":
                    if board[i][j].get_kinged() == False:
                        gameDisplay.blit(black_piece,(j * 100, i * 100))
                    else:
                        gameDisplay.blit(black_king,(j * 100, i * 100))
                else:
                    if board[i][j].get_kinged() == False:
                        gameDisplay.blit(red_piece,(j * 100, i * 100))
                    else:
                        gameDisplay.blit(red_king,(j * 100, i * 100))
    
    pygame.display.update()
    
    
    # Handles the AI choosing a move
    if turn == "red" and red_has_ai: # Red AI
        time.sleep(1)
        possible_moves = red_ai.next_move(board)
        move_choice = random.randrange(len(possible_moves))
        #print(possible_moves)
        
        
        # Displays multi-piece jumps in a stagered manner
        was_kinged = board[possible_moves[move_choice][0][0]][possible_moves[move_choice][0][1]].get_kinged()
        for index in range(len(possible_moves[move_choice])):
            if index != 0:
                i,j = possible_moves[move_choice][index]
                i_prev,j_prev = possible_moves[move_choice][index - 1]
                gameDisplay.blit(blank_space,(j_prev * 100, i_prev * 100))
                i_diff = i - i_prev
                j_diff = j - j_prev
                if i_diff == 2 or i_diff == -2:
                    gameDisplay.blit(blank_space,((j_prev + j_diff/2) * 100, (i_prev + i_diff/2) * 100))
                if i == 0:
                    was_kinged = True
                if was_kinged:
                    gameDisplay.blit(red_king,(j * 100, i * 100))
                else:
                    gameDisplay.blit(red_piece,(j * 100, i * 100))
                pygame.display.update()
                if index != len(possible_moves[move_choice]) - 1:
                    time.sleep(0.5)
        mover.execute(board, possible_moves[move_choice])
        #print(possible_moves[move_choice])
        turn = "black"
    elif turn == "black" and black_has_ai: # Black AI
        time.sleep(1)
        possible_moves = black_ai.next_move(board)
        move_choice = random.randrange(len(possible_moves))
        #print(possible_moves)
        
        #print("Was kinged: " + str(was_kinged))
        # Displays multi-piece jumps in a stagered manner
        was_kinged = board[possible_moves[move_choice][0][0]][possible_moves[move_choice][0][1]].get_kinged()
        for index in range(len(possible_moves[move_choice])):
            if index != 0:
                i,j = possible_moves[move_choice][index]
                i_prev,j_prev = possible_moves[move_choice][index - 1]
                gameDisplay.blit(blank_space,(j_prev * 100, i_prev * 100))
                i_diff = i - i_prev
                j_diff = j - j_prev
                if i_diff == 2 or i_diff == -2:
                    gameDisplay.blit(blank_space,((j_prev + j_diff/2) * 100, (i_prev + i_diff/2) * 100))
                if i == 7:
                    was_kinged = True
                if was_kinged:
                    gameDisplay.blit(black_king,(j * 100, i * 100))
                else:
                    gameDisplay.blit(black_piece,(j * 100, i * 100))
                pygame.display.update()
                if index != len(possible_moves[move_choice]) - 1:
                    time.sleep(0.5)
        mover.execute(board, possible_moves[move_choice])
        print(possible_moves[move_choice])
        turn = "red"

    # Checks for user input
    for event in pygame.event.get():
        # Pressing "space" ends the game
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                pygame.quit()
                x = 1
            if event.key == pygame.K_LSHIFT:
                if black_has_ai:
                    black_has_ai = False
                else:
                    black_has_ai = True
            if event.key == pygame.K_RSHIFT:
                if red_has_ai:
                    red_has_ai = False
                else:
                    red_has_ai = True
        elif event.type == pygame.QUIT:
            pygame.quit()
            x = 1
        # Handles mouse input
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse1, mouse2, mouse3 = pygame.mouse.get_pressed()
            if mouse1:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if mouse_x <= 800:
                    selections.append(((mouse_y // 100), (mouse_x // 100)))
                    print((mouse_y // 100), (mouse_x // 100))
                else:
                    if len(selections) != 0:
                        if mouse_y >= 490 and mouse_y <= 547:
                            result = mover.validator(board, turn, selections)
                            if result:
                                # Displays multi-piece jumps in a stagered manner
                                was_kinged = board[selections[0][0]][selections[0][1]].get_kinged()
                                for index in range(len(selections)):
                                    i,j = selections[index]
                                    gameDisplay.blit(blank_space,(j * 100, i * 100))
                                for index in range(len(selections)):
                                    if index != 0:
                                        i,j = selections[index]
                                        i_prev,j_prev = selections[index - 1]
                                        gameDisplay.blit(blank_space,(j_prev * 100, i_prev * 100))
                                        i_diff = i - i_prev
                                        j_diff = j - j_prev
                                        if i_diff == 2 or i_diff == -2:
                                            gameDisplay.blit(blank_space,((j_prev + j_diff/2) * 100, (i_prev + i_diff/2) * 100))
                                        if i == 7:
                                            was_kinged = True
                                        if was_kinged:
                                            if turn == "black":
                                                gameDisplay.blit(black_king,(j * 100, i * 100))
                                            else:
                                                gameDisplay.blit(red_king,(j * 100, i * 100))
                                        else:
                                            if turn == "black":
                                                gameDisplay.blit(black_piece,(j * 100, i * 100))
                                            else:
                                                gameDisplay.blit(red_piece,(j * 100, i * 100))
                                        pygame.display.update()
                                        if index != len(selections) - 1:
                                            time.sleep(0.5)

                                jump_count = mover.execute(board, selections)
                                if turn == "red":
                                    black_count = black_count - jump_count
                                    turn = "black"
                                else:
                                    red_count = red_count - jump_count
                                    turn = "red"
                                state = win_handle.loss_check(board, (red_count, black_count))
                                if state == "RED":
                                    print("Black won")
                                    pygame.quit()
                                elif state == "BLACK":
                                    print("Red won")
                                    pygame.quit()
                                elif state == "DRAW":
                                    print("Draw")
                                    pygame.quit()
                            else:
                                print("Invalid")
                            selections = []
                        elif mouse_y >= 590 and mouse_y <= 647:
                            selections = []  
    
    # Handle Winning
    


print("Done")