from __future__ import division
import re
from curses.ascii import isdigit
from nltk.corpus import cmudict
d = cmudict.dict()


def phonemes(word):
    return max(d[word.lower()], key=len)


def nsyl(word):
    # return the max syllable count in the case of multiple pronunciations
    return max([len([y for y in x if isdigit(y[-1])]) for x in d[word.lower()]])
    # For example: d["concatenate".lower()] == [['K', 'AH0', 'N', 'K', 'AE1', 'T', 'AH0', 'N', 'EY2', 'T']]
    # Oh, and those numbers are actually stress/inflection (0: no stress, 1: primary stress, 2: secondary stress)
    # This grabs each item where the last character is a digit (how cmudict represents vowel sounds), and counts them
    # Algorithm via http://runningwithdata.com/post/3576752158/w


# Still needs code for fallback when a word isn't found in cmudict
def rhyme(word1, word2):
    reverse_word1 = max(d[word1.lower()], key=len)
    reverse_word1.reverse()
    reverse_word2 = max(d[word2.lower()], key=len)
    reverse_word2.reverse()
    for i, v in enumerate(reverse_word1):
        if isdigit(v[-1]):
            if reverse_word1[:i] == reverse_word2[:i]:
                return True
    return False


def rhyme_from_phonemes(word1, word2):  # Oh god refactor
    word1.reverse()
    word2.reverse()
    for i, v in enumerate(word1):
        if isdigit(v[-1]):
            if word1[:i] == word2[:i]:
                word1.reverse()  # Necessary, but surely there's a better way
                word2.reverse()
                return True
    word1.reverse()
    word2.reverse()
    return False


def tokenize(file_path, array):
    with open(file_path) as f:
        data = f.read()
        data = re.sub("[^a-zA-Z\s-]", '', data)
        data = re.sub("\s+", " ", data)
        words = re.split("\s|-", data)
        array += words
    if array[0] == '': del array[0]
    if array[-1] == '': del array[-1]

# Thinking about inflection:
# In "there once" [was a man from Nantucket], I'd want to see that "there" is unstressed, and "once" is stressed
# But cmudict sees the single vowel in each of them as 1 (primary stress), because it looks at each word in isolation
# Maybe for now just assume than monosyllabic words are flexible, and use cmudict for stress on polysyllabic words?
