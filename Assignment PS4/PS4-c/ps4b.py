# Problem Set 4B
# Name: Lynn Zhang
# Collaborators:
# Time Spent: 133min
# 2021-03-28 63min 10:39 - 11:42 understand the problem and write the class Message and debug
# 2021-03-29 70min 05:10 - 06:20 use class to decrypt a story message - true nature of using class.

import string


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


def get_story_string():
    """
    Returns: a story in encrypted text.
    """
    f = open("story.txt", "r")
    story = str(f.read())
    f.close()
    return story


### END HELPER CODE ###

WORDLIST_FILENAME = 'words.txt'
STORY_FILENAME = 'story.txt'

class Message(object):
    def __init__(self, text):
        '''
        Initializes a Message object

        text (string): the message's text

        a Message object has two attributes:
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

    def build_shift_dict(self, shift):
        '''
        Creates a dictionary that can be used to apply a cipher to a letter.
        The dictionary maps every uppercase and lowercase letter to a
        character shifted down the alphabet by the input shift. The dictionary
        should have 52 keys of all the uppercase letters and all the lowercase
        letters only.

        shift (integer): the amount by which to shift every letter of the
        alphabet. 0 <= shift < 26

        Returns: a dictionary mapping a letter (string) to
                 another letter (string).
        '''
        # all lower cases
        letters_lower = string.ascii_lowercase
        # all upper cases
        letters_upper = string.ascii_uppercase
        # create a dictionary
        dict_shift = {}

        # shift integer need to be less than 26: 0-26. %26
        shift = shift%26

        # loop in letters, put the letter into dict as key
        # find the key's index, and shift the index by integer (need to be less than the range),
        # find that letter and assign to its value

        # loop the lowercase letters
        index = 0
        for letter in letters_lower:
            # if index = 25 - end, index + shift should go back to the beginning again
            # if index + shift > len(letters_lower)
            if index + shift > len(letters_lower)-1:
                dict_shift[letter] = letters_lower[index+shift-len(letters_lower)]
            # else
            else:
                dict_shift[letter] = letters_lower[index+shift]
            index += 1
        # loop the uppercase letters, same as above
        # TODO: maybe use a function?
        index = 0
        for letter in letters_upper:
            if index + shift > len(letters_upper) - 1:
                dict_shift[letter] = letters_upper[index + shift - len(letters_upper)]
            else:
                dict_shift[letter] = letters_upper[index + shift]
            index += 1
        # return a dictionary shifted by integer
        return dict_shift

    def apply_shift(self, shift):
        '''
        Applies the Caesar Cipher to self.message_text with the input shift.
        Creates a new string that is self.message_text shifted down the
        alphabet by some number of characters determined by the input shift

        shift (integer): the shift with which to encrypt the message.
        0 <= shift < 26

        Returns: the message text (string) in which every character is shifted
             down the alphabet by the input shift
        '''
        # loop in the message, and shift every letter by the function build_shift_dict(self,shift)
        dict_shift = self.build_shift_dict(shift) #right?
        new_message = ''
        exceptions = " !@#$%^&*()-_+={}[]|\:;'<>?,./\""
        for letter in self.message_text:
            # exception dealing: spaces, punctations  (" !@#$%^&*()-_+={}[]|\:;'<>?,./\"")
            if letter in exceptions:
                # no change
                new_letter = letter
            # else if all letters, then shift according to the shift dictionary
            else:
                new_letter = dict_shift[letter]
            # add the letter into the new message
            new_message += new_letter
        # return new message with shifted letters
        return new_message


class PlaintextMessage(Message):
    def __init__(self, text, shift):
        '''
        Initializes a PlaintextMessage object

        text (string): the message's text
        shift (integer): the shift associated with this message

        A PlaintextMessage object inherits from Message and has five attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words)
            self.shift (integer, determined by input shift)
            self.encryption_dict (dictionary, built using shift)
            self.message_text_encrypted (string, created using shift)

        '''
        Message.__init__(self, text)
        self.shift = shift
        self.encryption_dict = self.build_shift_dict(shift)
        self.message_text_encrypted = self.apply_shift(shift)

    def get_shift(self):
        '''
        Used to safely access self.shift outside of the class

        Returns: self.shift
        '''
        return self.shift

    def get_encryption_dict(self):
        '''
        Used to safely access a copy self.encryption_dict outside of the class

        Returns: a COPY of self.encryption_dict
        '''
        # note: return a copy. why? - the dictionary is mutable, prevent someone from mutating the original dict
        return self.encryption_dict.copy()

    def get_message_text_encrypted(self):
        '''
        Used to safely access self.message_text_encrypted outside of the class

        Returns: self.message_text_encrypted
        '''
        return self.message_text_encrypted

    def change_shift(self, shift):
        '''
        Changes self.shift of the PlaintextMessage and updates other
        attributes determined by shift.

        shift (integer): the new shift that should be associated with this message.
        0 <= shift < 26

        Returns: nothing
        '''
        # change shift
        self.shift = shift
        # update other attributes determined by shift
        self.encryption_dict = self.build_shift_dict(shift)
        self.message_text_encrypted = self.apply_shift(shift)
        #todo: thinking about other methods?

class CiphertextMessage(Message):
    def __init__(self, text):
        '''
        Initializes a CiphertextMessage object

        text (string): the message's text

        a CiphertextMessage object has two attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words)
        '''
        Message.__init__(self, text)

    def decrypt_message(self):
        '''
        Decrypt self.message_text by trying every possible shift value
        and find the "best" one. We will define "best" as the shift that
        creates the maximum number of real words when we use apply_shift(shift)
        on the message text. If s is the original shift value used to encrypt
        the message, then we would expect 26 - s to be the best shift value
        for decrypting it.

        Note: if multiple shifts are equally good such that they all create
        the maximum number of valid words, you may choose any of those shifts
        (and their corresponding decrypted messages) to return

        Returns: a tuple of the best shift value used to decrypt the message
        and the decrypted message text using that shift value
        '''

        # try every shift from 0 to 25
        # find the one with maximum number of valid words

        # not ideal one, forget that there is attribute - valid_words
        # word_list =load_words(WORDLIST_FILENAME) # load the valid words list

        # keep track of the valid word count for each shift
        count_list = []

        for s in range(26):   # shift to try
            new_message = self.apply_shift(s)
            # check how many valid words are there in the new message
            # first - split the message by space
            wordlist = new_message.split()
            valid_word_count = 0      # keep track of the count of valid words
            # then - check each word validity
            for word in wordlist:
                # if valid word, then count + 1
                if is_word(self.valid_words, word): # self note: 1st attempt forget there is such attribute valid_words
                    valid_word_count += 1
            # add count number in the list
            count_list.append(valid_word_count)

        # find the max count in the list
        max_count = max(count_list)
        max_count_index = count_list.index(max_count)      # the index is actually the shift itself

        # decrypt the message using the shift
        decrypted_message = self.apply_shift(max_count_index)

        # return the tuple
        return (max_count_index, decrypted_message)


if __name__ == '__main__':


    # #Example test case (PlaintextMessage)
    # plaintext = PlaintextMessage('hello', 2)
    # print('Expected Output: jgnnq')
    # print('Actual Output:', plaintext.get_message_text_encrypted())

    # #Example test case (CiphertextMessage)
    # ciphertext = CiphertextMessage('jgnnq')
    # print('Expected Output:', (24, 'hello'))
    # print('Actual Output:', ciphertext.decrypt_message())

    # WRITE YOUR TEST CASES HERE

    # #Example test case (Message)
    # shift = 3
    # message = Message('hello, z')
    # print('Message is:',message.get_message_text())
    # # apply shift
    # print('Expected Output:', ('khoor, c'))
    # print('Encrypted Message is:', message.apply_shift(shift))
    #
    # # Example test case (Message)
    # shift = 3
    # message = Message('HELLO, Z')
    # print('Message is:', message.get_message_text())
    # # apply shift
    # print('Expected Output:', ('HKOOR, C'))
    # print('Encrypted Message is:', message.apply_shift(shift))

    # Part 4 - best shift value and unencrypted story:

    # load the story text to a string
    print("Loading story...")
    file = open(STORY_FILENAME)
    whole_story = file.read()   # the original story string
    print(whole_story)
    file.close()

    # decrypt the story
    # decrypt each word using the same shift.
    # and count the max words in the whole story. the max is the result

    # the above is exactly what is in ciphertext method
    # the beauty of using class!

    ciphertext = CiphertextMessage(whole_story)
    print('True Story:', ciphertext.decrypt_message())