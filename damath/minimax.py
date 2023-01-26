import pygame
import operator
from .constants import ROWS, COLS, PLAYER_ONE, PLAYER_TWO
from options import *
from .piece import Piece

def copy_piece(piece: Piece):

    new_piece = Piece(piece.surface, (piece.col, piece.row), piece.color, piece.number)
    return new_piece

def copy_board(board: list):
    new_board = []
    
    for col in range(COLS):
        new_board.append([])
        for row in range(ROWS):
            new_piece = copy_piece(board[col][row])
            new_board[col].append(new_piece)

    return new_board

def update_board(board: list, piece: Piece, move: tuple):

    board = copy_board(board)
    board[move[0]][move[1]] = piece
    board[piece.col][piece.row] = Piece(piece.surface, piece.cell, 0, 0)
    piece.move(*move)
    
    return board

def board_evaluation(board: list, p1_score, p2_score):

    # print(f"{p1_score} {p2_score}")
    p1_eval, p2_eval = 0, 0
    for col in range(COLS):
        for row in range(ROWS):
            piece = board[col][row]
            if piece.color == PLAYER_ONE:
                p1_eval+=piece.number
            elif piece.color == PLAYER_TWO:
                p2_eval+=piece.number

    # if positive, PLAYER ONE is winning, otherwise PLAYER TWO 
    p1_eval += p1_score
    p2_eval += p2_score
    evaluation = p1_eval - p2_eval

    return evaluation

def add_score(game, piece: Piece, skip: list, move: tuple):

    result = 0
    operations = []

    OPERATOR_MAP = {'+' : operator.add,
                    '-' : operator.sub,
                    'x' : operator.mul,
                    '÷' : operator.truediv}

    # print(f"PIECE TO MOVE: {piece.color} {piece.number} to {move}")    

    for skipped_piece in skip:
        op = game.Board.piece_landed(*move)
        operations.append(op)
        # print(f"{piece.color} {piece.number} {op} {skipped_piece.color} {skipped_piece.number}")

    for skipped_piece, operation in zip(skip, operations):
        op = OPERATOR_MAP.get(operation)

        if operation == '÷' and float(skipped_piece.number) == 0:
            continue
        else:
            result += op(float(piece.number), float(skipped_piece.number))

            if piece.IsKing:
                if piece.IsOnPromotion:
                    piece.done_promote()
                else:
                    result *= 2

    # print(f"SCORE: {result}")
    return result

def minimax(game, board: list, depth, p1_score, p2_score, is_max: bool, best_move):
    
    # print(f"P1_SCORE P2_SCORE {p1_score} {p2_score}")

    if depth == 0:
        # print(best_move)
        # print(board_evaluation(board, p1_score, p2_score))
        return board_evaluation(board, p1_score, p2_score), best_move

    if is_max:
        turn = PLAYER_ONE
    else:
        turn = PLAYER_TWO

    # deep copy the 2D array representation of the board since
    # get_all_possible_moves() function only needs the list and not the object
    temp_board = copy_board(board)

    # get all the possible moves for the passed board
    all_valid_moves = game.get_all_possible_moves(temp_board, turn)

    if len(all_valid_moves.keys()) == 0:
        # print(board_evaluation(board, p1_score, p2_score))
        # print(best_move)
        return board_evaluation(board, p1_score, p2_score), best_move

    max_val = float('-inf')
    min_val = float('inf')

    # if there are valid moves for the player, try every single moves and 
    # call the function again to create more branches for the recursion tree
    for piece_to_move in all_valid_moves.keys():

         new_piece = copy_piece(piece_to_move)

         for raw_possible_moves in all_valid_moves.get(piece_to_move):

            # since the moves are raw cells, get its actual board cell first
            cell_possible_moves = game.Board.get_col_row(raw_possible_moves)

            # copy the piece and board first
            new_board = copy_board(temp_board)

            # update the temp_board and the piece's cell to simulate the move
            updated_board = update_board(new_board, new_piece, cell_possible_moves)

            if is_max: # if PLAYER_ONE's turn

                skip = all_valid_moves.get(piece_to_move).get(raw_possible_moves)

                if skip:
                    added_score = add_score(game, piece_to_move, skip, cell_possible_moves)
                    new_score = p1_score + added_score
                    board_eval = minimax(game, updated_board, depth - 1, new_score, p2_score, False, best_move)[0]
                else:
                    board_eval = minimax(game, updated_board, depth - 1, p1_score, p2_score, False, best_move)[0]
                
                    # print(f"{piece_to_move.number} {game.board.piece_landed(*cell_possible_moves)} {skip[0].number}")
                
                if board_eval > max_val:
                    max_val = board_eval
                    best_move = (new_piece, cell_possible_moves)
                    
            else:

                skip = all_valid_moves.get(piece_to_move).get(raw_possible_moves)

                if skip:
                    added_score = add_score(game, piece_to_move, skip, cell_possible_moves)
                    new_score = added_score + p2_score
                    board_eval = minimax(game, updated_board, depth - 1, p1_score, new_score, True, best_move)[0]
                    # print(f"{piece_to_move.number} {game.board.piece_landed(*cell_possible_moves)} {skip[0].number}")
                else:
                    board_eval = minimax(game, updated_board, depth - 1, p1_score, p2_score, True, best_move)[0]

                if board_eval < min_val:
                    min_val = board_eval
                    best_move = (new_piece, cell_possible_moves)

    if is_max:
        return max_val, best_move
    else:
        return min_val, best_move

            # print(f"Evaluated:{new_piece.number} {cell_possible_moves} {board_eval}")


    # print(f"{best_move[0].number, best_move[1]}")


