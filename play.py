from wordle import Wordle
import logging
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Play Wordle')
    parser.add_argument('--debug', action='store_true', default=False, help='turn ON debug messages')
    parser.add_argument('--hardmode', action='store_true', default=False, help='turn ON hard mode')

    args = parser.parse_args()
    if args.debug:
        logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.DEBUG)
    else:
        logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.INFO)

    gameState = Wordle(hardmode=args.hardmode, verbose=args.debug)
    gameState.randomTarget()
    print("Game Begins!")
    while not gameState.finished:
        word = input("Guess a word: ")
        gameState = gameState.step(word)
        print(gameState)
        gameState.getLegalMoves()
        # print(gameState.validWords)
        # print(gameState.greens)
        # print(gameState.yellows)
        # print(gameState.greys)
    print("Game finished!")
