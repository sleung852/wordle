import csv
from copy import deepcopy
import random

from pyparsing import Word

# ['FUZZY', 'VIVID', 'MAMMA', 'CHECK', 'RETRO', 'ERROR', 'GONER', 'BOXER', 'WOOER', 'POWER', 'SOWER', 'LOWER']

class Eldrow:
    def __init__(self):
        self.state = []
        # helper variables
        self.setup()
        
    def setup(self):
        out = csv.reader(open('Eldrow Wordlist - Sheet1.csv', 'r'))
        self.word_list = [line[0] for line in out]
        
    def setTarget(self, target = "SANDY"):
        assert target in self.word_list, "Word is not valid to be target"
        self.target = target
        self.state = [target]
        self.validWords = self.word_list
        self.validWords.remove(target)  

    def step(self, word):
        if self._isLegalWord(word):
            self._isLegalWord(word, debug=True)
            print("HELOO!")
            assert False, f"{word} is an Illegal word"
        nextGameState = deepcopy(self)
        nextGameState.state.append(word)
        nextGameState.getLegalMoves()
        return nextGameState
        
    def getLegalMoves(self):
        validWords = []
        for word_choice in self.validWords:
            if (self._isLegalWord(word_choice)):
                validWords.append(word_choice)
        self.validWords = validWords

    def _isLegalWord(self, word, debug=True) -> bool:
        """
        word:   SANDY
        state: ['CIVIC', 'FLUFF', 'WHOOP', 'MAMMA', 'KAYAK',
                'JAZZY', 'BAGGY', 'TATTY', 'NANNY', 'DANDY',
                'RANDY', 'SANDY']
        """
        for word_state in self.state[1:]:
            for i in range(5):
                # green must be replayed (definitely correct)
                # ie target: APPLE->EXIST next: ABYSS (A cannot be in position 0)
                if (word[i] == self.target[i]) and (word[i] != word_state[i]):
                    if debug:
                        print("green must be replayed ")
                    return False
                # yellow cannot be replayed in the same position (definitely correct)
                # ie target: APPLE->EXIST next: EXTRA (E cannot be in position 0)
                if (word[i] != self.target[i]) and (word[i] == word_state[i]):
                    if debug:
                        print("yellow cannot be replayed in the same position")
                    return False
                # grey cannot be replayed (definitely correct)
                # ie target: APPLE->CIVIC next: COVER (C cannot be played since it does not exist)
                if (word[i] not in self.target) and (word[i] in word_state):
                    if debug:
                        print("grey cannot be replayed")
                    return False
                # yellow must be replayed 
                # if yellow and not in next word_state
                if (word[i] in self.target) and (word[i] != self.target[i]) and (word[i] not in word_state):
                    if debug:
                        print("yellow must be replayed")
                    return False
        return True

    def __str__(self):
        state = self.state[::-1]
        msg = state[0]
        for word in state[1:]:
            msg += f"->{word}"
        return msg
        
"""
SOWER -> ERROR -> LOWER
1. W(2) = W(2) or the last

POWER -> SOWER -> CHECK

? -> WORD_X -> WORD_TARGET

?[i] != WORD_TARGET[i] if WORD_X[i] != WORD_Y[i]


"""

if __name__ == "__main__":
    input_str_list = ['FUZZY', 'VIVID', 'MAMMA', 'CHECK', 'RETRO', 'ERROR', 'GONER', 'BOXER', 'WOOER', 'POWER', 'SOWER', 'LOWER']
    gs = Eldrow()
    target = input_str_list[-1]
    msg = target
    gs.setTarget(target)
    for word in input_str_list[::-1][1:]:
        msg = msg+"->"+word
        print(msg)
        gs = gs.step(word)
        print(f"no of words: {len(gs.validWords)}")
        print(gs.validWords)
        print()

# if __name__ == "__main__":
#     input_str_list = ['FUZZY', 'VIVID', 'MAMMA', 'CHECK', 'RETRO', 'ERROR', 'GONER', 'BOXER', 'WOOER', 'POWER', 'SOWER', 'LOWER']
#     gs = Eldrow()
#     target = input_str_list[-1]
#     msg = target
#     gs.setTarget(target)
#     for word in input_str_list[::-1][1:]:
#         msg = msg+"->"+word
#         print(msg)
#         gs = gs.step(word)
#         print(f"no of words: {len(gs.validWords)}")
#         print(gs.validWords)
#         print()


# if __name__ == "__main__":
#     gs = Eldrow()
#     target = "SANDY"
#     msg = target
#     gs.setTarget(target)
#     while (len(gs.validWords)>0):
#         print(f"no of words: {len(gs.validWords)}")
#         word = input("Enter a word now: ")
#         gs = gs.step(word)
#         msg = f"{word}->" + msg
#         print(msg)



# if __name__ == "__main__":
#     gs = Eldrow()
#     gs.setTarget("SANDY")
#     total = 15

#     count = 0
#     flag = True
#     while (count < 5):
#         gs = Eldrow()
#         gs.setTarget("SANDY")
#         total = 15
#         while (total > 0 and len(gs.validWords)>0):
#             word = random.choice(gs.validWords)
#             gs = gs.step(word)
#             print(gs)
#             total -= 1
#             if total == 0:
#                 print("Got one!")
#                 flag = False
#         count += 1

#     # l = [1,2,3]
#     # print(l[::-1])