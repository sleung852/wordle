from wordle import Wordle
import multiprocessing
from tqdm import tqdm
from agents import HeuristicAgent
import csv

def filter_word(word, missing_alphabet):
    for i in range(5):
        if word[i] not in missing_alphabet:
            return False
    return True

def filter_word_2(word):
    if word[1] == "A":
        return False
    return True

"""
Leveraging Multi-processing
"""

def breathFirstSearch(n=4):
    assert n > 0, "No. of processes cannot be 0 or negative"
    game = Wordle()
    wordChoices = compute_filtered_words()
    if n == 1:
        return worker(wordChoices)
    split = int(len(wordChoices) / n)
    wordChoicesList = []

    for p in range(n-1):
        wordChoicesList.append(wordChoices[p*split:(p+1)*split])
    wordChoicesList.append(wordChoices[(p+1)*split:])
    
    pool = multiprocessing.Pool(processes=n)
    pool.map(worker, wordChoicesList)

def worker(wordChoices, verbose=False):
    # outputs
    longestGuesses = []
    maxSteps = 0
    agent = HeuristicAgent()
    for wordChoice in tqdm(wordChoices):
        gameState = Wordle()
        gameState.word_list = compute_filtered_words()
        gameState.setTarget(wordChoice)
        words, _ = agent.getAction(gameState)
        nextGameStates = [gameState.step(word) for word in words]
        while nextGameStates:
            temp = []
            for nextGameState in nextGameStates:
                words, _ = agent.getAction(nextGameState)
                for word in words:
                    nextNextGameState = nextGameState.step(word)
                    if nextNextGameState.finished:
                        if len(nextNextGameState.guesses) > maxSteps:
                            maxSteps = len(nextNextGameState.guesses)
                            longestGuesses = nextNextGameState.guesses
                            print("Longest Length: ", maxSteps)
                            # print result
                            result_str = ""
                            guesses = nextNextGameState.guesses
                            for i, gw in enumerate(guesses):
                                if (i != len(guesses)-1):
                                    result_str += (gw + "->")
                                else:
                                    result_str += gw
                            print(result_str)
                    else:
                        temp.append(nextNextGameState)
            nextGameStates = temp
    print(longestGuesses)
    print(len(longestGuesses))

def compute_filtered_words():
    chars = []
    seq = ['KAPPA', 'TATTY', 'MAMMY', 'JAZZY', 'BAGGY', 'NANNY', 'DANDY', 'CANDY', 'SANDY']
    print(len(seq))
    for word in seq:
        for i in range(5):
            if word[i] not in chars:
                chars.append(word[i])
    alphabet = [c for c in "ABCDEFGHIJKLMNOPQRSTUVWXYZ"]
    missing_alphabet = alphabet
    for c in chars:
        missing_alphabet.remove(c)
    missing_alphabet = missing_alphabet + ['A']

    out = csv.reader(open('Eldrow Wordlist - Sheet1.csv', 'r'))
    word_list = [line[0] for line in out]
    
    filtered_words = []
    for word in word_list:
        if filter_word(word, missing_alphabet) and filter_word_2(word) and (word not in seq):
            filtered_words.append(word)
    return filtered_words


if __name__ == "__main__":
    breathFirstSearch(10)
