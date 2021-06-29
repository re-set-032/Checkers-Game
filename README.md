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

Currently includes AI vs AI simulations for test purposes and Human vs AI mode for normal playing.
Three difficulty levels: Normal, Hard and BOSS_LVL (based on the depth of min-max tree)

## Controls

Control mechanism implemented for the human player in Human vs AI mode is briefly described below:
> 1. Normal checkers can move diagonally left or right towards the opposite side of the board.
> 2. Once selected, all possible moves from that checker will be highlighted as blue tiles as mentioned below.
> 3. Once selected, all possible moves from that checker will be highlighted as blue tiles as mentioned below.
> 4. If the player wishes to move other checker instead of the one that's selected, then the player has to unselect the selected checker before selecting that other checker.

<p align="center">
  <img width="300" height="300" src="https://user-images.githubusercontent.com/68694355/123746129-d72f5c80-d8ce-11eb-97ca-4b480c920e4f.PNG">
</p>

## Implementation

The game board initially contains 12 black checkers and 12 red checkers. By default, the red player will make the first move in both game modes, then black and this will continue till one of them wins. There are 4 different checker pieces (2 for each player- normal and king checker marked as N and K)

<p align="center">
  <img width="300" height="300" src="https://user-images.githubusercontent.com/68694355/123748709-304cbf80-d8d2-11eb-9299-3606cf5a7cc8.PNG">
</p>

The internal implementation uses two checker boards - internal board and the GUI checker board.
The changes in board state through game moves are first made in the internal board before updating the GUI board which gets updated after each move has been made internally.
For computing the next move, minimax algorithm (with αβ pruning) is used where black AI is the max player and the red AI is the min player. The depth
limit for black AI is based on the difficulty level selected from the start menu whereas the red AI has a fixed depth limit of 1. The scoring criteria for a game state is discussed in detail in the next section.

<p align="center">
  <img width="330" height="300" src="https://user-images.githubusercontent.com/68694355/123746459-4b6a0000-d8cf-11eb-9528-ddd72b370a4d.PNG">
</p>

## Heuristics used in scoring mechanism

Heuristics used - Tile + Distance + Count score
The heuristic score of any game state is defined as the cumulative summation of three different scores which are mentioned below:
- Tile Score : This scoring mechanism assigns each checker with a tile score on which it is located based on its distance from the center. The idea behind this is to prioritize defense (as checkers closer to the center will have higher probability of getting attacked by the opponent) while moving in order to increase your winning chance.

<p align="center">
  <img width="300" height="300" src="https://user-images.githubusercontent.com/68694355/123748390-c46a5700-d8d1-11eb-86e5-2aa81fcab3df.PNG">
</p>

> T<sub>score</sub>(Checker) = Chess board distance ofcenter tile (if present otherwise calculated considering the mid-point of the board) and the checker’s tile.

> T<sub>score</sub>(Player) =  Σ T<sub>score</sub>(Checker) ∀ Checker ∈ Player’s current set of checkers.

- Distance Score : This score is calculated based on the distance between checker and the opposite boundary at which kings are made once reached. Its main aim is to focus moving closer to the end if it's optimal from the current game state to become king as king pieces have higher value as it has larger attack and move capabilities.

> D<sub>score</sub>(Checker) = Distance between checker and the opposite end boundary

> D<sub>score</sub>(Player) = Σ D<sub>score</sub>(Checker) ∀Checker ∈ Player’s current set of checkers.

- Count Score : This score has the highest deciding factor in finding the optimum move from current game state as it calculates the difference between the pieces of the player and the opponent. As more opponent pieces are captured higher this score will become resulting in high count score which is reasonable since the main objective is to capture all the opponent’s pieces.

Notations 
> 1. nP<sub>N</sub> = Total player normal checkers
> 2. nP<sub>K</sub> = Total player king checkers
> 3. nO<sub>N</sub> = Total opponent normal checkers
> 4. nO<sub>K</sub> = Total opponent king checkers
> 5. N = Normal piece weight
> 6. K = King piece weight

> CScore(Player) = N(nP<sub>N</sub>- nO<sub>N</sub>)+ K(nP<sub>K</sub> - nO<sub>K</sub>)

The final score is the total sum of these individual
scores 
> Score (Player) = T<sub>score</sub> (Player) + D<sub>score</sub>(Player) + C<sub>score</sub>(Player)

In this game, black AI is the max player and red is the min player according to the minimax tree built for computing moves for each one of these AI’s from the current game state. And more specifically, the score that's mentioned below is used by black AI (the above one is the generalized one):

> Score (Black) = T<sub>score</sub> (Black) + D<sub>score</sub>(Black) + C<sub>score</sub>(Black)
