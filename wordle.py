import csv
import random
from copy import deepcopy
from typing import List
import logging

class Wordle:
    """
    Game Engine for the recently popular game - Wordle
    """

    def __init__(self, wordListFile='Eldrow Wordlist - Sheet1.csv',
                 verbose=False, hardmode=True):
        # game
        self.targetWord = None
        self.colours = ["W"] * 5
        self.loadWordList(wordListFile)
        self.guesses = []
        self.finished = False

        # helper variables
        self.greens = [''] * 5
        self.yellows = [[], [], [], [], []]
        self.greys = {}

        # game settings
        self.verbose = verbose
        self.hardmode = hardmode

    # setup
    def loadWordList(self, f: str) -> None:
        out = csv.reader(open(f, 'r'))
        self.WORDLIST = [line[0] for line in out]
        self.validWords = self.WORDLIST

    def randomTarget(self) -> None:
        self.targetWord = random.choice(self.WORDLIST)
        self._setTargetD()

    def setTarget(self, targetWord: str):
        targetWord = targetWord.upper()
        assert targetWord in self.WORDLIST, "Word not in word list"
        self.targetWord = targetWord
        self._setTargetD()

    def _setTargetD(self):
        self.targetWordD = {}
        for i, c in enumerate(self.targetWord):
            if c not in self.targetWordD.keys():
                self.targetWordD[c] = [i]
            else:
                self.targetWordD[c].append(i)

    # game
    def step(self, guessWord: str):
        guessWord = guessWord.upper()
        nextGamestate = self._guess(guessWord)
        # if error occurs
        if nextGamestate is None:
            raise ValueError
            return self
        if (not nextGamestate.finished) and self.hardmode:
            nextGamestate._getValidWords()
        return nextGamestate

    def getLegalMoves(self) -> List[str]:
        return self.validWords

    # helper functions
    def _guess(self, guessWord: str):
        if guessWord not in self.validWords:
            logging.info("Invalid word. Try again!")
            logging.debug(f"{guessWord} is not in {self.validWords}")
            print("NOT VALID!")
            self._isValidWord(guessWord, debug=True)
            return
        nextGameState = deepcopy(self)
        assert guessWord not in nextGameState.guesses, "Guessed the same word twice"
        nextGameState.guesses.append(guessWord)

        if (guessWord == nextGameState.targetWord):
            if self.verbose:
                logging.info("Game finished!")
            nextGameState.finished = True
            for i in range(5):
                nextGameState.colours[i] = "G"
            nextGameState.validWords = []
            return nextGameState

        for i in range(5):
            # marked for green firsts
            if guessWord[i] == nextGameState.targetWord[i]:
                nextGameState.colours[i] = "G"
                nextGameState.greens[i] = guessWord[i]
                continue
            # marked yellow or grey
            nextGameState.colours[i] = "X"
            if nextGameState._isYellow(guessWord, i):
                nextGameState.colours[i] = "Y"
                nextGameState.yellows[i].append(guessWord[i])
            else:
                nextGameState.colours[i] = "X"

        for i in range(5):
            if nextGameState.colours[i] == "X":
                none_grey_count = 0
                for j in range(5):
                    if nextGameState.targetWord[j] == guessWord[i] and \
                        (nextGameState.targetWord[j] != 'X'):
                        none_grey_count += 1
                nextGameState.greys[guessWord[i]] = none_grey_count

        return nextGameState

    def _isYellow(self, guessWord, idx):
        logging.debug(f'\nidx: {idx}')
        c = guessWord[idx]
        logging.debug(c)
        if c not in self.targetWordD.keys():
            return False
        total_yellows = 0
        # take away all the greens
        for i in range(5):
            if guessWord[i] != self.targetWord[i] and self.targetWord[i] == c:
                total_yellows += 1
        logging.debug(f'total yellows: {total_yellows}')
        # total yellows
        j = 0
        while (j < idx):
            logging.debug(f"Checking 1: {self.targetWord[j]} == {c}")
            logging.debug(f"Checking 2: {self.colours[j]} == 'Y'")
            if self.colours[j] == "Y" and guessWord[j] == c:
                total_yellows -= 1
            j += 1
        logging.debug(f'total_yellows: {total_yellows}')
        return total_yellows > 0

    def _getValidWords(self) -> None:
        validWords = []
        for word in self.validWords:
            if self._isValidWord(word):
                validWords.append(word)

        for guess in self.guesses:
            if guess in validWords:
                validWords.remove(guess)

        self.validWords = validWords

    def _isValidWord(self, word, debug=False):
        if debug:
            print("target word:", self.targetWord)
            print("guess word:", word)

        for idx, char in enumerate(word):
            if debug:
                print(f"Checking guess_char {char} vs target_char {self.targetWord[idx]}")
            # condition: green letter must be used again
            if self.greens[idx] != '' and char != self.greens[idx]:
                if debug:
                    print("Failed -> green letter must be used again")
                return False
            # condition: yellow cannot be played in the same position
            if char in self.yellows[idx]:
                if debug:
                    print("Failed -> yellow cannot be played in the same position")
                return False

            if char in self.greys.keys() and char not in self.targetWord:
                if debug:
                    print("Failed -> grey cannot be played in any position")
                return False

            if char in self.targetWord and char in self.greys.keys():
                if debug:
                    print("grey duplicated condition triggered")
                # count no of chars
                count = 0
                for i in range(5):
                    if char == word[i]:
                        if debug:
                            print(f"char: {word[i]}")
                    # if char == self.targetWord[i]:
                        count += 1
                if debug:
                    print(f"count: {count} self.greys[char]: {self.greys[char]} count <= self.greys[char]: {count <= self.greys[char]}")
                # if not too many
                if count <= self.greys[char]:
                    continue
                if debug:
                    print("Failed -> grey cannot be played in any position")
                return False
        # condition: check if all yellows are played
        for posV in self.yellows:
            for charYellow in posV:
                if charYellow not in word:
                    return False
        return True

    def __str__(self):
        if len(self.guesses) == 0:
            return "Round 0\n?????"
        if self.verbose:
            return f"Round {len(self.guesses)}:\nWord choices: {len(self.validWords)}\n{self.guesses[-1]}\n{''.join(self.colours)}"
        return f"Round {len(self.guesses)}:\n{self.guesses[-1]}\n{''.join(self.colours)}"
