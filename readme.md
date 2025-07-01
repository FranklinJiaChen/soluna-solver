# soluna-solver

Solves the combinatorial game [Soluna](https://boardgamegeek.com/boardgame/131199/soluna).

## Methodology

1. Represent the board using a 2d array containing the information about the stack size of each symbol.
2. Normalize the board to reduce the solution space.
3. Solve using Dynamic Programming.

##
I also used heuristics and the set cover problem to
minimize the optimal strategy game space.

My results matches with [JBra's claims on BoardGameGeeks](https://videogamegeek.com/blogpost/116793/solving-soluna)
on which player can force a win based on starting position.
