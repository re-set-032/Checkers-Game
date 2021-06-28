# Checkers game
Author- ronin117-prog

Language - Python + Tkinter(for GUI)

## Version - 1.0 (Stable alpha release)

Checkers game implemented using game-trees and the heuristics used in computing the end results scoring mechanism for determining the next most optimal move based on the current game state along with the other game components and rules followed while playing the game of checkers.

Checkers is a strategic board game played among two players where the main objective for any player is to capture all the opponent’s checkers in order to win though there are other ways of winning the game as well which will be discussed in detail in the rules section.

## Rules

Rules considered of this game simulation are pretty standard and straight forward which are mentioned below:
> 1. Normal checkers can move diagonally left or right towards the opposite side of the board.
> 2. When a normal checker reaches the end of the board it becomes a king piece.
> 3. Both normal and king piece can capture as many enemy pieces in one move using the same attacking piece by jumping over it. A piece can’t jump over a piece of its own kind.
> 4. If attacking is possible then it has to happen. The player has to make one such attack move.
> 5. King pieces can move/attack along both forward and backward diagonals whereas the normal checkers can move/attack towards the opposite end direction only.
> 6. A player wins if he/she captures all enemy pieces/checkers i.e. when no enemy piece is left on board.
> 7. Also, even if a player has pieces on board but cant make a move on his/her turn (if all pieces ofthe player are blocked by enemy ones) then the opponent is declared a winner.

Currently Supports AI vs AI simulations and Human vs AI mode for normal playing.
Three difficulty levels added : Normal, Hard and BOSS_LVL

Heuristics used - Tile + Distance + Count score 
