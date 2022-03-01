import csv
from copy import deepcopy

def filter_wordchain(word, missing_alphabet):
    for i in range(5):
        if word[i] not in missing_alphabet:
            return False
    return True

def filter_lastword(word, lastword, targetword, seq):
    lastchar = [c for c in lastword]
    targetchar = [c for c in targetword]
    still_available_char = {}
    for char in lastchar:
        if char in targetchar and char not in still_available_char:
            still_available_char_idx = []
            i = 0
            found = lastword.find(char, 0)
            while (found != -1):
                still_available_char_idx.append(found)
                found = lastword.find(char, found+1)
            still_available_char[char] = still_available_char_idx
            
    target_counts = {c: targetword.count(c) for c in still_available_char.keys()}
    last_count = {c: lastword.count(c) for c in still_available_char.keys()}
                
    for char, idxs in still_available_char.items():
        
        count = word.count(char)
        if (last_count[char] > target_counts[char]):
            if (count >= last_count[char]):
                return False
        
        for idx in idxs:
            if (word[idx] == char) and (targetword[idx] != char):
                return False

            if (word[idx] == char) and (targetword[idx] == char) and (lastword[idx] != char):
                return False

            for i in range(5):
                if word[i] == char and lastword[i] != char and targetword[i] == word[i]:
                    return False
                
        lastwordcount = lastword.count(char)
        targetcount = targetword.count(char)
        if count > targetcount:
            for word_i in seq[:-1]:
                if word_i.count(char) > targetcount:
                    return False
        
    return True

def unique_chars_blah(lastword, targetword):
    lastchar = [c for c in lastword]
    targetchar = [c for c in targetword]
    still_available_char = {}
    for char in lastchar:
        if char in targetchar and char not in still_available_char:
            still_available_char[char] = 1
    return list(still_available_char.keys())

class gameEngine:
    
    def __init__(self, seq=[]):
        self.seq = seq
        self.yellows = []
        self.get_word_list()

        if len(seq) == 1:
            self.prepare_one()
        elif len(seq) > 0:
            self.prepare()
    
    def step(self, word):
        nextGamestate = deepcopy(self)
        nextGamestate.seq = [word] + nextGamestate.seq
        nextGamestate.prepare()
        return nextGamestate

    def prepare_one(self):
        self.legalwords.remove(self.seq[0])
    
    def prepare(self):
        
        # filter chars from seq
        self.chars = []
        for word in self.seq:
            for i in range(5):
                if word[i] not in self.chars:
                    self.chars.append(word[i])
                    
        missing_alphabet = [c for c in "ABCDEFGHIJKLMNOPQRSTUVWXYZ"]
        for c in self.chars:
            missing_alphabet.remove(c)
            
        missing_alphabet += unique_chars_blah(self.seq[0], self.seq[-1])

        filtered_words = []
        for word in self.legalwords:
            if filter_wordchain(word, missing_alphabet) and filter_lastword(word, self.seq[0], self.seq[-1], self.seq):
                filtered_words.append(word)
                
        self.legalwords = filtered_words
                    
    def get_word_list(self):
        out = csv.reader(open('Eldrow Wordlist - Sheet1.csv', 'r'))
        self.legalwords = [line[0] for line in out]
        
    def __str__(self):
        return str(self.seq)
    
    def __hash__(self):
        return hash(str(self))