from collections import Counter
import requests
import re

def get_word_lists():
    baseurl = 'https://www.powerlanguage.co.uk/wordle/'
    u = requests.get(baseurl)
    
    match = re.search(r"(main\..+?\.js)", u.text)
    u = requests.get(baseurl + match.group())

    La = re.search(r"La=\[(.+?)\]", u.text)
    possibles = [s[1:-1] for s in La.group(1).split(",")]

    Ta = re.search(r"Ta=\[(.+?)\]", u.text)
    fullwordlist = [s[1:-1] for s in Ta.group(1).split(",")]
    
    return possibles, fullwordlist

def get_letter_dist(words):
    letterdist = []
    for i in range(5):
        letterdist.append(Counter())
        for word in words:
            letterdist[i][word[i]] += 1
    return letterdist

def get_word_scores(words, letterdist):
    wordscores = Counter()
    for word in words:
        for i in range(5):
            wordscores[word] += letterdist[i][word[i]]
    return wordscores

def reduce_words(words, guess, guess_result):
    for i in range(5):
        if guess_result[i] == '0':
            words = [w for w in words if not w.count(guess[i])]
        elif guess_result[i] == '1':
            words = [w for w in words if w.count(guess[i]) and w[i] != guess[i]]
        elif guess_result[i] == '2':
            words = [w for w in words if w[i] == guess[i]]
    return words



words, all_words = get_word_lists()

for turn in range(6):
    letterdist = get_letter_dist(possibles)
    wordscores = get_word_scores(possibles, letterdist)
    guess = wordscores.most_common(1)[0][0]
    
    print(f'{len(possibles)} possible words remaining; the next best guess is: \'{guess}\'')
    result = input('What was the result?')
    possibles = reduce_words(possibles, guess, result)