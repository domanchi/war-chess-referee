from .enum import ResultType
from .enum import Piece


class GameState:
    def __init__(self):
        self.previous_piece = None

    def process(self, piece: str) -> ResultType:
        """
        :raises: KeyError
        """
        try:
            rank = Piece.translate(piece)
        except KeyError:
            return ResultType.ERROR

        if self.previous_piece:
            result = compare_pieces(self.previous_piece, rank)
            self.previous_piece = None

            return result
        else:
            self.previous_piece = rank
            return ResultType.PENDING
    

def compare_pieces(pieceA: Piece, pieceB: Piece) -> ResultType:
    # First, check for victory.
    # NOTE: It doesn't make sense that both pieces are flags, because flags can't move.
    # Furthermore, since flags can only be defenders, we only have to check one way.
    if pieceB == Piece.FLAG:
        return ResultType.VICTORY

    # Same ranks kill each other.
    if pieceA == pieceB:
        return ResultType.BOTH_LOSE
    
    # Bombs blow everything up.
    if pieceA == Piece.BOMB or pieceB == Piece.BOMB:
        return ResultType.BOTH_LOSE
    
    # Only engineers know how to clear mines.
    # Otherwise, mines destroy anyone who touch it.
    # Also, mines don't move, so can only be defense.
    if pieceA == Piece.ENGINEER and pieceB == Piece.MINE:
        return ResultType.DEFENDER_LOSE
    if pieceB == Piece.MINE:
        return ResultType.BOTH_LOSE

    return (
        ResultType.DEFENDER_LOSE
        if pieceA.value > pieceB.value
        else ResultType.ATTACKER_LOSE
    )
