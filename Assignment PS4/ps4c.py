# Problem Set 4C
# Name: Lynn Zhang
# Collaborators:
# Time Spent: 66min
# 2021-03-22 66min 06:26 - 07:28 stuck in the descrypt - how to change it back. the word count
#                        - 07:32 - solved - to get the dictionary's key with the maximum count:
#                                       wrong usage of max(count_dict)
#                                       shoud use:  max(count_dict, key=count_dict.get)

import string
from ps4a import get_permutations


### HELPER CODE ###
def load_words(file_name):
    '''
    file_name (string): the name of the file containing
    the list of words to load

    Returns: a list of valid words. Words are strings of lowercase letters.

    Depending on the size of the word list, this function may
    take a while to finish.
    '''

    print("Loading word list from file...")
    # inFile: file
    inFile = open(file_name, 'r')
    # wordlist: list of strings
    wordlist = []
    for line in inFile:
        wordlist.extend([word.lower() for word in line.split(' ')])
    print("  ", len(wordlist), "words loaded.")
    return wordlist


def is_word(word_list, word):
    '''
    Determines if word is a valid word, ignoring
    capitalization and punctuation

    word_list (list): list of words in the dictionary.
    word (string): a possible word.

    Returns: True if word is in word_list, False otherwise

    Example:
    >>> is_word(word_list, 'bat') returns
    True
    >>> is_word(word_list, 'asdf') returns
    False
    '''
    word = word.lower()
    word = word.strip(" !@#$%^&*()-_+={}[]|\:;'<>?,./\"")
    return word in word_list


### END HELPER CODE ###

WORDLIST_FILENAME = 'words.txt'

# you may find these constants helpful
VOWELS_LOWER = 'aeiou'
VOWELS_UPPER = 'AEIOU'
CONSONANTS_LOWER = 'bcdfghjklmnpqrstvwxyz'
CONSONANTS_UPPER = 'BCDFGHJKLMNPQRSTVWXYZ'


class SubMessage(object):
    def __init__(self, text):
        '''
        Initializes a SubMessage object

        text (string): the message's text

        A SubMessage object has two attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words)
        '''
        self.message_text = text
        self.valid_words = load_words(WORDLIST_FILENAME)

    def get_message_text(self):
        '''
        Used to safely access self.message_text outside of the class

        Returns: self.message_text
        '''
        return self.message_text

    def get_valid_words(self):
        '''
        Used to safely access a copy of self.valid_words outside of the class.
        This helps you avoid accidentally mutating class attributes.

        Returns: a COPY of self.valid_words
        '''
        return self.valid_words.copy()

    def build_transpose_dict(self, vowels_permutation):
        '''
        vowels_permutation (string): a string containing a permutation of vowels (a, e, i, o, u)

        Creates a dictionary that can be used to apply a cipher to a letter.
        The dictionary maps every uppercase and lowercase letter to an
        uppercase and lowercase letter, respectively. Vowels are shuffled
        according to vowels_permutation. The first letter in vowels_permutation
        corresponds to a, the second to e, and so on in the order a, e, i, o, u.
        The consonants remain the same. The dictionary should have 52
        keys of all the uppercase letters and all the lowercase letters.

        Example: When input "eaiuo":
        Mapping is a->e, e->a, i->i, o->u, u->o
        and "Hello World!" maps to "Hallu Wurld!"

        Returns: a dictionary mapping a letter (string) to
                 another letter (string).
        '''
        # transpose dictionary
        transpose_dict ={}
        # change all vowels permutation to lower first - easier
        vowels_permutation = vowels_permutation.lower()
        # for vowels, use the corresponding vowel in vowels permutation as its key
        i = 0
        for vowel in vowels_permutation:
            transpose_dict[VOWELS_LOWER[i]] = vowel
            transpose_dict[VOWELS_UPPER[i]] = vowel.upper()
            i += 1

        # for consonants, no change, but need to put into the dictionary, itself is its key
        for consonant in CONSONANTS_LOWER:
            transpose_dict[consonant] = consonant

        for consonant in CONSONANTS_UPPER:
            transpose_dict[consonant] = consonant
        # return
        return transpose_dict

    def apply_transpose(self, transpose_dict):
        '''
        transpose_dict (dict): a transpose dictionary

        Returns: an encrypted version of the message text, based
        on the dictionary
        '''
        message_copy = self.get_message_text()
        encrypted_message = ''
        exceptions = " !@#$%^&*()-_+={}[]|\:;'<>?,./\""

        for letter in message_copy:
            # if letter in exceptions
            if letter in exceptions:
                # no change
                new_letter = letter
            else:
            # otherwise map the letter according to the dictionary
                new_letter = transpose_dict[letter]
            # put the new letter in the message
            encrypted_message += new_letter

        return encrypted_message


class EncryptedSubMessage(SubMessage):
    def __init__(self, text):
        '''
        Initializes an EncryptedSubMessage object

        text (string): the encrypted message text

        An EncryptedSubMessage object inherits from SubMessage and has two attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words)
        '''
        SubMessage.__init__(self, text)

    def decrypt_message(self):
        '''
        Attempt to decrypt the encrypted message

        Idea is to go through each permutation of the vowels and test it
        on the encrypted message. For each permutation, check how many
        words in the decrypted text are valid English words, and return
        the decrypted message with the most English words.

        If no good permutations are found (i.e. no permutations result in
        at least 1 valid word), return the original string. If there are
        multiple permutations that yield the maximum number of words, return any
        one of them.

        Returns: the best decrypted message

        Hint: use your function from Part 4A
        '''
        # get the permutation LIST, and go through each of them
        permutations = get_permutations(VOWELS_LOWER)
        word_list = self.get_valid_words()
        count_dict = {} # is it good to use dict here? message(key): count of valid words(value)
        original_text = self.get_message_text()

        for p in permutations: # p is the vowels_permutation in the build_transpose_dict
            # print('permutation:',p)
            transpose_dict = self.build_transpose_dict(p)
            # create the descrypted message according to transpose_dict
            # find the vowels in the message, and change it back
            new_message = ''
            for letter in original_text:
                # if letter is a vowel, change
                if letter in VOWELS_LOWER:
                    # find the index of the letter in the permutation
                    index_vowel = p.find(letter)
                    # update the new letter
                    new_letter = VOWELS_LOWER[index_vowel]
                elif letter in VOWELS_UPPER:
                    # find the index of the letter in the permutation
                    index_vowel = p.find(letter.upper())
                    # update the new letter
                    new_letter = VOWELS_UPPER[index_vowel]
                # else no change
                else:
                    new_letter = letter
                # add in the new_message
                new_message += new_letter

            # new_message = self.apply_transpose(transpose_dict) # wrong logic!
            # check how many valid words are there
            # keep track of the valid word count
            valid_word_count = 0
            # self note: haven't splitted the new message into list of words
            for word in new_message.split():
                if is_word(word_list, word):
                    valid_word_count += 1
            count_dict[new_message] = valid_word_count
            # print('valid word count is', valid_word_count)
        # find the max valid word count in dict
        max_valid_word_count = max(count_dict.values())
        # if max = 0, return original
        if max_valid_word_count == 0:
            return original_text
        # else return the corresponding new message in the dict
        else:
            return max(count_dict, key=count_dict.get)    # get the dictionary's key with the maximum count

if __name__ == '__main__':
    # # Example test case
    # message = SubMessage("Hello World!")
    # permutation = "eaiuo"
    # enc_dict = message.build_transpose_dict(permutation)
    # print("Original message:", message.get_message_text(), "Permutation:", permutation)
    # print("Expected encryption:", "Hallu Wurld!")
    # print("Actual encryption:", message.apply_transpose(enc_dict))
    # enc_message = EncryptedSubMessage(message.apply_transpose(enc_dict))
    # print("Decrypted message:", enc_message.decrypt_message())

    # TODO: WRITE YOUR TEST CASES HERE
    # Example test case
    message = SubMessage("Pain + Reflection = Progress :) ")
    permutation = "euiao"
    enc_dict = message.build_transpose_dict(permutation)
    print("Original message:", message.get_message_text(), "Permutation:", permutation)
    print("Expected encryption:", "Pein + Rufluctian = Pragruss :) ")
    print("Actual encryption:", message.apply_transpose(enc_dict))
    enc_message = EncryptedSubMessage(message.apply_transpose(enc_dict))
    print("Decrypted message:", enc_message.decrypt_message())