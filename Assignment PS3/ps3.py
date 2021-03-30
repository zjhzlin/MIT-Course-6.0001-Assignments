# 6.0001 Problem Set 3
#
# The 6.0001 Word Game
# Created by: Kevin Luu <luuk> and Jenna Wiens <jwiens>
#
# Name          : Lynn ZHANG
# Collaborators :
# Time spent    : 198min
# 23/03/2021: 61min = 15min + 6min + 5min + 10min + 25min
# 24/03/2021: 137min
#            3 07:36-39 - debugging updated is_invalid - make wildcard test success;
#            42 07:55 - 08:37 problem 5
#            32 08:38 - 09:10 problem 6 substitute hand func
#            60 21:00 - 22:00 problem 6 done. with some issue with is_valid_word - solved - wrong order - need to find * first

import math
import random
import string

VOWELS = 'aeiou'
CONSONANTS = 'bcdfghjklmnpqrstvwxyz'
HAND_SIZE = 7

SCRABBLE_LETTER_VALUES = {
    'a': 1, 'b': 3, 'c': 3, 'd': 2, 'e': 1, 'f': 4, 'g': 2, 'h': 4, 'i': 1, 'j': 8, 'k': 5, 'l': 1,
    'm': 3, 'n': 1, 'o': 1, 'p': 3, 'q': 10, 'r': 1, 's': 1, 't': 1, 'u': 1, 'v': 4, 'w': 4, 'x': 8,
    'y': 4, 'z': 10, '*': 0
}

# -----------------------------------
# Helper code
# (you don't need to understand this helper code)

WORDLIST_FILENAME = "words.txt"

def load_words():
    """
    Returns a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    """
    
    print("Loading word list from file...")
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r')
    # wordlist: list of strings
    wordlist = []
    for line in inFile:
        wordlist.append(line.strip().lower())
    print("  ", len(wordlist), "words loaded.")
    return wordlist

def get_frequency_dict(sequence):
    """
    Returns a dictionary where the keys are elements of the sequence
    and the values are integer counts, for the number of times that
    an element is repeated in the sequence.

    sequence: string or list
    return: dictionary
    """
    
    # freqs: dictionary (element_type -> int)
    freq = {}
    for x in sequence:
        freq[x] = freq.get(x,0) + 1
    return freq
	

# (end of helper code)
# -----------------------------------

#
# Problem #1: Scoring a word
#
def get_word_score(word, n):
    """
    Returns the score for a word. Assumes the word is a
    valid word.

    You may assume that the input word is always either a string of letters, 
    or the empty string "". You may not assume that the string will only contain 
    lowercase letters, so you will have to handle uppercase and mixed case strings 
    appropriately. 

	The score for a word is the product of two components:

	The first component is the sum of the points for letters in the word.
	The second component is the larger of:
            1, or
            7*wordlen - 3*(n-wordlen), where wordlen is the length of the word
            and n is the hand length when the word was played

	Letters are scored as in Scrabble; A is worth 1, B is
	worth 3, C is worth 3, D is worth 2, E is worth 1, and so on.

    word: string
    n: int >= 0
    returns: int >= 0
    """

    # make the word into lower case
    word_lower = word.lower()
    wordlen= len(word)

    # first component: search through letters in the word
    sum_points = 0
    for letter in word_lower:
        # points for letters in the word - use of dictionary
        sum_points += SCRABBLE_LETTER_VALUES[letter]

    # second component: larger of the two
    second_comp = 7 * wordlen - 3 * (n-wordlen)
    if second_comp <= 1:
        second_comp = 1

    return sum_points * second_comp

# Make sure you understand how this function works and what it does!
#
def display_hand(hand):
    """
    Displays the letters currently in the hand.

    For example:
       display_hand({'a':1, 'x':2, 'l':3, 'e':1})
    Should print out something like:
       a x x l l l e
    The order of the letters is unimportant.

    hand: dictionary (string -> int)
    """
    
    for letter in hand.keys():
        for j in range(hand[letter]):
             print(letter, end=' ')      # print all on the same line
    print()                              # print an empty line

#
# Make sure you understand how this function works and what it does!
# You will need to modify this for Problem #4.
#
def deal_hand(n):
    """
    Returns a random hand containing n lowercase letters.
    ceil(n/3) letters in the hand should be VOWELS (note,
    ceil(n/3) means the smallest integer not less than n/3).

    Hands are represented as dictionaries. The keys are
    letters and the values are the number of times the
    particular letter is repeated in that hand.

    n: int >= 0
    returns: dictionary (string -> int)
    """
    
    num_vowels = int(math.ceil(n / 3))
    hand={'*':1}

    for i in range(num_vowels-1):
        x = random.choice(VOWELS)
        hand[x] = hand.get(x, 0) + 1
    
    for i in range(num_vowels, n):    
        x = random.choice(CONSONANTS)
        hand[x] = hand.get(x, 0) + 1
    
    return hand
#
# Problem #2: Update a hand by removing letters
#
def update_hand(hand, word):
    """
    Does NOT assume that hand contains every letter in word at least as
    many times as the letter appears in word. Letters in word that don't
    appear in hand should be ignored. Letters that appear in word more times
    than in hand should never result in a negative count; instead, set the
    count in the returned hand to 0 (or remove the letter from the
    dictionary, depending on how your code is structured). 

    Updates the hand: uses up the letters in the given word
    and returns the new hand, without those letters in it.

    Has no side effects: does not modify hand.

    word: string
    hand: dictionary (string -> int)    
    returns: dictionary (string -> int)
    """
    updated_hand = hand.copy()
    # FIXED self note: forget to lower the case
    # FROM TAO:
    # FIXME - not expected, BUG to fix later
    # TODO: should add feature X here
    # END FROM TAO
    word_lower = word.lower()
    # if * is used in the word, then update the * value as well
    if '*' in hand:
        for vowel in VOWELS:
        # if the vowel is in word but not in hand, then * is used
        # update the hand
            if word_lower.find(vowel) != -1 and vowel not in hand:  # self note: for param, no need for ' '
                updated_hand['*'] = 0
                break
        # else no * is used
    # loop the word
    for letter in word_lower:
        # check whether each letter is in hand
        # if in and the value is not 0, then update the hand value
        if letter in updated_hand:
            if updated_hand[letter] != 0:
                updated_hand[letter] -= 1
            # if value = 0, then still 0, no change.
    # del the key with value 0
    for letter in hand:
        if updated_hand[letter] == 0:
            del(updated_hand[letter])
    return updated_hand

#
# Problem #3: Test word validity
#
def is_valid_word(word, hand, word_list):
    """
    Returns True if word is in the word_list and is entirely
    composed of letters in the hand. Otherwise, returns False.
    Does not mutate hand or word_list.
   
    word: string
    hand: dictionary (string -> int)
    word_list: list of lowercase strings
    returns: boolean
    """
    word_lower = word.lower()
    updated_hand = hand.copy()

    # check whether the word is in the word list
    # if there is a wildcard
    if word_lower.find('*') != -1:
        # replace * with vowels and try to find a match, if find it, return true
        index = word_lower.find('*')
        word_l = list(word_lower)
        for vowel in VOWELS:
            word_l[index] = vowel
            updated_word = ''.join(word_l)
            if updated_word in word_list:
                return True
        return False
    # no wildcard, search directly
    elif word_lower not in word_list:
        return False
    else:
        return True

    # FIXME previous code will never get here
    # check whether the word is composed of letters in the hand
    for letter in word_lower:
        if letter not in updated_hand:
            return False
        else:
            if updated_hand[letter] == 0:
                return False
            else:
                updated_hand[letter] -= 1

#
# Problem #5: Playing a hand
#
def calculate_handlen(hand):
    """ 
    Returns the length (number of letters) in the current hand.
    
    hand: dictionary (string-> int)
    returns: integer
    """
    return len(hand.keys())

def play_hand(hand, word_list):

    """
    Allows the user to play the given hand, as follows:

    * The hand is displayed.
    
    * The user may input a word.

    * When any word is entered (valid or invalid), it uses up letters
      from the hand.

    * An invalid word is rejected, and a message is displayed asking
      the user to choose another word.

    * After every valid word: the score for that word is displayed,
      the remaining letters in the hand are displayed, and the user
      is asked to input another word.

    * The sum of the word scores is displayed when the hand finishes.

    * The hand finishes when there are no more unused letters.
      The user can also finish playing the hand by inputing two 
      exclamation points (the string '!!') instead of a word.

      hand: dictionary (string -> int)
      word_list: list of lowercase strings
      returns: the total score for the hand
      
    """
    
    # BEGIN PSEUDOCODE <-- Remove this comment when you implement this function
    # Keep track of the total score
    total_score = 0
    # As long as there are still letters left in the hand:
    n = calculate_handlen(hand) # number of letters available in the hand
    while n != 0:
        # Display the hand
        print('Current Hand:', end=' ') # print on the same line
        display_hand(hand)
        # Ask user for input
        word = input('Enter word, or "!!" to indicate that you are finished:')
        # If the input is two exclamation points:
        if word == '!!':
            # End the game (break out of the loop)
            break
            
        # Otherwise (the input is not two exclamation points):
        else:
            # If the word is valid:
            if is_valid_word(word, hand, word_list):
                # Tell the user how many points the word earned,
                # and the updated total score
                score = get_word_score(word, n)
                total_score += score
                print('"', word, '" earned',score,'points. Total:', total_score, 'points')
            # Otherwise (the word is not valid):
                # Reject invalid word (print a message)
            else:
                print('This is not a valid word. Please choose another word')
            # update the user's hand by removing the letters of their inputted word
            hand = update_hand(hand, word)
            n = calculate_handlen(hand)

    # Game is over (user entered '!!' or ran out of letters),
    # so tell user the total score
    if n == 0:
        print('Ran out of letters', end=' ')
    # Return the total score as result of function
    print('Total Score:', total_score, 'points')
    return total_score

#
# Problem #6: Playing a game
# 


#
# procedure you will use to substitute a letter in a hand
#

def substitute_hand(hand, letter):
    """ 
    Allow the user to replace all copies of one letter in the hand (chosen by user)
    with a new letter chosen from the VOWELS and CONSONANTS at random. The new letter
    should be different from user's choice, and should not be any of the letters
    already in the hand.

    If user provide a letter not in the hand, the hand should be the same.

    Has no side effects: does not mutate hand.

    For example:
        substitute_hand({'h':1, 'e':1, 'l':2, 'o':1}, 'l')
    might return:
        {'h':1, 'e':1, 'o':1, 'x':2} -> if the new letter is 'x'
    The new letter should not be 'h', 'e', 'l', or 'o' since those letters were
    already in the hand.
    
    hand: dictionary (string -> int)
    letter: string
    returns: dictionary (string -> int)
    """
    # assume the user enters a valid input

    # keep track of the updated hand
    updated_hand = hand.copy()
    # if the user provide a letter in the hand, then update hand
    if letter in updated_hand:
        # keep track of the chosen letter's value
        value = updated_hand[letter]
        # delete the letter user provides in the hand
        del(updated_hand[letter])
        # choose a random letter and it cannot be the same with the letters in the hand
        # define the random selection pool and choose from it
        Letters_to_choose = random_pool_select(hand)
        new_letter = random.choice(Letters_to_choose)
        # update the random letter in the hand with the previous value
        updated_hand[new_letter] = value
        # return updated hand
    # else simply return the same hand
    return updated_hand


def random_pool_select(hand):
    '''
    updated letters pool to randomly choose from without all the letters in the hand
    :param hand:dictionary (string -> int)
    :return: updated letters (string)
    '''
    letter_list = list(VOWELS+CONSONANTS)
    # delete the letters in the hand
    for letter in hand:
        if letter != '*':
            letter_list.remove(letter)
    updated_letters = ''.join(letter_list)
    return updated_letters

# print(substitute_hand({'h':1, '*':1, 'l':2, 'o':1}, 'l'))

def play_game(word_list):
    """
    Allow the user to play a series of hands

    * Asks the user to input a total number of hands

    * Accumulates the score for each hand into a total score for the 
      entire series
 
    * For each hand, before playing, ask the user if they want to substitute
      one letter for another. If the user inputs 'yes', prompt them for their
      desired letter. This can only be done once during the game. Once the
      substitue option is used, the user should not be asked if they want to
      substitute letters in the future.

    * For each hand, ask the user if they would like to replay the hand.
      If the user inputs 'yes', they will replay the hand and keep 
      the better of the two scores for that hand.  This can only be done once 
      during the game. Once the replay option is used, the user should not
      be asked if they want to replay future hands. Replaying the hand does
      not count as one of the total number of hands the user initially
      wanted to play.

            * Note: if you replay a hand, you do not get the option to substitute
                    a letter - you must play whatever hand you just had.
      
    * Returns the total score for the series of hands

    word_list: list of lowercase strings
    """
    # Asks the user to input a total number of hands
    num_hands = int(input("Enter total number of hands:"))

    # Accumulates the score for each hand into a total score for the entire series
    # keep track of the total score
    total_score = 0

    hand = deal_hand(HAND_SIZE)
    # dislay hand
    print('Current hand:',end=' ')
    display_hand(hand)

    # before playing, ask the user if they want to substitute one letter for another.
    substitute = input('Would you like to substitute a letter?')
    # if yes then ask for which letter to substitute then continue (only once in the game)
        # ask which letter to substitute
    if substitute.lower() == 'yes':
        letter_to_substitute = input('Which letter would you like to replace:')
        # then substitute according to user input
        updated_hand = substitute_hand(hand,letter_to_substitute)
    else:
        updated_hand = hand
    # while the num_hands not 0, then can still play
    while num_hands != 0:
        # play hand
        score = play_hand(updated_hand, word_list)
        # ask whether they would like to replay the hand
        replay = input('Would you like to replay the hand?')
        # if user wants to replay, then keep track of the current score - need to compare and update in the score
        if replay.lower() == 'yes':
            score_first = score
            # play again
            replay_hand = deal_hand(HAND_SIZE)
            score_second = play_hand(replay_hand, word_list)
            # compare the two scores and update the max to score
            if score_second > score_first:
                score = score_second
        # update the total score using the bigger score
        total_score += score
        # update number of hands
        num_hands -= 1
        # update a new hand
        updated_hand = deal_hand(HAND_SIZE)
    # FINISH
    print('----------')
    print('Total score over all hands:',total_score)

# Build data structures used for entire session and play game
# Do not remove the "if __name__ == '__main__':" line - this code is executed
# when the program is run directly, instead of through an import statement
#
if __name__ == '__main__':
    word_list = load_words()

    # hand = deal_hand(HAND_SIZE)
    # play_hand(hand,word_list)

    play_game(word_list)
